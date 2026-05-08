from datetime import timedelta

from app.domain import Loan, MemberType
from app.repositories.book_repository import InMemoryBookRepository
from app.repositories.errors import DataSourceError
from app.repositories.loan_repository import InMemoryLoanRepository
from app.repositories.member_repository import InMemoryMemberRepository
from app.services.errors import (
    BookAlreadyOnLoanError,
    BookNotFoundError,
    BookUnavailableError,
    InvalidReturnDateError,
    InvalidLoanDatesError,
    InvalidMemberStatusError,
    LoanAlreadyReturnedError,
    LoanCreationUnavailableError,
    LoanListUnavailableError,
    LoanNotAllowedError,
    LoanNotFoundError,
    LoanReturnUnavailableError,
    MemberNotFoundError,
    ReferenceOnlyLoanError,
)
from app.services.lending_policy_service import LendingPolicyService


class LoanService:
    def __init__(
        self,
        loan_repository: InMemoryLoanRepository,
        book_repository: InMemoryBookRepository | None = None,
        member_repository: InMemoryMemberRepository | None = None,
    ) -> None:
        # The repository is injected so service tests can use a fake data source.
        self.loan_repository = loan_repository
        self.book_repository = book_repository
        self.member_repository = member_repository
        self.policy = LendingPolicyService().get_policy()

    def list_loans(self) -> list[Loan]:
        # Ask the data layer for loans and translate data failures into a user-facing error.
        try:
            loans = self.loan_repository.list_loans()
            members = self.member_repository.list_members() if self.member_repository else []
            return [self._with_default_charges(loan, members) for loan in loans]
        except DataSourceError as error:
            raise LoanListUnavailableError() from error

    def create_loan(
        self,
        *,
        member_id: str,
        book_id: str,
        loan_date,
    ) -> Loan:
        try:
            members = self._list_members_for_creation()
            books = self._list_books_for_creation()
            loans = self.loan_repository.list_loans()
        except DataSourceError as error:
            raise LoanCreationUnavailableError() from error

        member = next((candidate for candidate in members if candidate.memberId == member_id), None)
        if member is None:
            raise MemberNotFoundError(member_id)

        member_type = self._member_type(member.memberType)

        if self._active_loan_count(member_id, loans) >= self.policy.maxActiveLoans:
            raise LoanNotAllowedError()

        book = next((candidate for candidate in books if candidate.bookId == book_id), None)
        if book is None:
            raise BookNotFoundError(book_id)

        if book.referenceOnly:
            raise ReferenceOnlyLoanError()

        if any(loan.bookId == book_id and loan.status == "active" for loan in loans):
            raise BookAlreadyOnLoanError()

        if not book.available:
            raise BookUnavailableError()

        due_date = loan_date + timedelta(days=self._loan_days(member_type))
        loan = Loan(
            loanId=self._next_loan_id(loans),
            bookId=book_id,
            memberId=member_id,
            loanDate=loan_date,
            dueDate=due_date,
            returnDate=None,
            initialLoanPrice=self._initial_loan_price(member_type, loan_date, due_date),
            currency=self.policy.currency,
        )
        return self.loan_repository.add_loan(loan)

    def return_loan(self, *, loan_id: str, return_date) -> Loan:
        try:
            loans = self.loan_repository.list_loans()
            members = self.member_repository.list_members() if self.member_repository else []
        except DataSourceError as error:
            raise LoanReturnUnavailableError() from error

        loan = next((candidate for candidate in loans if candidate.loanId == loan_id), None)
        if loan is None:
            raise LoanNotFoundError(loan_id)

        if loan.status == "returned":
            raise LoanAlreadyReturnedError(loan_id)

        if return_date < loan.loanDate:
            raise InvalidReturnDateError()

        member = next((candidate for candidate in members if candidate.memberId == loan.memberId), None)
        member_type = self._member_type(member.memberType) if member else MemberType.DEFAULT
        enriched_loan = self._with_default_charges(loan, members)
        overdue_days = max((return_date - loan.dueDate).days, 0)
        overdue_daily_price = self._overdue_daily_price(member_type, overdue_days)
        overdue_fine = self._overdue_fine(overdue_days)

        returned_loan = Loan(
            loanId=loan.loanId,
            bookId=loan.bookId,
            memberId=loan.memberId,
            loanDate=loan.loanDate,
            dueDate=loan.dueDate,
            returnDate=return_date,
            initialLoanPrice=enriched_loan.initialLoanPrice,
            overdueDailyPrice=overdue_daily_price,
            overdueFine=overdue_fine,
            currency=self.policy.currency,
        )

        try:
            return self.loan_repository.update_loan(returned_loan)
        except DataSourceError as error:
            raise LoanReturnUnavailableError() from error

    def _list_books_for_creation(self):
        if self.book_repository is None:
            raise DataSourceError("Book data could not be loaded.")
        return self.book_repository.list_books()

    def _list_members_for_creation(self):
        if self.member_repository is None:
            raise DataSourceError("Member data could not be loaded.")
        return self.member_repository.list_members()

    def _next_loan_id(self, loans: list[Loan]) -> str:
        max_id = 0
        for loan in loans:
            if loan.loanId.startswith("L") and loan.loanId[1:].isdigit():
                max_id = max(max_id, int(loan.loanId[1:]))
        return f"L{max_id + 1:03d}"

    def _member_type(self, raw_member_type: str) -> MemberType:
        try:
            return MemberType.from_text(raw_member_type)
        except Exception as error:
            raise InvalidMemberStatusError() from error

    def _loan_days(self, member_type: MemberType) -> int:
        if member_type == MemberType.STUDENT:
            return self.policy.studentLoanDays
        if member_type == MemberType.SENIOR:
            return self.policy.seniorLoanDays
        return self.policy.defaultLoanDays

    def _initial_loan_price(self, member_type: MemberType, loan_date, due_date) -> float:
        if member_type == MemberType.STUDENT:
            return self.policy.studentInitialLoanPrice
        return round((due_date - loan_date).days * self.policy.dailyLoanPrice, 2)

    def _overdue_daily_price(self, member_type: MemberType, overdue_days: int) -> float:
        if overdue_days <= 0:
            return 0.0
        if member_type == MemberType.STUDENT:
            return round(overdue_days * self.policy.studentOverdueDailyPrice, 2)
        return round(overdue_days * self.policy.dailyLoanPrice, 2)

    def _overdue_fine(self, overdue_days: int) -> float:
        if overdue_days <= 0:
            return 0.0
        return round(
            min(overdue_days * self.policy.dailyOverdueFine, self.policy.maxOverdueFine),
            2,
        )

    def _active_loan_count(self, member_id: str, loans: list[Loan]) -> int:
        return sum(
            1
            for loan in loans
            if loan.memberId == member_id and loan.status == "active"
        )

    def _with_default_charges(self, loan: Loan, members) -> Loan:
        if (
            loan.initialLoanPrice != 0.0
            or loan.overdueDailyPrice != 0.0
            or loan.overdueFine != 0.0
        ):
            return loan

        member = next((candidate for candidate in members if candidate.memberId == loan.memberId), None)
        member_type = self._member_type(member.memberType) if member else MemberType.DEFAULT
        return Loan(
            loanId=loan.loanId,
            bookId=loan.bookId,
            memberId=loan.memberId,
            loanDate=loan.loanDate,
            dueDate=loan.dueDate,
            returnDate=loan.returnDate,
            initialLoanPrice=self._initial_loan_price(member_type, loan.loanDate, loan.dueDate),
            overdueDailyPrice=loan.overdueDailyPrice,
            overdueFine=loan.overdueFine,
            currency=loan.currency,
        )

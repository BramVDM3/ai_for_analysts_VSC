from datetime import date

from app.domain import Book, Loan, Member
from app.repositories.errors import DataSourceError
from app.services.errors import (
    BookAlreadyOnLoanError,
    BookNotFoundError,
    BookUnavailableError,
    InvalidReturnDateError,
    InvalidMemberStatusError,
    LoanAlreadyReturnedError,
    LoanListUnavailableError,
    LoanNotAllowedError,
    LoanNotFoundError,
    MemberNotFoundError,
    ReferenceOnlyLoanError,
)
from app.services.loan_service import LoanService


class SuccessfulLoanRepository:
    def __init__(self, loans=None):
        self.loans = [
            Loan(
                loanId="L001",
                bookId="B006",
                memberId="M001",
                loanDate=date(2026, 1, 2),
                dueDate=date(2026, 1, 23),
                returnDate=None,
            )
        ] if loans is None else loans

    def list_loans(self):
        return list(self.loans)

    def add_loan(self, loan):
        self.loans.append(loan)
        return loan

    def update_loan(self, updated_loan):
        self.loans = [
            updated_loan if loan.loanId == updated_loan.loanId else loan
            for loan in self.loans
        ]
        return updated_loan


class FailingLoanRepository:
    def list_loans(self):
        raise DataSourceError("Loan list data could not be loaded.")


class SuccessfulBookRepository:
    def __init__(self, books=None):
        self.books = books or [
            Book(
                bookId="B002",
                title="Introduction to Data Science",
                category="education",
                referenceOnly=False,
                available=True,
            )
        ]

    def list_books(self):
        return list(self.books)


class SuccessfulMemberRepository:
    def __init__(self, members=None):
        self.members = members or [
            Member(
                memberId="M001",
                firstName="Emily",
                lastName="Johnson",
                email="emily.johnson@example.org",
                memberType="default",
                suspendedUntil=None,
                createdAt=date(2019, 3, 12),
            )
        ]

    def list_members(self):
        return list(self.members)


def test_loan_service_returns_loans_from_repository():
    loans = LoanService(SuccessfulLoanRepository()).list_loans()

    assert len(loans) == 1
    assert loans[0].loanId == "L001"
    assert loans[0].status == "active"


def test_loan_service_converts_data_errors_to_loan_list_error():
    service = LoanService(FailingLoanRepository())

    try:
        service.list_loans()
    except LoanListUnavailableError as error:
        assert error.code == "LOAN_LIST_UNAVAILABLE"
        assert str(error) == "Loan list data could not be loaded."
    else:
        raise AssertionError("Expected LoanListUnavailableError")


def test_loan_service_creates_active_loan():
    loan_repository = SuccessfulLoanRepository([])
    service = LoanService(
        loan_repository,
        SuccessfulBookRepository(),
        SuccessfulMemberRepository(),
    )

    loan = service.create_loan(
        member_id="M001",
        book_id="B002",
        loan_date=date(2026, 2, 1),
    )

    assert loan.loanId == "L001"
    assert loan.memberId == "M001"
    assert loan.bookId == "B002"
    assert loan.dueDate == date(2026, 2, 22)
    assert loan.initialLoanPrice == 21.0
    assert loan.overdueDailyPrice == 0.0
    assert loan.overdueFine == 0.0
    assert loan.totalDue == 21.0
    assert loan.returnDate is None
    assert loan.status == "active"
    assert loan_repository.list_loans() == [loan]


def test_loan_service_creates_free_initial_student_loan():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository(),
        SuccessfulMemberRepository(
            [
                Member(
                    memberId="M002",
                    firstName="Daniel",
                    lastName="Smith",
                    email="daniel.smith@example.org",
                    memberType="student",
                    suspendedUntil=None,
                    createdAt=date(2023, 9, 1),
                )
            ]
        ),
    )

    loan = service.create_loan(
        member_id="M002",
        book_id="B002",
        loan_date=date(2026, 2, 1),
    )

    assert loan.dueDate == date(2026, 2, 15)
    assert loan.initialLoanPrice == 0.0
    assert loan.totalDue == 0.0


def test_loan_service_creates_senior_loan_with_longer_period_and_daily_price():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository(),
        SuccessfulMemberRepository(
            [
                Member(
                    memberId="M003",
                    firstName="Patricia",
                    lastName="Walker",
                    email="patricia.walker@example.org",
                    memberType="senior",
                    suspendedUntil=None,
                    createdAt=date(2014, 9, 2),
                )
            ]
        ),
    )

    loan = service.create_loan(
        member_id="M003",
        book_id="B002",
        loan_date=date(2026, 2, 1),
    )

    assert loan.dueDate == date(2026, 3, 1)
    assert loan.initialLoanPrice == 28.0
    assert loan.totalDue == 28.0


def test_loan_service_rejects_missing_member():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository(),
        SuccessfulMemberRepository([]),
    )

    try:
        service.create_loan(
            member_id="M999",
            book_id="B002",
            loan_date=date(2026, 2, 1),
        )
    except MemberNotFoundError as error:
        assert error.code == "MEMBER_NOT_FOUND"
    else:
        raise AssertionError("Expected MemberNotFoundError")


def test_loan_service_rejects_missing_book():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository([]),
        SuccessfulMemberRepository(),
    )

    try:
        service.create_loan(
            member_id="M001",
            book_id="B999",
            loan_date=date(2026, 2, 1),
        )
    except BookNotFoundError as error:
        assert error.code == "BOOK_NOT_FOUND"
    else:
        raise AssertionError("Expected BookNotFoundError")


def test_loan_service_rejects_reference_only_book():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository(
            [
                Book(
                    bookId="B003",
                    title="Oxford English Dictionary",
                    category="reference",
                    referenceOnly=True,
                    available=True,
                )
            ]
        ),
        SuccessfulMemberRepository(),
    )

    try:
        service.create_loan(
            member_id="M001",
            book_id="B003",
            loan_date=date(2026, 2, 1),
        )
    except ReferenceOnlyLoanError as error:
        assert error.code == "REFERENCE_ONLY"
    else:
        raise AssertionError("Expected ReferenceOnlyLoanError")


def test_loan_service_rejects_unavailable_book_without_active_loan():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository(
            [
                Book(
                    bookId="B099",
                    title="Temporarily Missing Book",
                    category="fiction",
                    referenceOnly=False,
                    available=False,
                )
            ]
        ),
        SuccessfulMemberRepository(),
    )

    try:
        service.create_loan(
            member_id="M001",
            book_id="B099",
            loan_date=date(2026, 2, 1),
        )
    except BookUnavailableError as error:
        assert error.code == "BOOK_UNAVAILABLE"
    else:
        raise AssertionError("Expected BookUnavailableError")


def test_loan_service_rejects_book_with_active_loan():
    service = LoanService(
        SuccessfulLoanRepository(
            [
                Loan(
                    loanId="L001",
                    bookId="B002",
                    memberId="M002",
                    loanDate=date(2026, 1, 1),
                    dueDate=date(2026, 1, 22),
                    returnDate=None,
                )
            ]
        ),
        SuccessfulBookRepository(),
        SuccessfulMemberRepository(),
    )

    try:
        service.create_loan(
            member_id="M001",
            book_id="B002",
            loan_date=date(2026, 2, 1),
        )
    except BookAlreadyOnLoanError as error:
        assert error.code == "BOOK_ALREADY_ON_LOAN"
    else:
        raise AssertionError("Expected BookAlreadyOnLoanError")


def test_loan_service_rejects_unsupported_member_status():
    service = LoanService(
        SuccessfulLoanRepository([]),
        SuccessfulBookRepository(),
        SuccessfulMemberRepository(
            [
                Member(
                    memberId="M004",
                    firstName="Unknown",
                    lastName="Member",
                    email="unknown.member@example.org",
                    memberType="unknown",
                    suspendedUntil=None,
                    createdAt=date(2026, 1, 1),
                )
            ]
        ),
    )

    try:
        service.create_loan(
            member_id="M004",
            book_id="B002",
            loan_date=date(2026, 2, 1),
        )
    except InvalidMemberStatusError as error:
        assert error.code == "INVALID_MEMBER_STATUS"
    else:
        raise AssertionError("Expected InvalidMemberStatusError")


def test_loan_service_rejects_member_at_active_loan_limit_with_generic_error():
    active_loans = [
        Loan(
            loanId=f"L00{index}",
            bookId=f"B10{index}",
            memberId="M001",
            loanDate=date(2026, 1, 1),
            dueDate=date(2026, 1, 22),
            returnDate=None,
        )
        for index in range(1, 6)
    ]
    service = LoanService(
        SuccessfulLoanRepository(active_loans),
        SuccessfulBookRepository(),
        SuccessfulMemberRepository(),
    )

    try:
        service.create_loan(
            member_id="M001",
            book_id="B002",
            loan_date=date(2026, 2, 1),
        )
    except LoanNotAllowedError as error:
        assert error.code == "LOAN_NOT_ALLOWED"
        assert str(error) == "The loan could not be created."
    else:
        raise AssertionError("Expected LoanNotAllowedError")


def test_loan_service_marks_active_loan_as_returned():
    loan_repository = SuccessfulLoanRepository()
    service = LoanService(loan_repository, member_repository=SuccessfulMemberRepository())

    loan = service.return_loan(
        loan_id="L001",
        return_date=date(2026, 1, 12),
    )

    assert loan.returnDate == date(2026, 1, 12)
    assert loan.status == "returned"
    assert loan.overdueDailyPrice == 0.0
    assert loan.overdueFine == 0.0
    assert loan_repository.list_loans()[0].status == "returned"


def test_loan_service_charges_student_daily_price_and_fine_after_initial_period():
    loan_repository = SuccessfulLoanRepository(
        [
            Loan(
                loanId="L001",
                bookId="B002",
                memberId="M002",
                loanDate=date(2026, 2, 1),
                dueDate=date(2026, 2, 15),
                returnDate=None,
                initialLoanPrice=0.0,
            )
        ]
    )
    service = LoanService(
        loan_repository,
        member_repository=SuccessfulMemberRepository(
            [
                Member(
                    memberId="M002",
                    firstName="Daniel",
                    lastName="Smith",
                    email="daniel.smith@example.org",
                    memberType="student",
                    suspendedUntil=None,
                    createdAt=date(2023, 9, 1),
                )
            ]
        ),
    )

    loan = service.return_loan(
        loan_id="L001",
        return_date=date(2026, 2, 22),
    )

    assert loan.overdueDailyPrice == 7.0
    assert loan.overdueFine == 1.75
    assert loan.totalDue == 8.75


def test_loan_service_caps_overdue_fine_but_not_overdue_daily_price():
    loan_repository = SuccessfulLoanRepository(
        [
            Loan(
                loanId="L001",
                bookId="B002",
                memberId="M002",
                loanDate=date(2026, 2, 1),
                dueDate=date(2026, 2, 15),
                returnDate=None,
                initialLoanPrice=0.0,
            )
        ]
    )
    service = LoanService(
        loan_repository,
        member_repository=SuccessfulMemberRepository(
            [
                Member(
                    memberId="M002",
                    firstName="Daniel",
                    lastName="Smith",
                    email="daniel.smith@example.org",
                    memberType="student",
                    suspendedUntil=None,
                    createdAt=date(2023, 9, 1),
                )
            ]
        ),
    )

    loan = service.return_loan(
        loan_id="L001",
        return_date=date(2026, 5, 1),
    )

    assert loan.overdueDailyPrice == 75.0
    assert loan.overdueFine == 10.0
    assert loan.totalDue == 85.0


def test_loan_service_rejects_missing_loan_return():
    service = LoanService(SuccessfulLoanRepository([]))

    try:
        service.return_loan(loan_id="L999", return_date=date(2026, 1, 12))
    except LoanNotFoundError as error:
        assert error.code == "LOAN_NOT_FOUND"
    else:
        raise AssertionError("Expected LoanNotFoundError")


def test_loan_service_rejects_already_returned_loan():
    service = LoanService(
        SuccessfulLoanRepository(
            [
                Loan(
                    loanId="L001",
                    bookId="B002",
                    memberId="M001",
                    loanDate=date(2026, 1, 2),
                    dueDate=date(2026, 1, 23),
                    returnDate=date(2026, 1, 10),
                )
            ]
        )
    )

    try:
        service.return_loan(loan_id="L001", return_date=date(2026, 1, 12))
    except LoanAlreadyReturnedError as error:
        assert error.code == "LOAN_ALREADY_RETURNED"
    else:
        raise AssertionError("Expected LoanAlreadyReturnedError")


def test_loan_service_rejects_return_date_before_loan_date():
    service = LoanService(SuccessfulLoanRepository())

    try:
        service.return_loan(loan_id="L001", return_date=date(2026, 1, 1))
    except InvalidReturnDateError as error:
        assert error.code == "INVALID_RETURN_DATE"
    else:
        raise AssertionError("Expected InvalidReturnDateError")

from dataclasses import dataclass, field
from datetime import date

from app.domain.loan_status import LoanStatus
from app.domain.validation import require_date, require_text


@dataclass(frozen=True)
class Loan:
    loanId: str
    bookId: str
    memberId: str
    loanDate: date
    dueDate: date
    returnDate: date | None
    initialLoanPrice: float = 0.0
    overdueDailyPrice: float = 0.0
    overdueFine: float = 0.0
    currency: str = "EUR"
    status: str = field(init=False)
    totalDue: float = field(init=False)

    def __post_init__(self) -> None:
        # Validate required loan fields and derive status from the return date.
        require_text(self.loanId, "Loan id is required.")
        require_text(self.bookId, "Book id is required.")
        require_text(self.memberId, "Member id is required.")
        require_date(self.loanDate, "Loan date is required.")
        require_date(self.dueDate, "Loan due date is required.")
        require_text(self.currency, "Loan currency is required.")

        object.__setattr__(self, "status", self._derive_status())
        object.__setattr__(
            self,
            "totalDue",
            round(self.initialLoanPrice + self.overdueDailyPrice + self.overdueFine, 2),
        )

    def _derive_status(self) -> str:
        # A loan without a return date is still active; otherwise it is returned.
        if self.returnDate is None:
            return LoanStatus.ACTIVE.value
        return LoanStatus.RETURNED.value

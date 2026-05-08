from dataclasses import dataclass


@dataclass(frozen=True)
class LendingPolicy:
    supportedMemberStatuses: tuple[str, ...] = ("default", "student", "senior")
    defaultLoanDays: int = 21
    studentLoanDays: int = 14
    seniorLoanDays: int = 28
    studentInitialLoanPrice: float = 0.0
    dailyLoanPrice: float = 1.0
    studentOverdueDailyPrice: float = 1.0
    dailyOverdueFine: float = 0.25
    maxOverdueFine: float = 10.0
    maxActiveLoans: int = 5
    currency: str = "EUR"

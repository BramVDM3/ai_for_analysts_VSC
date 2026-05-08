from pydantic import BaseModel


class LendingPolicyResponse(BaseModel):
    supportedMemberStatuses: list[str]
    defaultLoanDays: int
    studentLoanDays: int
    seniorLoanDays: int
    studentInitialLoanPrice: float
    dailyLoanPrice: float
    studentOverdueDailyPrice: float
    dailyOverdueFine: float
    maxOverdueFine: float
    maxActiveLoans: int
    currency: str

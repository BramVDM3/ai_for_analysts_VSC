from datetime import date

from pydantic import BaseModel


class LoanResponse(BaseModel):
    # Shape of a loan object returned by the API to the frontend.
    loanId: str
    bookId: str
    memberId: str
    loanDate: date
    dueDate: date
    returnDate: date | None
    status: str
    initialLoanPrice: float
    overdueDailyPrice: float
    overdueFine: float
    totalDue: float
    currency: str


class CreateLoanRequest(BaseModel):
    memberId: str
    bookId: str
    loanDate: date


class ReturnLoanRequest(BaseModel):
    returnDate: date

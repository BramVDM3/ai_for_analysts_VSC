from datetime import date

from pydantic import BaseModel

from app.schemas.loan import LoanResponse


class MemberResponse(BaseModel):
    # Shape of a member object returned by the API to the frontend.
    memberId: str
    firstName: str
    lastName: str
    email: str
    memberType: str
    suspendedUntil: date | None
    createdAt: date


class MemberOverviewResponse(BaseModel):
    # Shape returned when the frontend opens a focused member overview.
    member: MemberResponse
    loans: list[LoanResponse]

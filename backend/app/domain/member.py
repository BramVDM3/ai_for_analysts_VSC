from dataclasses import dataclass
from datetime import date

from app.domain.validation import require_date, require_text


@dataclass(frozen=True)
class Member:
    memberId: str
    firstName: str
    lastName: str
    email: str
    memberType: str
    suspendedUntil: date | None
    createdAt: date

    def __post_init__(self) -> None:
        # Validate the required member fields while allowing suspendedUntil to stay optional.
        require_text(self.memberId, "Member id is required.")
        require_text(self.firstName, "Member first name is required.")
        require_text(self.lastName, "Member last name is required.")
        require_text(self.email, "Member email is required.")
        require_text(self.memberType, "Member type is required.")
        require_date(self.createdAt, "Member creation date is required.")

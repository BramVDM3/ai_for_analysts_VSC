from enum import Enum

from app.domain.validation import enum_from_value, normalize_required_value


class LoanStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"

    @classmethod
    def from_text(cls, value: str | None) -> "LoanStatus":
        # Convert raw text from an API or CSV into a supported loan status.
        normalized = normalize_required_value(value, "Loan status is required.")
        return enum_from_value(cls, normalized, "Unsupported loan status.")

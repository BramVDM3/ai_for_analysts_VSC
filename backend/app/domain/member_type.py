from enum import Enum

from app.domain.validation import enum_from_value, normalize_required_value


class MemberType(str, Enum):
    DEFAULT = "default"
    STUDENT = "student"
    SENIOR = "senior"

    @classmethod
    def from_text(cls, value: str | None) -> "MemberType":
        # Convert raw text from an API or CSV into a supported member type.
        normalized = normalize_required_value(value, "Member type is required.")
        if normalized == "adult":
            normalized = cls.DEFAULT.value
        return enum_from_value(cls, normalized, "Unsupported member type.")

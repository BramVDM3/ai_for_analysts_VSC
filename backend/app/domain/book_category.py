from enum import Enum

from app.domain.validation import enum_from_value, normalize_required_value


class BookCategory(str, Enum):
    FICTION = "fiction"
    EDUCATION = "education"
    REFERENCE = "reference"
    TECHNOLOGY = "technology"
    ARTS = "arts"
    NON_FICTION = "non-fiction"
    CHILDREN = "children"
    HISTORY = "history"

    @classmethod
    def from_text(cls, value: str | None) -> "BookCategory":
        # Convert raw text from an API or CSV into a supported book category.
        normalized = normalize_required_value(value, "Book category is required.")
        return enum_from_value(cls, normalized, "Unsupported book category.")

from dataclasses import dataclass

from app.domain.validation import require_boolean, require_text


@dataclass(frozen=True)
class Book:
    bookId: str
    title: str
    category: str
    referenceOnly: bool
    available: bool
    status: str | None = None

    def __post_init__(self) -> None:
        # Validate the core book fields as soon as a Book object is created.
        require_text(self.bookId, "Book id is required.")
        require_text(self.title, "Book title is required.")
        require_text(self.category, "Book category is required.")
        require_boolean(self.referenceOnly, "Book reference-only must be true or false.")
        require_boolean(self.available, "Book availability must be true or false.")

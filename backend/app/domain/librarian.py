from dataclasses import dataclass

from app.domain.validation import require_text


@dataclass(frozen=True)
class Librarian:
    librarianId: str
    firstName: str
    lastName: str
    email: str

    def __post_init__(self) -> None:
        # Validate the required identity fields for a librarian.
        require_text(self.librarianId, "Librarian id is required.")
        require_text(self.firstName, "Librarian first name is required.")
        require_text(self.lastName, "Librarian last name is required.")
        require_text(self.email, "Librarian email is required.")

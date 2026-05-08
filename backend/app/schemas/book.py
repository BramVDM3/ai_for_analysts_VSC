from pydantic import BaseModel


class BookResponse(BaseModel):
    # Shape of a book object returned by the API to the frontend.
    bookId: str
    title: str
    category: str
    referenceOnly: bool
    available: bool
    status: str

    @classmethod
    def from_attributes(cls, book):
        if book.status:
            status = book.status
        elif book.referenceOnly:
            status = "reference-only"
        elif not book.available:
            status = "unavailable"
        else:
            status = "available"
        return cls(
            bookId=book.bookId,
            title=book.title,
            category=book.category,
            referenceOnly=book.referenceOnly,
            available=book.available,
            status=status,
        )

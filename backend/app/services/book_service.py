from app.domain import Book
from app.repositories.book_repository import InMemoryBookRepository
from app.repositories.errors import DataSourceError
from app.repositories.loan_repository import InMemoryLoanRepository
from app.services.errors import BookCatalogueUnavailableError


class BookService:
    def __init__(
        self,
        book_repository: InMemoryBookRepository,
        loan_repository: InMemoryLoanRepository | None = None,
    ) -> None:
        # The repository is injected so service tests can use a fake data source.
        self.book_repository = book_repository
        self.loan_repository = loan_repository

    def list_books(self) -> list[Book]:
        # Ask the data layer for books and translate data failures into a business-facing error.
        try:
            books = self.book_repository.list_books()
            loans = self.loan_repository.list_loans() if self.loan_repository else []
        except DataSourceError as error:
            raise BookCatalogueUnavailableError() from error

        active_book_ids = {loan.bookId for loan in loans if loan.status == "active"}
        return [
            Book(
                bookId=book.bookId,
                title=book.title,
                category=book.category,
                referenceOnly=book.referenceOnly,
                available=book.available and book.bookId not in active_book_ids,
                status="lent" if book.bookId in active_book_ids else None,
            )
            for book in books
        ]

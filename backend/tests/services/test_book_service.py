from datetime import date

from app.domain import Book, Loan
from app.repositories.errors import DataSourceError
from app.services.book_service import BookService
from app.services.errors import BookCatalogueUnavailableError


class SuccessfulBookRepository:
    def list_books(self):
        return [
            Book(
                bookId="B001",
                title="The Great Gatsby",
                category="fiction",
                referenceOnly=False,
                available=True,
            )
        ]


class FailingBookRepository:
    def list_books(self):
        raise DataSourceError("Book catalogue data could not be loaded.")


class LoanRepository:
    def __init__(self, loans):
        self.loans = loans

    def list_loans(self):
        return list(self.loans)


def test_book_service_returns_books_from_repository():
    books = BookService(SuccessfulBookRepository()).list_books()

    assert len(books) == 1
    assert books[0].bookId == "B001"


def test_book_service_converts_data_errors_to_catalogue_error():
    service = BookService(FailingBookRepository())

    try:
        service.list_books()
    except BookCatalogueUnavailableError as error:
        assert error.code == "BOOK_CATALOGUE_UNAVAILABLE"
        assert str(error) == "Book catalogue data could not be loaded."
    else:
        raise AssertionError("Expected BookCatalogueUnavailableError")


def test_book_service_marks_books_with_active_loans_as_lent():
    service = BookService(
        SuccessfulBookRepository(),
        LoanRepository(
            [
                Loan(
                    loanId="L001",
                    bookId="B001",
                    memberId="M001",
                    loanDate=date(2026, 1, 1),
                    dueDate=date(2026, 1, 22),
                    returnDate=None,
                )
            ]
        ),
    )

    books = service.list_books()

    assert books[0].available is False
    assert books[0].status == "lent"


def test_book_service_ignores_returned_loans_for_availability():
    service = BookService(
        SuccessfulBookRepository(),
        LoanRepository(
            [
                Loan(
                    loanId="L001",
                    bookId="B001",
                    memberId="M001",
                    loanDate=date(2026, 1, 1),
                    dueDate=date(2026, 1, 22),
                    returnDate=date(2026, 1, 15),
                )
            ]
        ),
    )

    books = service.list_books()

    assert books[0].available is True
    assert books[0].status is None

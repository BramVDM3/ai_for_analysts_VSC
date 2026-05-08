from io import StringIO

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.book_repository import CsvBookRepository
from app.repositories.errors import DataSourceError
from app.routers.books import get_book_service
from app.services.book_service import BookService
from app.services.errors import BookCatalogueUnavailableError


class InMemoryBookSource:
    def __init__(self, content: str) -> None:
        self.content = content

    def open(self, newline="", encoding="utf-8-sig"):
        return StringIO(self.content)


class MissingBookSource:
    def open(self, newline="", encoding="utf-8-sig"):
        raise FileNotFoundError("missing books source")


def test_csv_book_repository_loads_books():
    source = InMemoryBookSource(
        "bookId,title,category,referenceOnly,available\n"
        "B001,The Great Gatsby,fiction,False,True\n"
    )

    books = CsvBookRepository(source).list_books()

    assert len(books) == 1
    assert books[0].bookId == "B001"
    assert books[0].title == "The Great Gatsby"
    assert books[0].category == "fiction"
    assert books[0].referenceOnly is False
    assert books[0].available is True


def test_csv_book_repository_returns_empty_list_for_empty_file():
    assert CsvBookRepository(InMemoryBookSource("")).list_books() == []


def test_csv_book_repository_raises_clear_error_when_file_is_missing():
    with pytest.raises(DataSourceError, match="Book catalogue data could not be loaded."):
        CsvBookRepository(MissingBookSource()).list_books()


def test_csv_book_repository_raises_clear_error_for_invalid_book_data():
    source = InMemoryBookSource(
        "bookId,title,category,referenceOnly,available\n"
        "B001,,fiction,False,True\n"
    )

    with pytest.raises(DataSourceError, match="Book catalogue data could not be loaded."):
        CsvBookRepository(source).list_books()


def test_book_service_returns_books_from_repository():
    source = InMemoryBookSource(
        "bookId,title,category,referenceOnly,available\n"
        "B001,The Great Gatsby,fiction,False,True\n"
    )

    books = BookService(CsvBookRepository(source)).list_books()

    assert len(books) == 1
    assert books[0].bookId == "B001"


def test_book_service_converts_data_errors_to_catalogue_error():
    service = BookService(CsvBookRepository(MissingBookSource()))

    with pytest.raises(BookCatalogueUnavailableError) as error:
        service.list_books()

    assert error.value.code == "BOOK_CATALOGUE_UNAVAILABLE"
    assert str(error.value) == "Book catalogue data could not be loaded."


def test_get_books_endpoint_returns_loan_aware_books():
    client = TestClient(app)

    response = client.get("/books")

    assert response.status_code == 200
    books = response.json()
    assert len(books) == 15
    assert books[0] == {
        "bookId": "B001",
        "title": "The Great Gatsby",
        "category": "fiction",
        "referenceOnly": False,
        "available": False,
        "status": "lent",
    }


class FailingBookService:
    def list_books(self):
        raise BookCatalogueUnavailableError()


def test_get_books_endpoint_returns_clear_error_when_catalogue_fails():
    app.dependency_overrides[get_book_service] = lambda: FailingBookService()
    client = TestClient(app)

    try:
        response = client.get("/books")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "code": "BOOK_CATALOGUE_UNAVAILABLE",
        "message": "Book catalogue data could not be loaded.",
    }

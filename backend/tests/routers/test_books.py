from fastapi.testclient import TestClient

from app.main import app
from app.routers.books import get_book_service
from app.services.errors import BookCatalogueUnavailableError


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

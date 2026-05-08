from fastapi.testclient import TestClient

from app.main import app


def test_get_books_endpoint_returns_all_in_memory_books():
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

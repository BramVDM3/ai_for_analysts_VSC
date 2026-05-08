from app.domain import Book
from app.repositories.book_repository import InMemoryBookRepository
from app.repositories.in_memory_data import BOOKS


def test_in_memory_book_repository_returns_seeded_books():
    books = InMemoryBookRepository().list_books()

    assert len(books) == 15
    assert books[0].bookId == "B001"
    assert books[0].title == "The Great Gatsby"
    assert books[0].category == "fiction"
    assert books[0].referenceOnly is False
    assert books[0].available is True


def test_in_memory_book_repository_accepts_injected_books():
    expected_books = [
        Book(
            bookId="B999",
            title="Injected Test Book",
            category="fiction",
            referenceOnly=False,
            available=True,
        )
    ]

    books = InMemoryBookRepository(expected_books).list_books()

    assert books == expected_books


def test_in_memory_book_repository_accepts_an_empty_injected_book_list():
    assert InMemoryBookRepository([]).list_books() == []


def test_in_memory_book_repository_returns_a_copy_of_the_book_list():
    books = InMemoryBookRepository().list_books()

    books.clear()

    assert len(BOOKS) == 15
    assert len(InMemoryBookRepository().list_books()) == 15

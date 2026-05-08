import csv

from app.domain import Book
from app.repositories.errors import DataSourceError
from app.repositories.in_memory_data import BOOKS


class InMemoryBookRepository:
    def __init__(self, books: list[Book] | None = None) -> None:
        # Allow tests to inject a small book list while production uses the seeded data.
        self.books = BOOKS if books is None else books

    def list_books(self) -> list[Book]:
        # Return a copy so callers cannot accidentally change the repository seed data.
        return list(self.books)


class CsvBookRepository:
    def __init__(self, source) -> None:
        # Retained for tests and optional source-file loading experiments.
        self.source = source

    def list_books(self) -> list[Book]:
        try:
            with self.source.open(newline="", encoding="utf-8-sig") as source_file:
                rows = csv.DictReader(source_file)
                return [
                    Book(
                        bookId=row.get("bookId", ""),
                        title=row.get("title", ""),
                        category=row.get("category", ""),
                        referenceOnly=self._to_bool(row.get("referenceOnly")),
                        available=self._to_bool(row.get("available")),
                    )
                    for row in rows
                ]
        except Exception as error:
            raise DataSourceError("Book catalogue data could not be loaded.") from error

    def _to_bool(self, value: str | None) -> bool:
        if value is None:
            raise ValueError("Boolean value is required.")
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
        raise ValueError("Boolean value must be true or false.")

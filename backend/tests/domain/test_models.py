from datetime import date

import pytest

from app.domain.errors import DomainValidationError
from app.domain.models import (
    Book,
    BookCategory,
    Librarian,
    Loan,
    LoanStatus,
    Member,
    MemberType,
)


def test_book_can_be_created_with_required_values():
    book = Book(
        bookId="B001",
        title="The Great Gatsby",
        category="fiction",
        referenceOnly=False,
        available=True,
    )

    assert book.bookId == "B001"
    assert book.title == "The Great Gatsby"
    assert book.category == "fiction"
    assert book.referenceOnly is False
    assert book.available is True


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("bookId", "", "Book id is required."),
        ("bookId", "   ", "Book id is required."),
        ("title", "", "Book title is required."),
        ("category", "", "Book category is required."),
    ],
)
def test_book_rejects_missing_required_text_fields(field_name, value, message):
    values = {
        "bookId": "B001",
        "title": "The Great Gatsby",
        "category": "fiction",
        "referenceOnly": False,
        "available": True,
    }
    values[field_name] = value

    with pytest.raises(DomainValidationError, match=message):
        Book(**values)


def test_member_can_be_created_without_suspension_date():
    member = Member(
        memberId="M001",
        firstName="Emily",
        lastName="Johnson",
        email="emily.johnson@example.org",
        memberType="default",
        suspendedUntil=None,
        createdAt=date(2019, 3, 12),
    )

    assert member.memberId == "M001"
    assert member.firstName == "Emily"
    assert member.lastName == "Johnson"
    assert member.email == "emily.johnson@example.org"
    assert member.memberType == "default"
    assert member.suspendedUntil is None
    assert member.createdAt == date(2019, 3, 12)


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("memberId", "", "Member id is required."),
        ("firstName", "", "Member first name is required."),
        ("lastName", "", "Member last name is required."),
        ("email", "", "Member email is required."),
        ("memberType", "", "Member type is required."),
    ],
)
def test_member_rejects_missing_required_fields(field_name, value, message):
    values = {
        "memberId": "M001",
        "firstName": "Emily",
        "lastName": "Johnson",
        "email": "emily.johnson@example.org",
        "memberType": "default",
        "suspendedUntil": None,
        "createdAt": date(2019, 3, 12),
    }
    values[field_name] = value

    with pytest.raises(DomainValidationError, match=message):
        Member(**values)


def test_librarian_can_be_created_with_required_values():
    librarian = Librarian(
        librarianId="LIB001",
        firstName="Richard",
        lastName="Miller",
        email="richard.miller@example.org",
    )

    assert librarian.librarianId == "LIB001"
    assert librarian.firstName == "Richard"
    assert librarian.lastName == "Miller"
    assert librarian.email == "richard.miller@example.org"


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("librarianId", "", "Librarian id is required."),
        ("firstName", "", "Librarian first name is required."),
        ("lastName", "", "Librarian last name is required."),
        ("email", "", "Librarian email is required."),
    ],
)
def test_librarian_rejects_missing_required_fields(field_name, value, message):
    values = {
        "librarianId": "LIB001",
        "firstName": "Richard",
        "lastName": "Miller",
        "email": "richard.miller@example.org",
    }
    values[field_name] = value

    with pytest.raises(DomainValidationError, match=message):
        Librarian(**values)


def test_loan_without_return_date_is_active():
    loan = Loan(
        loanId="L001",
        bookId="B006",
        memberId="M001",
        loanDate=date(2026, 1, 2),
        dueDate=date(2026, 1, 23),
        returnDate=None,
    )

    assert loan.loanId == "L001"
    assert loan.bookId == "B006"
    assert loan.memberId == "M001"
    assert loan.status == "active"


def test_loan_with_return_date_is_returned():
    loan = Loan(
        loanId="L005",
        bookId="B010",
        memberId="M007",
        loanDate=date(2025, 12, 1),
        dueDate=date(2025, 12, 22),
        returnDate=date(2025, 12, 20),
    )

    assert loan.status == "returned"


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("loanId", "", "Loan id is required."),
        ("bookId", "", "Book id is required."),
        ("memberId", "", "Member id is required."),
    ],
)
def test_loan_rejects_missing_required_ids(field_name, value, message):
    values = {
        "loanId": "L001",
        "bookId": "B006",
        "memberId": "M001",
        "loanDate": date(2026, 1, 2),
        "dueDate": date(2026, 1, 23),
        "returnDate": None,
    }
    values[field_name] = value

    with pytest.raises(DomainValidationError, match=message):
        Loan(**values)


@pytest.mark.parametrize("raw_value", ["default", "Default", " DEFAULT "])
def test_member_type_accepts_supported_values_case_insensitively(raw_value):
    assert MemberType.from_text(raw_value).value == "default"


@pytest.mark.parametrize("raw_value", ["adult", "Adult", " ADULT "])
def test_member_type_accepts_adult_as_legacy_default_value(raw_value):
    assert MemberType.from_text(raw_value).value == "default"


def test_member_type_rejects_unsupported_values():
    with pytest.raises(DomainValidationError, match="Unsupported member type."):
        MemberType.from_text("guest")


@pytest.mark.parametrize("raw_value", ["active", "Active", " ACTIVE "])
def test_loan_status_accepts_supported_values_case_insensitively(raw_value):
    assert LoanStatus.from_text(raw_value).value == "active"


def test_loan_status_rejects_unsupported_values():
    with pytest.raises(DomainValidationError, match="Unsupported loan status."):
        LoanStatus.from_text("lost")


@pytest.mark.parametrize(
    "raw_value",
    ["fiction", "Education", " REFERENCE ", "technology", "arts", "non-fiction", "children", "history"],
)
def test_book_category_accepts_current_raw_data_values(raw_value):
    assert BookCategory.from_text(raw_value).value == raw_value.strip().lower()


def test_book_category_rejects_unsupported_values():
    with pytest.raises(DomainValidationError, match="Unsupported book category."):
        BookCategory.from_text("magazine")

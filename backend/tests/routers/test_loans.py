from fastapi.testclient import TestClient

from app.main import app
from app.routers.loans import get_loan_service
from app.services.errors import (
    BookAlreadyOnLoanError,
    BookNotFoundError,
    InvalidReturnDateError,
    LoanAlreadyReturnedError,
    LoanListUnavailableError,
    LoanNotAllowedError,
    LoanNotFoundError,
)


class FailingLoanService:
    def list_loans(self):
        raise LoanListUnavailableError()


class CreatingLoanService:
    def create_loan(self, *, member_id, book_id, loan_date):
        from app.domain import Loan

        return Loan(
            loanId="L013",
            bookId=book_id,
            memberId=member_id,
            loanDate=loan_date,
            dueDate=loan_date.replace(day=22),
            returnDate=None,
            initialLoanPrice=21.0,
        )


class MissingBookLoanService:
    def create_loan(self, *, member_id, book_id, loan_date):
        raise BookNotFoundError(book_id)


class AlreadyOnLoanService:
    def create_loan(self, *, member_id, book_id, loan_date):
        raise BookAlreadyOnLoanError()


class LoanNotAllowedService:
    def create_loan(self, *, member_id, book_id, loan_date):
        raise LoanNotAllowedError()


class ReturningLoanService:
    def return_loan(self, *, loan_id, return_date):
        from app.domain import Loan
        from datetime import date

        return Loan(
            loanId=loan_id,
            bookId="B002",
            memberId="M001",
            loanDate=date(2026, 2, 1),
            dueDate=date(2026, 2, 22),
            returnDate=return_date,
        )


class MissingReturnLoanService:
    def return_loan(self, *, loan_id, return_date):
        raise LoanNotFoundError(loan_id)


class AlreadyReturnedLoanService:
    def return_loan(self, *, loan_id, return_date):
        raise LoanAlreadyReturnedError(loan_id)


class InvalidReturnDateLoanService:
    def return_loan(self, *, loan_id, return_date):
        raise InvalidReturnDateError()


def test_get_loans_endpoint_returns_clear_error_when_loan_list_fails():
    app.dependency_overrides[get_loan_service] = lambda: FailingLoanService()
    client = TestClient(app)

    try:
        response = client.get("/loans")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "code": "LOAN_LIST_UNAVAILABLE",
        "message": "Loan list data could not be loaded.",
    }


def test_create_loan_endpoint_returns_created_loan():
    app.dependency_overrides[get_loan_service] = lambda: CreatingLoanService()
    client = TestClient(app)

    try:
        response = client.post(
            "/loans",
            json={
                "memberId": "M001",
                "bookId": "B002",
                "loanDate": "2026-02-01",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["loanId"] == "L013"
    assert response.json()["dueDate"] == "2026-02-22"
    assert response.json()["initialLoanPrice"] == 21.0
    assert response.json()["totalDue"] == 21.0
    assert response.json()["status"] == "active"


def test_create_loan_endpoint_accepts_api_prefix():
    app.dependency_overrides[get_loan_service] = lambda: CreatingLoanService()
    client = TestClient(app)

    try:
        response = client.post(
            "/api/loans",
            json={
                "memberId": "M001",
                "bookId": "B002",
                "loanDate": "2026-02-01",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["loanId"] == "L013"


def test_create_loan_endpoint_accepts_trailing_slash():
    app.dependency_overrides[get_loan_service] = lambda: CreatingLoanService()
    client = TestClient(app)

    try:
        response = client.post(
            "/loans/",
            json={
                "memberId": "M001",
                "bookId": "B002",
                "loanDate": "2026-02-01",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["loanId"] == "L013"


def test_create_loan_endpoint_returns_not_found_error():
    app.dependency_overrides[get_loan_service] = lambda: MissingBookLoanService()
    client = TestClient(app)

    try:
        response = client.post(
            "/loans",
            json={
                "memberId": "M001",
                "bookId": "B999",
                "loanDate": "2026-02-01",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "code": "BOOK_NOT_FOUND",
        "message": "Book B999 was not found.",
    }


def test_create_loan_endpoint_returns_blocked_business_error():
    app.dependency_overrides[get_loan_service] = lambda: AlreadyOnLoanService()
    client = TestClient(app)

    try:
        response = client.post(
            "/loans",
            json={
                "memberId": "M001",
                "bookId": "B002",
                "loanDate": "2026-02-01",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["code"] == "BOOK_ALREADY_ON_LOAN"


def test_create_loan_endpoint_returns_generic_not_allowed_error():
    app.dependency_overrides[get_loan_service] = lambda: LoanNotAllowedService()
    client = TestClient(app)

    try:
        response = client.post(
            "/loans",
            json={
                "memberId": "M001",
                "bookId": "B002",
                "loanDate": "2026-02-01",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {
        "code": "LOAN_NOT_ALLOWED",
        "message": "The loan could not be created.",
    }


def test_return_loan_endpoint_marks_loan_as_returned():
    app.dependency_overrides[get_loan_service] = lambda: ReturningLoanService()
    client = TestClient(app)

    try:
        response = client.patch(
            "/loans/L001/return",
            json={"returnDate": "2026-02-10"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["loanId"] == "L001"
    assert response.json()["returnDate"] == "2026-02-10"
    assert response.json()["status"] == "returned"


def test_return_loan_endpoint_accepts_api_prefix():
    app.dependency_overrides[get_loan_service] = lambda: ReturningLoanService()
    client = TestClient(app)

    try:
        response = client.patch(
            "/api/loans/L001/return",
            json={"returnDate": "2026-02-10"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["status"] == "returned"


def test_return_loan_endpoint_returns_not_found_error():
    app.dependency_overrides[get_loan_service] = lambda: MissingReturnLoanService()
    client = TestClient(app)

    try:
        response = client.patch(
            "/loans/L999/return",
            json={"returnDate": "2026-02-10"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["code"] == "LOAN_NOT_FOUND"


def test_return_loan_endpoint_returns_already_returned_error():
    app.dependency_overrides[get_loan_service] = lambda: AlreadyReturnedLoanService()
    client = TestClient(app)

    try:
        response = client.patch(
            "/loans/L001/return",
            json={"returnDate": "2026-02-10"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["code"] == "LOAN_ALREADY_RETURNED"


def test_return_loan_endpoint_returns_invalid_return_date_error():
    app.dependency_overrides[get_loan_service] = lambda: InvalidReturnDateLoanService()
    client = TestClient(app)

    try:
        response = client.patch(
            "/loans/L001/return",
            json={"returnDate": "2026-01-01"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["code"] == "INVALID_RETURN_DATE"

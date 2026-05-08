from datetime import date

from fastapi.testclient import TestClient

from app.domain import Book, Member
from app.main import app
from app.repositories.book_repository import InMemoryBookRepository
from app.repositories.loan_repository import InMemoryLoanRepository
from app.repositories.member_repository import InMemoryMemberRepository
from app.routers.loans import get_loan_service
from app.routers.members import get_member_service
from app.services.loan_service import LoanService
from app.services.member_service import MemberService


def test_created_loan_is_returned_in_loan_list_and_member_overview():
    loan_repository = InMemoryLoanRepository([])
    book_repository = InMemoryBookRepository(
        [
            Book(
                bookId="B002",
                title="Introduction to Data Science",
                category="education",
                referenceOnly=False,
                available=True,
            )
        ]
    )
    member_repository = InMemoryMemberRepository(
        [
            Member(
                memberId="M001",
                firstName="Emily",
                lastName="Johnson",
                email="emily.johnson@example.org",
                memberType="default",
                suspendedUntil=None,
                createdAt=date(2019, 3, 12),
            ),
            Member(
                memberId="M002",
                firstName="Daniel",
                lastName="Smith",
                email="daniel.smith@example.org",
                memberType="student",
                suspendedUntil=None,
                createdAt=date(2023, 9, 1),
            ),
        ]
    )

    app.dependency_overrides[get_loan_service] = lambda: LoanService(
        loan_repository,
        book_repository,
        member_repository,
    )
    app.dependency_overrides[get_member_service] = lambda: MemberService(
        member_repository,
        loan_repository,
    )
    client = TestClient(app)

    try:
        create_response = client.post(
            "/loans",
            json={
                "memberId": "M001",
                "bookId": "B002",
                "loanDate": "2026-02-01",
            },
        )
        loans_response = client.get("/loans")
        member_response = client.get("/members/M001/overview")
        other_member_response = client.get("/members/M002/overview")
    finally:
        app.dependency_overrides.clear()

    assert create_response.status_code == 201
    assert create_response.json()["loanId"] == "L001"
    assert create_response.json()["dueDate"] == "2026-02-22"
    assert create_response.json()["initialLoanPrice"] == 21.0
    assert loans_response.json()[0]["loanId"] == "L001"
    assert member_response.json()["loans"][0]["loanId"] == "L001"
    assert other_member_response.json()["loans"] == []

from fastapi.testclient import TestClient

from app.main import app


def test_get_loans_endpoint_returns_all_in_memory_loans():
    client = TestClient(app)

    response = client.get("/loans")

    assert response.status_code == 200
    loans = response.json()
    assert len(loans) == 12
    assert loans[0] == {
        "loanId": "L001",
        "bookId": "B006",
        "memberId": "M001",
        "loanDate": "2026-01-02",
        "dueDate": "2026-01-23",
        "returnDate": None,
        "status": "active",
        "initialLoanPrice": 21.0,
        "overdueDailyPrice": 0.0,
        "overdueFine": 0.0,
        "totalDue": 21.0,
        "currency": "EUR",
    }


def test_get_loans_endpoint_includes_returned_loan_status():
    client = TestClient(app)

    response = client.get("/loans")

    loans = response.json()
    returned_loan = next(loan for loan in loans if loan["loanId"] == "L005")
    assert returned_loan["returnDate"] == "2025-12-20"
    assert returned_loan["status"] == "returned"

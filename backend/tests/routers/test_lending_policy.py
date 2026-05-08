from fastapi.testclient import TestClient

from app.main import app


def test_lending_policy_endpoint_returns_policy_defaults():
    client = TestClient(app)

    response = client.get("/lending-policy")

    assert response.status_code == 200
    assert response.json() == {
        "supportedMemberStatuses": ["default", "student", "senior"],
        "defaultLoanDays": 21,
        "studentLoanDays": 14,
        "seniorLoanDays": 28,
        "studentInitialLoanPrice": 0.0,
        "dailyLoanPrice": 1.0,
        "studentOverdueDailyPrice": 1.0,
        "dailyOverdueFine": 0.25,
        "maxOverdueFine": 10.0,
        "maxActiveLoans": 5,
        "currency": "EUR",
    }


def test_lending_policy_endpoint_accepts_api_prefix():
    client = TestClient(app)

    response = client.get("/api/lending-policy")

    assert response.status_code == 200
    assert response.json()["supportedMemberStatuses"] == ["default", "student", "senior"]

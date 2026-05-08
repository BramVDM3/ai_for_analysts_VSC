from fastapi.testclient import TestClient

from app.main import app


def test_get_member_overview_returns_member_details_and_related_loans():
    client = TestClient(app)

    response = client.get("/members/M002/overview")

    assert response.status_code == 200
    overview = response.json()
    assert overview["member"]["memberId"] == "M002"
    assert overview["member"]["firstName"] == "Daniel"
    assert {loan["memberId"] for loan in overview["loans"]} == {"M002"}
    assert {loan["status"] for loan in overview["loans"]} == {"active", "returned"}


def test_get_member_overview_returns_empty_loans_for_member_without_loans():
    client = TestClient(app)

    response = client.get("/members/M009/overview")

    assert response.status_code == 200
    overview = response.json()
    assert overview["member"]["memberId"] == "M009"
    assert overview["loans"] == []


def test_get_member_overview_returns_member_not_found():
    client = TestClient(app)

    response = client.get("/members/M999/overview")

    assert response.status_code == 404
    assert response.json() == {
        "code": "MEMBER_NOT_FOUND",
        "message": "Member M999 was not found.",
    }

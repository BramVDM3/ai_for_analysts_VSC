from fastapi.testclient import TestClient

from app.main import app


def test_get_members_endpoint_returns_all_in_memory_members():
    client = TestClient(app)

    response = client.get("/members")

    assert response.status_code == 200
    members = response.json()
    assert len(members) == 15
    assert members[0] == {
        "memberId": "M001",
        "firstName": "Emily",
        "lastName": "Johnson",
        "email": "emily.johnson@example.org",
        "memberType": "default",
        "suspendedUntil": None,
        "createdAt": "2019-03-12",
    }


def test_get_members_endpoint_includes_suspended_member_status():
    client = TestClient(app)

    response = client.get("/members")

    members = response.json()
    michael = next(member for member in members if member["memberId"] == "M003")
    assert michael["suspendedUntil"] == "2026-02-15"

from fastapi.testclient import TestClient

from app.main import app
from app.routers.members import get_member_service
from app.services.errors import MemberListUnavailableError


class FailingMemberService:
    def list_members(self):
        raise MemberListUnavailableError()


class UnknownMemberOverviewService:
    def get_member_overview(self, member_id):
        from app.services.errors import MemberNotFoundError

        raise MemberNotFoundError(member_id)


class FailingMemberOverviewService:
    def get_member_overview(self, member_id):
        from app.services.errors import MemberOverviewUnavailableError

        raise MemberOverviewUnavailableError()


class UnexpectedFailingMemberOverviewService:
    def get_member_overview(self, member_id):
        raise RuntimeError("database password is secret")


def test_get_members_endpoint_returns_clear_error_when_member_list_fails():
    app.dependency_overrides[get_member_service] = lambda: FailingMemberService()
    client = TestClient(app)

    try:
        response = client.get("/members")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "code": "MEMBER_LIST_UNAVAILABLE",
        "message": "Member list data could not be loaded.",
    }


def test_get_member_overview_returns_clear_not_found_error():
    app.dependency_overrides[get_member_service] = lambda: UnknownMemberOverviewService()
    client = TestClient(app)

    try:
        response = client.get("/members/M999/overview")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "code": "MEMBER_NOT_FOUND",
        "message": "Member M999 was not found.",
    }


def test_get_member_overview_returns_clear_loading_error():
    app.dependency_overrides[get_member_service] = lambda: FailingMemberOverviewService()
    client = TestClient(app)

    try:
        response = client.get("/members/M001/overview")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "code": "MEMBER_OVERVIEW_UNAVAILABLE",
        "message": "Member overview could not be loaded.",
    }


def test_get_member_overview_hides_unexpected_internal_errors():
    app.dependency_overrides[get_member_service] = lambda: UnexpectedFailingMemberOverviewService()
    client = TestClient(app)

    try:
        response = client.get("/members/M001/overview")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "code": "MEMBER_OVERVIEW_UNAVAILABLE",
        "message": "Member overview could not be loaded.",
    }

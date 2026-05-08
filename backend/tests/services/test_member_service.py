from datetime import date

from app.domain import Member
from app.repositories.errors import DataSourceError
from app.services.errors import MemberListUnavailableError
from app.services.member_service import MemberService


class SuccessfulMemberRepository:
    def list_members(self):
        return [
            Member(
                memberId="M001",
                firstName="Emily",
                lastName="Johnson",
                email="emily.johnson@example.org",
                memberType="default",
                suspendedUntil=None,
                createdAt=date(2019, 3, 12),
            )
        ]


class FailingMemberRepository:
    def list_members(self):
        raise DataSourceError("Member list data could not be loaded.")


def test_member_service_returns_members_from_repository():
    members = MemberService(SuccessfulMemberRepository()).list_members()

    assert len(members) == 1
    assert members[0].memberId == "M001"


def test_member_service_converts_data_errors_to_member_list_error():
    service = MemberService(FailingMemberRepository())

    try:
        service.list_members()
    except MemberListUnavailableError as error:
        assert error.code == "MEMBER_LIST_UNAVAILABLE"
        assert str(error) == "Member list data could not be loaded."
    else:
        raise AssertionError("Expected MemberListUnavailableError")

from datetime import date

from app.domain import Member
from app.repositories.in_memory_data import MEMBERS
from app.repositories.member_repository import InMemoryMemberRepository


def test_in_memory_member_repository_returns_seeded_members():
    members = InMemoryMemberRepository().list_members()

    assert len(members) == 15
    assert members[0].memberId == "M001"
    assert members[0].firstName == "Emily"
    assert members[0].lastName == "Johnson"
    assert members[0].email == "emily.johnson@example.org"
    assert members[0].memberType == "default"
    assert members[0].suspendedUntil is None
    assert members[0].createdAt == date(2019, 3, 12)


def test_in_memory_member_repository_includes_suspended_members():
    members = InMemoryMemberRepository().list_members()

    michael = next(member for member in members if member.memberId == "M003")

    assert michael.suspendedUntil == date(2026, 2, 15)


def test_in_memory_member_repository_accepts_injected_members():
    expected_members = [
        Member(
            memberId="M999",
            firstName="Test",
            lastName="Member",
            email="test.member@example.org",
            memberType="default",
            suspendedUntil=None,
            createdAt=date(2026, 1, 1),
        )
    ]

    members = InMemoryMemberRepository(expected_members).list_members()

    assert members == expected_members


def test_in_memory_member_repository_accepts_an_empty_injected_member_list():
    assert InMemoryMemberRepository([]).list_members() == []


def test_in_memory_member_repository_returns_a_copy_of_the_member_list():
    members = InMemoryMemberRepository().list_members()

    members.clear()

    assert len(MEMBERS) == 15
    assert len(InMemoryMemberRepository().list_members()) == 15

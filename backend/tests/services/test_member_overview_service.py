from datetime import date

from app.domain import Loan, Member
from app.repositories.errors import DataSourceError
from app.services.errors import MemberNotFoundError, MemberOverviewUnavailableError
from app.services.member_service import MemberService


class MemberRepository:
    def __init__(self, members):
        self.members = members

    def list_members(self):
        return self.members


class LoanRepository:
    def __init__(self, loans):
        self.loans = loans

    def list_loans(self):
        return self.loans


class FailingLoanRepository:
    def list_loans(self):
        raise DataSourceError("Loan data failed.")


def make_member(member_id="M001"):
    return Member(
        memberId=member_id,
        firstName="Emily",
        lastName="Johnson",
        email="emily.johnson@example.org",
        memberType="default",
        suspendedUntil=None,
        createdAt=date(2019, 3, 12),
    )


def make_loan(loan_id, member_id, return_date=None):
    return Loan(
        loanId=loan_id,
        bookId="B001",
        memberId=member_id,
        loanDate=date(2026, 1, 1),
        dueDate=date(2026, 1, 22),
        returnDate=return_date,
    )


def test_member_overview_returns_member_and_only_that_members_loans():
    service = MemberService(
        MemberRepository([make_member("M001"), make_member("M002")]),
        LoanRepository(
            [
                make_loan("L001", "M001"),
                make_loan("L002", "M002"),
                make_loan("L003", "M001", date(2026, 1, 10)),
            ]
        ),
    )

    overview = service.get_member_overview("M001")

    assert overview["member"].memberId == "M001"
    assert [loan.loanId for loan in overview["loans"]] == ["L001", "L003"]
    assert [loan.status for loan in overview["loans"]] == ["active", "returned"]


def test_member_overview_returns_empty_loan_list_when_member_has_no_loans():
    service = MemberService(MemberRepository([make_member("M009")]), LoanRepository([]))

    overview = service.get_member_overview("M009")

    assert overview["member"].memberId == "M009"
    assert overview["loans"] == []


def test_member_overview_raises_not_found_for_unknown_member():
    service = MemberService(MemberRepository([make_member("M001")]), LoanRepository([]))

    try:
        service.get_member_overview("M999")
    except MemberNotFoundError as error:
        assert error.code == "MEMBER_NOT_FOUND"
        assert str(error) == "Member M999 was not found."
    else:
        raise AssertionError("Expected MemberNotFoundError")


def test_member_overview_converts_loan_loading_failure():
    service = MemberService(MemberRepository([make_member("M001")]), FailingLoanRepository())

    try:
        service.get_member_overview("M001")
    except MemberOverviewUnavailableError as error:
        assert error.code == "MEMBER_OVERVIEW_UNAVAILABLE"
        assert str(error) == "Member overview could not be loaded."
    else:
        raise AssertionError("Expected MemberOverviewUnavailableError")

from app.domain import Member
from app.repositories.errors import DataSourceError
from app.repositories.loan_repository import InMemoryLoanRepository
from app.repositories.member_repository import InMemoryMemberRepository
from app.services.errors import (
    MemberListUnavailableError,
    MemberNotFoundError,
    MemberOverviewUnavailableError,
)


class MemberService:
    def __init__(
        self,
        member_repository: InMemoryMemberRepository,
        loan_repository: InMemoryLoanRepository | None = None,
    ) -> None:
        # The repository is injected so service tests can use a fake data source.
        self.member_repository = member_repository
        self.loan_repository = loan_repository

    def list_members(self) -> list[Member]:
        # Ask the data layer for members and translate data failures into a user-facing error.
        try:
            return self.member_repository.list_members()
        except DataSourceError as error:
            raise MemberListUnavailableError() from error

    def get_member_overview(self, member_id: str) -> dict[str, object]:
        try:
            members = self.member_repository.list_members()
            loans = self._list_loans_for_overview()
        except DataSourceError as error:
            raise MemberOverviewUnavailableError() from error

        member = next((item for item in members if item.memberId == member_id), None)
        if member is None:
            raise MemberNotFoundError(member_id)

        member_loans = [loan for loan in loans if loan.memberId == member_id]
        return {"member": member, "loans": member_loans}

    def _list_loans_for_overview(self):
        if self.loan_repository is None:
            raise DataSourceError("Member overview data could not be loaded.")
        return self.loan_repository.list_loans()

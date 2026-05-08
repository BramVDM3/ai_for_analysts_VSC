from app.domain import Member
from app.repositories.in_memory_data import MEMBERS


class InMemoryMemberRepository:
    def __init__(self, members: list[Member] | None = None) -> None:
        # Allow tests to inject a small member list while production uses the seeded data.
        self.members = MEMBERS if members is None else members

    def list_members(self) -> list[Member]:
        # Return a copy so callers cannot accidentally change the repository seed data.
        return list(self.members)

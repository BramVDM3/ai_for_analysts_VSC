from app.domain import LendingPolicy


class LendingPolicyService:
    def get_policy(self) -> LendingPolicy:
        return LendingPolicy()

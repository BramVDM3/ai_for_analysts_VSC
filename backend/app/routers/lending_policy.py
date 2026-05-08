from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.schemas.lending_policy import LendingPolicyResponse
from app.services.errors import LendingPolicyUnavailableError
from app.services.lending_policy_service import LendingPolicyService

router = APIRouter(prefix="/lending-policy", tags=["lending-policy"])


def get_lending_policy_service() -> LendingPolicyService:
    return LendingPolicyService()


@router.get("", response_model=LendingPolicyResponse)
@router.get("/", response_model=LendingPolicyResponse, include_in_schema=False)
def get_lending_policy(
    lending_policy_service: LendingPolicyService = Depends(get_lending_policy_service),
):
    try:
        policy = lending_policy_service.get_policy()
        return {
            **policy.__dict__,
            "supportedMemberStatuses": list(policy.supportedMemberStatuses),
        }
    except LendingPolicyUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.repositories.loan_repository import InMemoryLoanRepository
from app.repositories.member_repository import InMemoryMemberRepository
from app.schemas.member import MemberOverviewResponse, MemberResponse
from app.services.errors import (
    MemberListUnavailableError,
    MemberNotFoundError,
    MemberOverviewUnavailableError,
)
from app.services.member_service import MemberService

router = APIRouter(prefix="/members", tags=["members"])


def get_member_service() -> MemberService:
    # Build the service dependency used by the members endpoint.
    return MemberService(InMemoryMemberRepository(), InMemoryLoanRepository())


@router.get("", response_model=list[MemberResponse])
def list_members(member_service: MemberService = Depends(get_member_service)):
    # Return member list data to the frontend, or a stable error response when retrieval fails.
    try:
        return member_service.list_members()
    except MemberListUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )


@router.get("/{member_id}/overview", response_model=MemberOverviewResponse)
def get_member_overview(
    member_id: str,
    member_service: MemberService = Depends(get_member_service),
):
    # Return one member with related loans, keeping not-found and loading failures distinct.
    try:
        return member_service.get_member_overview(member_id)
    except MemberNotFoundError as error:
        return JSONResponse(
            status_code=404,
            content={"code": error.code, "message": str(error)},
        )
    except MemberOverviewUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "code": MemberOverviewUnavailableError.code,
                "message": "Member overview could not be loaded.",
            },
        )

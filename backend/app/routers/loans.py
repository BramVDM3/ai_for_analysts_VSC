from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.repositories.book_repository import InMemoryBookRepository
from app.repositories.loan_repository import InMemoryLoanRepository
from app.repositories.member_repository import InMemoryMemberRepository
from app.schemas.loan import CreateLoanRequest, LoanResponse, ReturnLoanRequest
from app.services.errors import (
    BookAlreadyOnLoanError,
    BookNotFoundError,
    BookUnavailableError,
    InvalidReturnDateError,
    InvalidLoanDatesError,
    InvalidMemberStatusError,
    LoanAlreadyReturnedError,
    LoanCreationUnavailableError,
    LoanListUnavailableError,
    LoanNotAllowedError,
    LoanNotFoundError,
    LoanReturnUnavailableError,
    MemberNotFoundError,
    ReferenceOnlyLoanError,
)
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["loans"])


def get_loan_service() -> LoanService:
    # Build the service dependency used by the loans endpoint.
    return LoanService(
        InMemoryLoanRepository(),
        InMemoryBookRepository(),
        InMemoryMemberRepository(),
    )


@router.get("", response_model=list[LoanResponse])
@router.get("/", response_model=list[LoanResponse], include_in_schema=False)
def list_loans(loan_service: LoanService = Depends(get_loan_service)):
    # Return loan list data to the frontend, or a stable error response when retrieval fails.
    try:
        return loan_service.list_loans()
    except LoanListUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )


@router.post("", response_model=LoanResponse, status_code=201)
@router.post("/", response_model=LoanResponse, status_code=201, include_in_schema=False)
def create_loan(
    request: CreateLoanRequest,
    loan_service: LoanService = Depends(get_loan_service),
):
    try:
        return loan_service.create_loan(
            member_id=request.memberId,
            book_id=request.bookId,
            loan_date=request.loanDate,
        )
    except (MemberNotFoundError, BookNotFoundError) as error:
        return JSONResponse(
            status_code=404,
            content={"code": error.code, "message": str(error)},
        )
    except (
        ReferenceOnlyLoanError,
        BookAlreadyOnLoanError,
        BookUnavailableError,
        InvalidLoanDatesError,
        InvalidMemberStatusError,
        LoanNotAllowedError,
    ) as error:
        return JSONResponse(
            status_code=400,
            content={"code": error.code, "message": str(error)},
        )
    except LoanCreationUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )


@router.patch("/{loan_id}/return", response_model=LoanResponse)
def return_loan(
    loan_id: str,
    request: ReturnLoanRequest,
    loan_service: LoanService = Depends(get_loan_service),
):
    try:
        return loan_service.return_loan(
            loan_id=loan_id,
            return_date=request.returnDate,
        )
    except LoanNotFoundError as error:
        return JSONResponse(
            status_code=404,
            content={"code": error.code, "message": str(error)},
        )
    except (LoanAlreadyReturnedError, InvalidReturnDateError) as error:
        return JSONResponse(
            status_code=400,
            content={"code": error.code, "message": str(error)},
        )
    except LoanReturnUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )

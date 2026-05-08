from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.repositories.book_repository import InMemoryBookRepository
from app.repositories.loan_repository import InMemoryLoanRepository
from app.schemas.book import BookResponse
from app.services.book_service import BookService
from app.services.errors import BookCatalogueUnavailableError

router = APIRouter(prefix="/books", tags=["books"])


def get_book_service() -> BookService:
    # Build the service dependency used by the books endpoint.
    return BookService(InMemoryBookRepository(), InMemoryLoanRepository())


@router.get("", response_model=list[BookResponse])
def list_books(book_service: BookService = Depends(get_book_service)):
    # Return catalogue data to the frontend, or a stable error response when loading fails.
    try:
        return [BookResponse.from_attributes(book) for book in book_service.list_books()]
    except BookCatalogueUnavailableError as error:
        return JSONResponse(
            status_code=500,
            content={"code": error.code, "message": str(error)},
        )

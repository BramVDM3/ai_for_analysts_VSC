from fastapi import APIRouter

from app.routers.books import router as books_router
from app.routers.lending_policy import router as lending_policy_router
from app.routers.loans import router as loans_router
from app.routers.members import router as members_router

router = APIRouter()


@router.get("/health")
def health_check():
    # Lightweight health endpoint for smoke tests and local checks.
    return {"status": "ok"}


router.include_router(books_router)
router.include_router(members_router)
router.include_router(loans_router)
router.include_router(lending_policy_router)

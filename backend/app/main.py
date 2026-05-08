from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

from app.routers import router  # noqa: E402

app = FastAPI(title="Library AI for Analysts")
app.include_router(router)
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    # Simple root endpoint used to confirm that the backend is running.
    return {"message": "Library AI for Analysts backend is running."}

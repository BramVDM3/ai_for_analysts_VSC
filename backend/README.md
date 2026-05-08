# Backend Service

This backend is a minimal Python FastAPI scaffold intended for analyst education and prototype development.

## Setup

1. Create a Python virtual environment.
2. Activate it.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy config values:
   ```bash
   copy ..\.env.example .env
   ```

## Run

```bash
uvicorn app.main:app --port 8000 --app-dir .
```

## Test

From the `backend` folder, run:

```powershell
..\.venv\Scripts\python.exe -m pytest tests -p no:cacheprovider
```

The `-p no:cacheprovider` option disables pytest cache writing. This avoids temporary pytest cache folders when the project is stored in OneDrive.

### Test structure

The test folder mirrors the backend application layers:

- `tests/domain/` - domain object and value object tests
- `tests/repositories/` - data layer tests
- `tests/services/` - service layer unit tests
- `tests/routers/` - API route tests with mocked dependencies
- `tests/integration/` - end-to-end backend tests through the real FastAPI app wiring

## Available endpoints

- `GET /` - health/root.
- `GET /health` - service health check.

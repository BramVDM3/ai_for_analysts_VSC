# Frontend for AI for Analysts

This is a minimal Vite + React frontend for educational use. It provides a simple UI to call the FastAPI backend and demonstrate how the frontend and backend work together.

## Setup

From the `frontend/` folder:

```bash
cp .env.example .env
npm install
npm run dev
```

## Development

- `npm run dev` starts the frontend locally with hot reload.
- `npm run build` creates a production bundle in `dist/`.
- `npm run preview` serves the built output for a preview.

## How it connects to the backend

The frontend uses the Vite dev server proxy to forward requests starting with `/api` to `VITE_BACKEND_URL`.

- In `src/App.jsx`, the app calls `/api/health`.
- Vite sends that request to the backend configured in `.env`.
- The default template points to `http://127.0.0.1:8000`.

This avoids browser CORS issues during development.

# Architecture

## Top-Level Layout

The repository separates the FastAPI service in `backend/` from the Vite React client in `frontend/`. This keeps runtime dependencies, build tooling, and deployment concerns independent while allowing both applications to evolve together.

## Backend

`backend/app/` owns HTTP entry points and currently exposes `GET /health` for local and deployment checks. The remaining backend packages make integration boundaries explicit: `ai/` for model providers, `database/` for persistence, `workflow/` for orchestration, and `mock_services/` for local substitutes. This avoids mixing vendor, data, and request-handling code as features are added.

## Frontend

The client uses React with Vite for a small, fast browser build and Tailwind CSS for utility-first styling without a separate component-library dependency. `src/pages/` contains route-level screens, `src/components/` reusable UI, and `src/lib/` browser-facing helpers such as API calls.

## Supporting Directories

`data/` is reserved for project data, `scripts/` for repeatable maintenance tasks, and `docs/` for durable project decisions. Configuration is intentionally minimal: API and client values should be supplied through environment variables (for example, `VITE_API_URL`) rather than committed secrets.

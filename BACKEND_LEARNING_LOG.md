# Backend Learning Log

## Phase 0: Repository Audit & Backend Learning Setup (2026-11-05)

### 1. Environment Audit Results
- **Operating System:** Windows 11.
- **Python Runtime:** Python 3.13.12 verified via `python --version`.
- **Package Manager:** `uv` 0.10.8 verified via `uv --version`.
- **Repository Structure:** Monorepo approach. Frontend lives at repository root (`/src`, Next.js 16); backend lives in `/MockPrep_BE`.
- **Git & Ignores:** Configured dedicated `MockPrep_BE/.gitignore` and updated root `.gitignore` to ignore `.venv/`, `__pycache__/`, `.pytest_cache/`, and `.ruff_cache/`.

### 2. Core Concepts Taught & Understood
- **Python's Role in the Backend:** Serves as the computational, authoritative engine for data persistence, cryptographic token verification, AI orchestration, and code evaluation.
- **What FastAPI is:** A high-performance Python web framework designed around standard Python type hints, automatic Pydantic request/response validation, and auto-generated interactive OpenAPI documentation (Swagger UI).
- **Backend Server vs. Frontend:** The Next.js frontend runs in user browsers and edge rendering nodes, handling UI state and presentation. The FastAPI backend is the trusted server that securely connects to the database, checks Clerk JWT signatures, guards secrets, and controls assessment state machines.
- **HTTP Request & Response Flow:** Clients issue requests with an HTTP verb (`GET`, `POST`, `PUT`, `DELETE`), headers (e.g. `Authorization: Bearer <token>`), and optional JSON bodies. The backend processes the request, validates data, queries the database, and returns a status code (e.g. `200 OK`, `201 Created`, `401 Unauthorized`, `422 Unprocessable Entity`) with serialized JSON.
- **API Endpoint:** A designated route path (such as `/api/v1/health` or `/api/v1/projects`) paired with an HTTP method and handler function.
- **Why Separate FastAPI from Next.js API Routes:**
  1. Python is the primary ecosystem for AI/LLM libraries, code evaluation, sandboxing, and data science tooling.
  2. Clear decoupling of UI rendering concerns from authoritative assessment logic, database transactions, and long-running execution jobs.
  3. Independent scaling, testing, and lifecycle management for frontend and backend.

### 3. Decisions & Next Steps
- Created tracking files: `BACKEND_CONTEXT.md`, `BACKEND_LEARNING_LOG.md`, `BACKEND_DECISIONS.md`.
- Next: Phase 3 FastAPI AI Service initialization.

---

## Phase 3: FastAPI AI Service Initialization & Health Endpoint (2026-11-05)

### 1. Concepts Mastered
- **Python Modules and Packages:**
  - Any folder containing an `__init__.py` file is treated by Python as a **package**.
  - A `.py` file is a **module**.
  - Import path `app.api.v1.endpoints.health` maps directly to `app/api/v1/endpoints/health.py`.
- **FastAPI Application Instance (`app = FastAPI(...)`):**
  - Creates the ASGI application router.
  - Automatically generates the OpenAPI 3.1 specification exposed at `/openapi.json`.
  - Powers interactive Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Route Decorators (`@router.get` / `@app.get`):**
  - In Python, `@decorator` wraps a function, registering metadata (HTTP method, path, response model, tags, status code) with FastAPI before the function executes.
- **`def` vs `async def`:**
  - `async def` functions run asynchronously on Python's `asyncio` event loop. Essential for non-blocking I/O (network requests, database calls).
  - Regular `def` functions are run by FastAPI in an external thread pool so they do not block the event loop.
- **Type Hints & Pydantic:**
  - Python type hints (`name: str`, `timestamp: datetime`) are used by Pydantic at runtime to validate input data and serialize output data to JSON.
  - `response_model=HealthResponse` guarantees that only declared fields are returned, filtering sensitive fields automatically.
- **Modern Lifespan Context Manager:**
  - Uses `@asynccontextmanager` on an `async def lifespan(app: FastAPI)` function to manage startup and shutdown logic cleanly.

### 2. Implemented & Verified
- `pyproject.toml` initialized with `fastapi[standard]`, `pytest`, `httpx`, and `[tool.fastapi]` entrypoint.
- Virtual environment created and managed by `uv` at `MockPrep_FastAPI/.venv`.
- `app/core/config.py`: Type-safe settings with `pydantic-settings`.
- `app/api/v1/endpoints/health.py`: Documented `GET /health` probe returning typed `HealthResponse`.
- `app/main.py`: ASGI entrypoint with CORS, lifespan, root index, and `/api/v1` router mount.
- `tests/test_health.py`: 5 automated tests via `pytest` (100% pass in 0.11s).
- Live verification: Verified `GET /health`, `GET /api/v1/health`, and `GET /openapi.json` on `http://127.0.0.1:8000`.

---

## Phase 4: API Contracts & Service-to-Service Communication (2026-11-06)

### 1. Concepts Mastered
- **What is an API Contract?**
  - An agreed specification defining how two services communicate: exact paths, HTTP methods, headers, request bodies (DTOs), response shapes, and error structures.
  - Ensures the calling service (Express) and receiving service (FastAPI) stay synchronized without silent runtime failures.
- **Data Transfer Objects (DTOs) with Pydantic v2:**
  - `ChallengeGenerateRequest`: Validates incoming project context (title, stack, summary, difficulty).
  - `ChallengeJobResponse`: Standardized response carrying tracking ID, status, and metadata.
  - Bridging Python `snake_case` and JavaScript `camelCase`: Used Pydantic's `to_camel` alias generator (`model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)`) so Python code uses idiomatic `project_id` while reading and emitting standard JSON `projectId`.
- **Machine-to-Machine (M2M) Service Authentication:**
  - Internal endpoints (`/internal/v1/*`) are NOT intended for public internet or browser access.
  - Protected using a shared secret header `X-Service-Token`.
  - In FastAPI, this is implemented as a reusable dependency: `verify_service_token(x_service_token: Annotated[str | None, Header(alias="X-Service-Token")])`.
  - Missing or mismatched tokens instantly yield `401 Unauthorized`.
- **The `202 Accepted` Asynchronous Job Model:**
  - AI challenge generation (prompting LLMs, analyzing ASTs, synthesizing tests) takes significant time (5-30+ seconds).
  - A synchronous HTTP request would risk socket timeouts and degraded client latency.
  - Instead, FastAPI immediately returns `202 Accepted` with a `jobId` and `status: "queued"`, allowing Express to track or poll progress via `GET /internal/v1/challenges/jobs/{job_id}`.
- **Standardized Error Envelope:**
  - Designed `{ "error": { "code": ..., "message": ..., "details": ... } }` to ensure consistent error handling across the entire multi-service monorepo.

### 2. Implemented & Verified
- `app/api/deps.py`: Dependency `verify_service_token` enforcing machine-to-machine security.
- `app/schemas/challenge.py`: Pydantic models with enums (`DifficultyLevel`, `ChallengeType`, `JobStatus`) and `to_camel` aliasing.
- `app/schemas/error.py`: Structured `ErrorResponse` and `ErrorDetail` schemas.
- `app/api/internal/v1/endpoints/challenges.py`: `POST /generate` (202 Accepted) and `GET /jobs/{job_id}`.
- `app/api/internal/v1/router.py`: Router aggregating internal endpoints under `/internal/v1`.
- `app/main.py`: Mounted `internal_router` at `/internal/v1`.
- `tests/test_challenges.py`: 6 automated tests testing 401 unauthenticated, 422 validation failure, 202 job creation, 200 job retrieval, and 404 not found.
- Verification: 11/11 tests pass in 0.18s (`uv run pytest -v`).

---

## Phase 5: PostgreSQL Foundation & Schema Ownership (2026-11-06)

### 1. Concepts Mastered
- **Database & Schema Architecture (Relational + Microservice Isolation):**
  - PostgreSQL is a relational database management system (RDBMS) storing data in typed tables with columns, rows, and mathematical constraints.
  - A **Schema** is a distinct namespace inside a PostgreSQL database (like a folder for tables).
  - **Schema Ownership Pattern:** Rather than running separate physical database clusters, Express and FastAPI share a single Neon PostgreSQL instance but operate inside separate isolated schemas:
    - Express owns `app` (`app.projects`, etc.).
    - FastAPI owns `ai` (`ai.ai_jobs`, etc.).
  - FastAPI has zero write access to `app.*` tables, and Express has zero write access to `ai.*` tables.
- **SQLAlchemy 2.0 Async Engine & `asyncpg` Driver:**
  - Modern Python async database operations use `asyncpg` via SQLAlchemy's `create_async_engine("postgresql+asyncpg://...")`.
  - Neon PostgreSQL requires SSL encryption. `asyncpg` manages SSL through `connect_args={"ssl": "require"}` rather than URL query parameters (`?sslmode=require`), requiring clean URL normalization in `Settings.async_database_url`.
- **DeclarativeBase with Schema Metadata:**
  - Created `app.db.base.Base` with `MetaData(schema="ai")`.
  - Every model inheriting from `Base` automatically belongs to the `ai` schema, preventing unintentional table creation in `public`.
- **Relational Model (`AIJob`):**
  - `ai.ai_jobs` table stores background AI generation jobs.
  - Columns: `id` (UUIDv4 primary key), `project_id` (string), `status` (string with index), `message`, `estimated_duration_seconds`, `result` (`JSONB` for unstructured model outputs), `error`, `created_at`, `updated_at`.
- **Request-Scoped Session Dependency (`get_db`):**
  - Dependency injection yields an `AsyncSession` per HTTP request.
  - Automatically manages transaction lifecycle: commits on success, issues `session.rollback()` on error, and closes the session upon request completion.
- **Alembic Async Migrations & Schema Isolation Filters:**
  - Alembic manages schema versioning and schema migrations.
  - Neon databases frequently host multiple schemas (e.g. `neon_auth`, existing user tables, and `app`).
  - By default, Alembic autogenerate inspects the entire database and attempts to DROP foreign tables!
  - We secured `migrations/env.py` using `include_object` and `include_name` hooks: Alembic only inspects and manages objects inside the `"ai"` schema.
  - `version_table_schema="ai"` isolates `alembic_version` to `ai.alembic_version`.
- **Windows ProactorEventLoop & Connection Pooling in Tests:**
  - In Windows, Python's ProactorEventLoop can close before background async connection pools drain, causing `RuntimeError: Event loop is closed`.
  - Solved in test fixtures by using SQLAlchemy's `NullPool` to close connections immediately after each test transaction.

### 2. Implemented & Verified
- `app/core/config.py`: Added `DATABASE_URL` and `async_database_url` computed property.
- `app/db/base.py`: SQLAlchemy `DeclarativeBase` with schema `"ai"`.
- `app/db/session.py`: Async engine, `async_session_maker`, and `get_db` dependency.
- `app/db/init_db.py`: Direct script to create `ai` schema and tables.
- `app/models/job.py`: `AIJob` model with `JSONB` output storage and status indexing.
- `migrations/env.py`: Async Alembic configuration with schema isolation filters.
- `migrations/versions/1b927feeecfc_create_ai_jobs_table.py`: Migration creating `ai.ai_jobs`.
- `tests/test_database.py`: Automated async tests for database health and full CRUD cycle on `ai.ai_jobs`.
- Verification: 13/13 tests pass in 0.95s (`uv run pytest -v`).




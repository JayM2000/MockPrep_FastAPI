# Backend Context — FastAPI AI Engine

## 1. Overview & Role in Multi-Service Architecture
- **Directory:** `MockPrep_FastAPI/` (excluded from frontend git tracking in root `.gitignore`).
- **Primary Framework:** FastAPI (Python 3.11/3.13+ via `uv`).
- **Package Manager:** `uv`.
- **Current Phase:** Phase 5 (PostgreSQL Foundation & Schema Ownership) completed. Next up: Phase 6 (First Complete Vertical Slice: Project Creation).
- **Role:** Dedicated **AI & Intelligence Service** in the separated architecture defined in `AI_Project_Platform_Monorepo_Phased_Implementation_Guide.md`.
- **Express vs. FastAPI Division of Responsibilities:**
  - **Node.js Express API (`MockPrep_Express/`):** The primary application backend. Owns users, organizations, project metadata, challenge records, session state machines, authoritative countdown timers, Socket.IO realtime rooms, and PostgreSQL `app` schema.
  - **Python FastAPI Service (`MockPrep_FastAPI/`):** The specialized AI computation backend. Owns LLM provider integrations, prompt templates, code chunking/indexing, vector retrieval (RAG / pgvector), synthetic challenge/bug injection, and AI evaluation signals.
  - **Service-to-Service Communication:** Express calls protected internal FastAPI endpoints mounted under `/internal/v1/*` using a shared `X-Service-Token` header. The browser/frontend NEVER calls FastAPI directly.

## 2. API Contracts & Service Endpoints
- **Public Probes:**
  - `GET /`: Service greeting and documentation index.
  - `GET /health` & `GET /api/v1/health`: Liveness probes.
- **Protected Internal Endpoints (`/internal/v1/*` - Requires `X-Service-Token`):**
  - `POST /internal/v1/challenges/generate`: Accepts project context DTO, queues challenge synthesis job, returns `202 Accepted` with `jobId`.
  - `GET /internal/v1/challenges/jobs/{job_id}`: Returns progress status (`queued` | `processing` | `completed` | `failed`) and result payload.

## 3. Database & Schema Ownership
- **Database Engine:** Neon PostgreSQL 17.11 (serverless cloud PostgreSQL with SSL).
- **Schema Ownership:** `ai` schema exclusively owned and written by FastAPI.
- **Driver & ORM:** SQLAlchemy 2.0 with `asyncpg` async driver.
- **Migration Manager:** Alembic (async env with `version_table_schema="ai"` and strict `include_object` filters).
- **Current Tables in `ai` Schema:**
  - `ai.ai_jobs`: Tracks asynchronous AI challenge synthesis jobs and outputs. Columns: `id` (UUID), `project_id` (str), `status` (str), `message` (str), `estimated_duration_seconds` (int), `result` (JSONB), `error` (str), `created_at` (timestamptz), `updated_at` (timestamptz).
  - `ai.alembic_version`: Tracks Alembic revision hash for `ai` schema.

## 4. Technology Stack
- **Runtime:** Python 3.13.12
- **Package & Environment Manager:** `uv`
- **Web Framework:** FastAPI (with Uvicorn standard server)
- **Data Validation:** Pydantic v2
- **Vector & Relational Storage:** PostgreSQL (`ai` schema / `pgvector`)
- **Testing:** `pytest` + `httpx`
- **Linting & Formatting:** Ruff

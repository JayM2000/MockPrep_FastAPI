# Backend Architecture Decisions

## BEDR-001: Monorepo Organization with `MockPrep_BE` Directory
- **Date:** 2026-11-05
- **Status:** Accepted
- **Context:** The application consists of a Next.js 16 frontend and a Python FastAPI backend. We need a clear repository layout that allows independent package management while keeping all code in one version-controlled workspace.
- **Decision:** Place the backend in a dedicated subfolder `MockPrep_BE/` at repository root. Root contains Next.js frontend code; `MockPrep_BE/` contains Python project files (`pyproject.toml`, virtual environment, backend source code, migrations, tests).
- **Alternatives Considered:**
  - Separate Git repository (adds coordination overhead for PRs, issues, and documentation in early development).
  - Merging backend into Next.js Route Handlers (rejected because Python is essential for the planned AI simulation, code analysis, and sandbox execution pipelines).
- **Consequences:** Easy navigation, single Git history, clean boundary between Node.js and Python ecosystems.

## BEDR-002: Package and Environment Management via `uv`
- **Date:** 2026-11-05
- **Status:** Accepted
- **Context:** Python package management historically involved disparate tools (`pip`, `virtualenv`, `poetry`, `pipenv`), often with slow resolution times and lockfile inconsistencies across platforms.
- **Decision:** Use `uv` (from Astral) as the unified package and virtual environment manager.
- **Alternatives Considered:**
  - Standard `pip` + `venv` (requires manual `requirements.txt` generation and lacks deterministic universal lockfiles).
  - `poetry` (slower dependency resolution, heavier runtime footprint).
- **Consequences:** Extremely fast installs, deterministic cross-platform `uv.lock`, seamless `uv run` command execution without manual virtualenv activation script issues.

## BEDR-003: FastAPI with Pydantic v2 and Async Architecture
- **Date:** 2026-11-05
- **Status:** Accepted
- **Context:** Need an asynchronous, type-safe Python API layer with first-class OpenAPI documentation and minimal boilerplate.
- **Decision:** Adopt FastAPI with Pydantic v2 for data validation and request/response serialization.
- **Alternatives Considered:**
  - Django / Django REST Framework (heavier monolithic battery, synchronous legacy defaults).
  - Flask (lacks native async, automatic validation, and modern OpenAPI schema generation).
- **Consequences:** High concurrency, automatic interactive Swagger UI documentation at `/docs`, compile-time/runtime type validation matching TypeScript developer mental models.

## BEDR-004: Shared Secret Header (`X-Service-Token`) for Internal Microservice Security
- **Date:** 2026-11-06
- **Status:** Accepted
- **Context:** Internal endpoints (such as challenge generation) should only ever be callable by trusted backend peers (Express API), never directly by public browsers or untrusted clients.
- **Decision:** Implement internal machine-to-machine security via a shared secret header `X-Service-Token` validated in FastAPI dependencies (`verify_service_token`).
- **Alternatives Considered:**
  - mTLS (Mutual TLS): Production gold standard for zero-trust VPCs, but introduces excessive certificate management complexity during local development.
  - Asymmetric JWT service accounts: Valid alternative, but shared token provides the right security level for current two-service boundary without token-issuing server overhead.
- **Consequences:** Protected internal endpoints, clear boundary between public vs internal routers.

## BEDR-005: 202 Accepted Asynchronous Job Model for AI Generation
- **Date:** 2026-11-06
- **Status:** Accepted
- **Context:** AI code analysis and bug synthesis can take 10 to 45 seconds depending on LLM latency. Synchronous HTTP calls risk gateway timeouts (504) and client latency degradation.
- **Decision:** Use an asynchronous job pattern where `POST /internal/v1/challenges/generate` validates input, immediately returns `202 Accepted` with a `jobId`, and exposes status polling via `GET /internal/v1/challenges/jobs/{job_id}`.
- **Alternatives Considered:**
  - Synchronous blocking HTTP request (causes connection timeouts on heavy workloads).
  - Heavy message broker (Kafka/RabbitMQ/Celery) (rejected prematurely per guide rules: start with in-memory/database job table before introducing external broker daemons).
- **Consequences:** Non-blocking API, predictable response times, status query capability.

## BEDR-006: Neon PostgreSQL as Cloud Database Engine
- **Date:** 2026-11-06
- **Status:** Accepted
- **Context:** The application requires a robust relational database engine capable of storing application entities (Express) and AI jobs/embeddings (FastAPI). Neon PostgreSQL (PostgreSQL 17.11) was selected as the cloud database.
- **Decision:** Use Neon PostgreSQL with SSL encryption (`sslmode=require`) across both Express and FastAPI services.
- **Alternatives Considered:**
  - Local Docker PostgreSQL (requires local Docker daemon running on Windows with resource overhead; cloud Neon allows instant serverless branching and zero local setup).
  - SQLite (lacks multi-process concurrency, JSONB indexing, and native schema isolation).
- **Consequences:** Zero local database maintenance, automated serverless scaling, modern PostgreSQL 17 features.

## BEDR-007: PostgreSQL Schema Isolation with `ai` Schema Ownership & Filtered Migrations
- **Date:** 2026-11-06
- **Status:** Accepted
- **Context:** Express and FastAPI share a single PostgreSQL database instance. We must prevent services from creating tables in arbitrary locations or interfering with each other's tables or third-party tables (such as `neon_auth` and existing user tables).
- **Decision:**
  1. FastAPI exclusively owns and writes to the `ai` schema. Express owns `app`.
  2. SQLAlchemy's `Base` is bound to `MetaData(schema="ai")`.
  3. Alembic is configured with strict `include_object` and `include_name` callbacks in `migrations/env.py` to only inspect the `"ai"` schema.
  4. Migration history table is stored inside `ai.alembic_version`.
- **Alternatives Considered:**
  - Separate database instances (higher operational cost and complexity for early stages).
  - Unscoped shared `public` schema (disaster prone: schema migrations can collide or accidentally drop tables owned by other services or database extensions).
- **Consequences:** Strict boundaries, zero risk of foreign table drops, clean microservice independence on a single database instance.


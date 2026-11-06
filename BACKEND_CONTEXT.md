# Backend Context — FastAPI AI Engine

## 1. Overview & Role in Multi-Service Architecture
- **Directory:** `MockPrep_FastAPI/` (excluded from frontend git tracking in root `.gitignore`).
- **Primary Framework:** FastAPI (Python 3.11/3.13+ via `uv`).
- **Package Manager:** `uv`.
- **Current Phase:** Phase 3 (FastAPI AI Service Initialization & Health Endpoint) completed. Next up: Phase 4 (Define API Contracts between Express & FastAPI).
- **Role:** Dedicated **AI & Intelligence Service** in the separated architecture defined in `AI_Project_Platform_Monorepo_Phased_Implementation_Guide.md`.
- **Express vs. FastAPI Division of Responsibilities:**
  - **Node.js Express API (`MockPrep_Express/`):** The primary application backend. Owns users, organizations, project metadata, challenge records, session state machines, authoritative countdown timers, Socket.IO realtime rooms, and PostgreSQL `app` schema.
  - **Python FastAPI Service (`MockPrep_BE/`):** The specialized AI computation backend. Owns LLM provider integrations, prompt templates, code chunking/indexing, vector retrieval (RAG / pgvector), synthetic challenge/bug injection, and AI evaluation signals.
  - **Service-to-Service Communication:** Express calls protected internal FastAPI endpoints. FastAPI does NOT perform general CRUD on Express application tables.

## 2. Technology Stack
- **Runtime:** Python 3.13.12
- **Package & Environment Manager:** `uv`
- **Web Framework:** FastAPI (with Uvicorn standard server)
- **Data Validation:** Pydantic v2
- **Vector & Relational Storage:** PostgreSQL (`ai` schema / `pgvector`)
- **Testing:** `pytest` + `httpx`
- **Linting & Formatting:** Ruff

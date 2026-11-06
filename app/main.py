from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.health import HealthResponse
from app.api.v1.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan context manager runs startup and shutdown logic.
    Replaces deprecated @app.on_event('startup') and @app.on_event('shutdown').
    """
    # Startup: Initialize connections, thread pools, or model cache
    print(f"[{settings.PROJECT_NAME}] Starting up in {settings.ENVIRONMENT} mode...")
    yield
    # Shutdown: Clean up connections or resources
    print(f"[{settings.PROJECT_NAME}] Shutting down gracefully...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Dedicated AI and Code Intelligence microservice for MockPrep platform.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Top-level root endpoint
@app.get(
    "/",
    summary="Root Service Index",
    tags=["Root"],
)
async def root() -> dict[str, str]:
    """Simple root greeting pointing to documentation."""
    return {
        "message": f"{settings.PROJECT_NAME} is running",
        "docs": "/docs",
        "version": settings.VERSION,
    }


# Top-level liveness probe (/health)
@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Top-Level Health Check",
    tags=["Health"],
)
async def root_health() -> HealthResponse:
    """Standard health check accessible at root level for orchestrators."""
    return HealthResponse(
        status="oks",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc),
    )


# Mount versioned API routes under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)

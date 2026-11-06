"""
Centralized API paths for Health check endpoints.
"""


class HealthPaths:
    """Path constants for liveness/readiness probes."""

    ROOT: str = "/"
    HEALTH: str = "/health"
    V1_HEALTH: str = "/api/v1/health"
    DOCS: str = "/docs"
    OPENAPI: str = "/openapi.json"


HEALTH_PATHS = HealthPaths()

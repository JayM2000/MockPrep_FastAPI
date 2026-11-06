from datetime import datetime, timezone
from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """
    Pydantic response schema documenting the health payload in Swagger/OpenAPI.
    """

    status: str = Field(default="ok", description="Service operational status")
    service: str = Field(..., description="Service identifier name")
    version: str = Field(..., description="Semantic version of the application")
    environment: str = Field(..., description="Runtime environment")
    timestamp: datetime = Field(..., description="Current server UTC timestamp")


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check Probe",
    description="Returns service availability, uptime timestamp, and metadata.",
)
async def check_health() -> HealthResponse:
    """
    Liveness probe used by container orchestrators and service monitors.
    """
    return HealthResponse(
        status="ok",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc),
    )

from typing import Any
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """
    Standardized inner error detail payload.
    """

    code: str = Field(..., description="Machine-readable error classification code")
    message: str = Field(..., description="Human-readable explanation of what went wrong")
    details: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional field-level validation errors or contextual metadata",
    )


class ErrorResponse(BaseModel):
    """
    Standardized error envelope used across both Express and FastAPI.
    Enforces a consistent shape: { "error": { "code": ..., "message": ..., "details": ... } }
    """

    error: ErrorDetail

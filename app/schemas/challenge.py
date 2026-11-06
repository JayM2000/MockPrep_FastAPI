from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class DifficultyLevel(str, Enum):
    """Target difficulty level for engineering challenges."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ChallengeType(str, Enum):
    """Types of challenges AI can inject into codebases."""

    BUG_FIX = "bug_fix"
    FEATURE_ADDITION = "feature_addition"
    REFACTORING = "refactoring"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    SECURITY_HARDENING = "security_hardening"


class JobStatus(str, Enum):
    """Lifecycle states of an asynchronous generation job."""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class CamelModel(BaseModel):
    """
    Base schema configured to support both camelCase (JSON API standard)
    and snake_case (Python standard) seamlessly.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ChallengeGenerateRequest(CamelModel):
    """
    Data Transfer Object (DTO) sent from Express to FastAPI to trigger challenge generation.
    """

    project_id: str = Field(..., min_length=1, description="Identifier of the project context")
    project_name: str = Field(..., min_length=1, description="Human-readable project title")
    difficulty: DifficultyLevel = Field(
        default=DifficultyLevel.MEDIUM,
        description="Target difficulty level",
    )
    tech_stack: list[str] = Field(
        default_factory=list,
        description="List of primary programming languages and frameworks",
    )
    code_summary: str = Field(
        ...,
        min_length=5,
        description="Architectural overview or summarized files of the project",
    )
    challenge_types: list[ChallengeType] = Field(
        default_factory=lambda: [ChallengeType.BUG_FIX],
        description="Types of challenges requested",
    )
    custom_instructions: str | None = Field(
        default=None,
        description="Optional author prompt notes or constraints",
    )


class ChallengeJobResponse(CamelModel):
    """
    Data Transfer Object (DTO) returned to Express indicating the job has been queued or its status.
    """

    job_id: str = Field(..., description="Unique tracking identifier for this background job")
    project_id: str = Field(..., description="Target project identifier")
    status: JobStatus = Field(
        default=JobStatus.QUEUED,
        description="Current lifecycle state of the AI generation job",
    )
    message: str = Field(..., description="Informative human-readable status description")
    estimated_duration_seconds: int = Field(
        default=15,
        description="Estimated duration in seconds before completion",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the job was accepted",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of the most recent status update",
    )
    result: dict[str, Any] | None = Field(
        default=None,
        description="Payload containing generated challenge details upon completion",
    )
    error: str | None = Field(
        default=None,
        description="Error details if the job status is failed",
    )

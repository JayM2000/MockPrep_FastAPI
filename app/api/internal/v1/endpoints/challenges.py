import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import verify_service_token
from app.schemas.challenge import (
    ChallengeGenerateRequest,
    ChallengeJobResponse,
    JobStatus,
)
from app.utils.challenge_paths import CHALLENGE_PATHS

router = APIRouter()

# Temporary in-memory dictionary for Phase 4 job tracking.
# In Phase 5+, this will be persisted in PostgreSQL.
_jobs_db: dict[str, ChallengeJobResponse] = {}


@router.post(
    CHALLENGE_PATHS.GENERATE,
    response_model=ChallengeJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Accept and Queue Challenge Generation Job",
    description="Called internally by Express API to queue AI challenge synthesis from project context.",
)
async def generate_challenge(
    payload: ChallengeGenerateRequest,
    _token: str = Depends(verify_service_token),
) -> ChallengeJobResponse:
    """
    Accepts project context from Express, creates an asynchronous job record,
    and returns 202 Accepted with tracking metadata.
    Protected by the internal service token.
    """
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)

    job = ChallengeJobResponse(
        job_id=job_id,
        project_id=payload.project_id,
        status=JobStatus.QUEUED,
        message=f"Challenge generation job accepted for project '{payload.project_name}'.",
        estimated_duration_seconds=15,
        created_at=now,
        updated_at=now,
    )

    _jobs_db[job_id] = job
    return job


@router.get(
    CHALLENGE_PATHS.JOB_BY_ID,
    response_model=ChallengeJobResponse,
    status_code=status.HTTP_200_OK,
    summary="Query Challenge Job Status",
    description="Polled or queried by Express to check status of an AI challenge generation task.",
)
async def get_challenge_job(
    job_id: str,
    _token: str = Depends(verify_service_token),
) -> ChallengeJobResponse:
    """
    Retrieves the current state of a background job by ID.
    Returns 404 if the job was not found.
    Protected by the internal service token.
    """
    job = _jobs_db.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID '{job_id}' not found",
        )
    return job

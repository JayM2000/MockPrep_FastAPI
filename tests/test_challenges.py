from fastapi.testclient import TestClient
from app.core.config import settings
from app.utils.challenge_paths import CHALLENGE_PATHS

VALID_TOKEN_HEADER = {"X-Service-Token": settings.INTERNAL_SERVICE_TOKEN}

SAMPLE_PAYLOAD = {
    "projectId": "proj_abc123",
    "projectName": "Payment Gateway Integration",
    "difficulty": "medium",
    "techStack": ["Node.js", "TypeScript", "PostgreSQL"],
    "codeSummary": "Express microservice processing Stripe webhook callbacks and subscription state.",
    "challengeTypes": ["bug_fix", "security_hardening"],
    "customInstructions": "Introduce an idempotency key validation issue and a missing signature check.",
}


def test_generate_challenge_unauthorized_missing_token(client: TestClient) -> None:
    """Verify request is rejected with 401 when X-Service-Token is omitted."""
    response = client.post(CHALLENGE_PATHS.FULL_GENERATE, json=SAMPLE_PAYLOAD)
    assert response.status_code == 401
    assert "detail" in response.json()


def test_generate_challenge_unauthorized_invalid_token(client: TestClient) -> None:
    """Verify request is rejected with 401 when X-Service-Token does not match."""
    response = client.post(
        CHALLENGE_PATHS.FULL_GENERATE,
        json=SAMPLE_PAYLOAD,
        headers={"X-Service-Token": "invalid-token"},
    )
    assert response.status_code == 401


def test_generate_challenge_validation_error(client: TestClient) -> None:
    """Verify request fails with 422 when required schema fields are missing or invalid."""
    invalid_payload = {
        "projectId": "proj_123",
        # Missing projectName and codeSummary
        "difficulty": "ultra-hard",  # Invalid enum value
    }
    response = client.post(
        CHALLENGE_PATHS.FULL_GENERATE,
        json=invalid_payload,
        headers=VALID_TOKEN_HEADER,
    )
    assert response.status_code == 422


def test_generate_challenge_success(client: TestClient) -> None:
    """Verify valid request returns 202 Accepted and creates a tracked job."""
    response = client.post(
        CHALLENGE_PATHS.FULL_GENERATE,
        json=SAMPLE_PAYLOAD,
        headers=VALID_TOKEN_HEADER,
    )
    assert response.status_code == 202
    data = response.json()

    assert "jobId" in data or "job_id" in data
    job_id = data.get("jobId") or data.get("job_id")
    assert job_id.startswith("job_")

    assert data.get("projectId") == "proj_abc123" or data.get("project_id") == "proj_abc123"
    assert data["status"] == "queued"
    assert "createdAt" in data or "created_at" in data


def test_get_challenge_job_status_success(client: TestClient) -> None:
    """Verify Express can poll/query the status of an existing job."""
    # First create a job
    create_res = client.post(
        CHALLENGE_PATHS.FULL_GENERATE,
        json=SAMPLE_PAYLOAD,
        headers=VALID_TOKEN_HEADER,
    )
    assert create_res.status_code == 202
    job_id = create_res.json().get("jobId") or create_res.json().get("job_id")

    # Now fetch it
    get_res = client.get(
        CHALLENGE_PATHS.full_job_by_id(job_id),
        headers=VALID_TOKEN_HEADER,
    )
    assert get_res.status_code == 200
    job_data = get_res.json()
    assert (job_data.get("jobId") or job_data.get("job_id")) == job_id
    assert job_data["status"] == "queued"


def test_get_challenge_job_status_not_found(client: TestClient) -> None:
    """Verify querying an unknown job returns 404."""
    response = client.get(
        CHALLENGE_PATHS.full_job_by_id("job_unknown_999"),
        headers=VALID_TOKEN_HEADER,
    )
    assert response.status_code == 404

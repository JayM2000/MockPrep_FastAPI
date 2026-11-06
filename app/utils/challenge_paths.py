"""
Centralized API paths for Challenge endpoints and internal service contracts.
"""


class ChallengePaths:
    """Path constants for internal challenge generation and tracking."""

    INTERNAL_PREFIX: str = "/internal/v1"
    CHALLENGES_PREFIX: str = "/challenges"

    GENERATE: str = "/generate"
    JOB_BY_ID: str = "/jobs/{job_id}"

    # Full endpoint paths
    FULL_GENERATE: str = "/internal/v1/challenges/generate"
    FULL_JOB_BASE: str = "/internal/v1/challenges/jobs"

    @staticmethod
    def full_job_by_id(job_id: str) -> str:
        """Returns the full path for querying a specific job by ID."""
        return f"/internal/v1/challenges/jobs/{job_id}"


CHALLENGE_PATHS = ChallengePaths()

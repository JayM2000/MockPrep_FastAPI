"""
Universal registry of API paths for the FastAPI service.
"""

from app.utils.challenge_paths import CHALLENGE_PATHS, ChallengePaths
from app.utils.health_paths import HEALTH_PATHS, HealthPaths


class ApiPaths:
    """Universal registry containing all service endpoint definitions."""

    HEALTH = HEALTH_PATHS
    CHALLENGES = CHALLENGE_PATHS


API_PATHS = ApiPaths()

__all__ = [
    "API_PATHS",
    "ApiPaths",
    "HEALTH_PATHS",
    "HealthPaths",
    "CHALLENGE_PATHS",
    "ChallengePaths",
]

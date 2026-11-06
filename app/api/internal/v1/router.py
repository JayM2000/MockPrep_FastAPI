from fastapi import APIRouter
from app.api.internal.v1.endpoints import challenges
from app.utils.challenge_paths import CHALLENGE_PATHS

internal_router = APIRouter()

# Mount challenge generation endpoints under /challenges
internal_router.include_router(
    challenges.router,
    prefix=CHALLENGE_PATHS.CHALLENGES_PREFIX,
    tags=["Internal - Challenges"],
)

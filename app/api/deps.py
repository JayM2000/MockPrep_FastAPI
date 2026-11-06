from typing import Annotated
from fastapi import Header, HTTPException, status
from app.core.config import settings


async def verify_service_token(
    x_service_token: Annotated[str | None, Header(alias="X-Service-Token")] = None,
) -> str:
    """
    Dependency to authenticate internal service-to-service requests.
    Validates that the caller provided the expected shared secret in the 'X-Service-Token' header.
    Rejects unauthorized external callers with 401 Unauthorized.
    """
    if not x_service_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing required internal authentication header: X-Service-Token",
            headers={"WWW-Authenticate": "ServiceToken"},
        )

    if x_service_token != settings.INTERNAL_SERVICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service token provided",
            headers={"WWW-Authenticate": "ServiceToken"},
        )

    return x_service_token

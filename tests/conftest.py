from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    TestClient fixture using httpx under the hood.
    Allows fast synchronous calls against the FastAPI ASGI app without opening network ports.
    """
    with TestClient(app) as test_client:
        yield test_client

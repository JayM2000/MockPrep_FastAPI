from fastapi.testclient import TestClient
from app.utils.health_paths import HEALTH_PATHS


def test_root_endpoint(client: TestClient) -> None:
    """Verify GET / returns 200 and docs pointer."""
    response = client.get(HEALTH_PATHS.ROOT)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert data["docs"] == HEALTH_PATHS.DOCS


def test_top_level_health_endpoint(client: TestClient) -> None:
    """Verify GET /health returns 200 and valid schema."""
    response = client.get(HEALTH_PATHS.HEALTH)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data
    assert "timestamp" in data


def test_v1_health_endpoint(client: TestClient) -> None:
    """Verify GET /api/v1/health returns 200."""
    response = client.get(HEALTH_PATHS.V1_HEALTH)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_openapi_schema(client: TestClient) -> None:
    """Verify OpenAPI JSON specification is generated."""
    response = client.get(HEALTH_PATHS.OPENAPI)
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert HEALTH_PATHS.HEALTH in schema["paths"]
    assert HEALTH_PATHS.V1_HEALTH in schema["paths"]


def test_swagger_docs(client: TestClient) -> None:
    """Verify Swagger UI HTML is served at /docs."""
    response = client.get(HEALTH_PATHS.DOCS)
    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower()

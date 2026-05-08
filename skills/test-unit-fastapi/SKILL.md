---
name: test-unit-fastapi
description: "FastAPI endpoint birim testi; httpx.AsyncClient ile in-process test, dependency injection override, pytest-asyncio entegrasyonu ve Sentinel API testleri"
---

## Purpose
FastAPI uygulamasını gerçek HTTP sunucusu başlatmadan test etmek; dependency injection'ı test ortamında override ederek izole ve hızlı birim testleri yazmak.

## Workflow

### Temel Test Yapısı
```python
# tests/test_metrics_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from sentinel.app import create_app
from sentinel.deps import get_prometheus_client

@pytest.fixture
async def client(mock_prometheus):
    app = create_app()
    # Gerçek Prometheus yerine mock kullan
    app.dependency_overrides[get_prometheus_client] = lambda: mock_prometheus
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()
```

### Endpoint Testleri
```python
@pytest.mark.asyncio
async def test_metrics_endpoint_returns_200(client):
    response = await client.get("/api/v1/metrics", params={"query": "up"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

@pytest.mark.asyncio
async def test_metrics_endpoint_validation_error(client):
    # Boş query parametresi
    response = await client.get("/api/v1/metrics", params={"query": ""})
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(e["loc"] == ["query", "query"] for e in errors)

@pytest.mark.asyncio
async def test_metrics_endpoint_backend_error(client, mock_prometheus):
    mock_prometheus.raise_on_call(httpx.ConnectError("bağlantı reddedildi"))
    response = await client.get("/api/v1/metrics", params={"query": "up"})
    assert response.status_code == 503
    assert "bağlantı" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

### Auth Middleware Testi
```python
@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client):
    response = await client.get("/api/v1/admin/config")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_valid_token(client, valid_jwt_token):
    response = await client.get(
        "/api/v1/admin/config",
        headers={"Authorization": f"Bearer {valid_jwt_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_protected_endpoint_expired_token(client, expired_jwt_token):
    response = await client.get(
        "/api/v1/admin/config",
        headers={"Authorization": f"Bearer {expired_jwt_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Token süresi dolmuş"
```

### Conftest Fixtures
```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_prometheus():
    mock = AsyncMock()
    mock.query.return_value = {
        "status": "success",
        "data": {"resultType": "vector", "result": []}
    }
    return mock

@pytest.fixture
def valid_jwt_token():
    from sentinel.auth import create_token
    return create_token({"sub": "test-user", "role": "admin"}, expires_in=3600)

@pytest.fixture
def expired_jwt_token():
    from sentinel.auth import create_token
    return create_token({"sub": "test-user"}, expires_in=-1)
```

### pyproject.toml
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"
```

## Common mistakes
- `TestClient` (sync) ile async handler test etmek — `httpx.AsyncClient` + `ASGITransport` kullan
- `dependency_overrides` temizlememek — fixture'da `app.dependency_overrides.clear()` zorunlu
- `pytest.mark.asyncio` unutmak — `asyncio_mode = "auto"` ile tüm async testler otomatik işaretlenir
- Mock'u return_value yerine side_effect olarak kurmak kafa karıştırıcı — exception için `side_effect`, normal dönüş için `return_value`

## References
- `skills/agentic-mcp-testing`
- `skills/test-mock-http`
- `skills/test-unit-pydantic`

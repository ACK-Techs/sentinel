---
name: fastapi-testing
description: "FastAPI TestClient ve async test kalıpları — Sentinel gateway endpoint testleri için entegrasyon test altyapısı"
---

## Purpose
FastAPI servislerini gerçek ASGI transport üzerinde, dependency override ile test etmek hem birim hem entegrasyon testlerinin gücünü birleştirir. Sentinel'de her route handler async TestClient ile test edilir; dış servisler (Tempo, Prometheus) mock client ile izole edilir.

## Workflow

### 1. Async TestClient conftest

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.dependencies import get_tempo_service, get_prometheus_service
from tests.mocks import MockTempoService, MockPrometheusService

@pytest_asyncio.fixture
async def app():
    _app = create_app()
    _app.dependency_overrides[get_tempo_service] = lambda: MockTempoService()
    _app.dependency_overrides[get_prometheus_service] = lambda: MockPrometheusService()
    yield _app
    _app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {make_test_token()}"},
    ) as ac:
        yield ac
```

### 2. Mock servisler

```python
# tests/mocks.py
from unittest.mock import AsyncMock
from app.models.trace import TraceResponse, SpanModel

class MockTempoService:
    async def get_trace(self, trace_id: str, **kwargs) -> TraceResponse | None:
        if trace_id == "not-found":
            return None
        return TraceResponse(
            trace_id=trace_id,
            spans=[
                SpanModel(id="span-1", service="gateway", duration_ms=10, status="OK"),
            ],
        )

    async def search_traces(self, **kwargs) -> list[TraceResponse]:
        return []
```

### 3. Endpoint testleri

```python
# tests/test_traces.py
import pytest

@pytest.mark.asyncio
async def test_get_trace_success(client):
    response = await client.get("/api/v1/traces/abc123")
    assert response.status_code == 200
    body = response.json()
    assert body["trace_id"] == "abc123"
    assert len(body["spans"]) == 1

@pytest.mark.asyncio
async def test_get_trace_not_found(client):
    response = await client.get("/api/v1/traces/not-found")
    assert response.status_code == 404
    assert response.json()["error"] == "TRACE_NOT_FOUND"

@pytest.mark.asyncio
async def test_unauthorized_without_token():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/traces/abc123")
    assert response.status_code == 401
```

### 4. Parametrize ile endpoint matrix testi

```python
@pytest.mark.parametrize("path,expected_status", [
    ("/health", 200),
    ("/ready", 200),
    ("/api/v1/traces/abc", 200),
    ("/api/v1/nonexistent", 404),
])
@pytest.mark.asyncio
async def test_endpoint_status_codes(client, path, expected_status):
    response = await client.get(path)
    assert response.status_code == expected_status
```

### 5. Lifespan ile entegrasyon testi

```python
from asgi_lifespan import LifespanManager

@pytest_asyncio.fixture
async def integration_client():
    """Gerçek lifespan çalıştıran tam entegrasyon testi."""
    app = create_app()
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
```

## Common mistakes

- `TestClient` (sync) kullanıp async route'ları test etmeye çalışmak — `AsyncClient` + `ASGITransport` kullan
- `dependency_overrides` temizlememek — sonraki test'e sızar
- Mock servislerin exception senaryolarını kapsamamak — `side_effect=TraceNotFoundError()` ekle
- `httpx.AsyncClient` ile `requests.Session` karıştırmak — FastAPI testleri için httpx zorunlu

## References
- `skills/python-testing-pytest`
- `skills/fastapi-dependency-injection`
- `skills/fastapi-exception-handlers`

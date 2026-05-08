---
name: test-mock-http
description: "respx/responses ile Sentinel dış HTTP çağrılarını mock'lama; Prometheus/Loki istemci testleri, request assertion ve ağ hatası simülasyonu"
---

## Purpose
Sentinel'in Prometheus, Loki, Tempo gibi dış servislere yaptığı HTTP çağrılarını ağ erişimi olmadan test etmek; spesifik request parametrelerini doğrulamak ve hata senaryolarını simüle etmek.

## Workflow

### respx ile httpx Mock (async)
```python
# tests/unit/test_prometheus_client.py
import pytest
import respx
import httpx
from sentinel.clients.prometheus import PrometheusClient

@pytest.mark.asyncio
@respx.mock
async def test_query_returns_parsed_result():
    # Mock endpoint tanımla
    respx.get("http://prometheus:9090/api/v1/query").mock(
        return_value=httpx.Response(200, json={
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [
                    {"metric": {"job": "sentinel"}, "value": [1700000000, "1"]}
                ]
            }
        })
    )
    
    client = PrometheusClient(base_url="http://prometheus:9090")
    result = await client.query("up{job='sentinel'}")
    
    assert result["status"] == "success"
    assert len(result["data"]["result"]) == 1

@pytest.mark.asyncio
@respx.mock
async def test_query_checks_correct_params():
    route = respx.get("http://prometheus:9090/api/v1/query")
    route.mock(return_value=httpx.Response(200, json={"status": "success", "data": {"result": []}}))
    
    client = PrometheusClient(base_url="http://prometheus:9090")
    await client.query("up", time="1700000000")
    
    # Request parametrelerini doğrula
    assert route.called
    request = route.calls.last.request
    assert "query=up" in str(request.url)
    assert "time=1700000000" in str(request.url)
```

### Hata Senaryoları
```python
@pytest.mark.asyncio
@respx.mock
async def test_connection_refused_raises_service_error():
    from sentinel.exceptions import BackendUnavailableError
    respx.get("http://prometheus:9090/api/v1/query").mock(
        side_effect=httpx.ConnectError("Connection refused")
    )
    
    client = PrometheusClient(base_url="http://prometheus:9090")
    
    with pytest.raises(BackendUnavailableError) as exc_info:
        await client.query("up")
    
    assert "prometheus" in str(exc_info.value).lower()

@pytest.mark.asyncio
@respx.mock
async def test_timeout_raises_service_error():
    respx.get("http://prometheus:9090/api/v1/query").mock(
        side_effect=httpx.TimeoutException("Timeout")
    )
    
    client = PrometheusClient(base_url="http://prometheus:9090")
    
    with pytest.raises(BackendUnavailableError):
        await client.query("up")

@pytest.mark.asyncio
@respx.mock
async def test_500_response_raises_error():
    respx.get("http://prometheus:9090/api/v1/query").mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )
    
    client = PrometheusClient(base_url="http://prometheus:9090")
    
    with pytest.raises(Exception):
        await client.query("up")
```

### Çoklu Endpoint Mock
```python
@pytest.fixture
def mock_observability_backends():
    with respx.mock() as mocked:
        mocked.get("http://prometheus:9090/-/healthy").mock(
            return_value=httpx.Response(200, text="Prometheus is Healthy.")
        )
        mocked.get("http://loki:3100/ready").mock(
            return_value=httpx.Response(200, text="ready")
        )
        mocked.get("http://tempo:3200/ready").mock(
            return_value=httpx.Response(200, json={"status": "ready"})
        )
        yield mocked

@pytest.mark.asyncio
async def test_all_backends_healthy(mock_observability_backends):
    from sentinel.health import check_all_backends
    result = await check_all_backends()
    assert result["prometheus"] is True
    assert result["loki"] is True
    assert result["tempo"] is True
```

### responses ile requests Mock (sync)
```python
import responses

@responses.activate
def test_sync_client_query():
    responses.add(
        responses.GET,
        "http://prometheus:9090/api/v1/query",
        json={"status": "success", "data": {"result": []}},
        status=200
    )
    
    from sentinel.clients.sync import SyncPrometheusClient
    client = SyncPrometheusClient(base_url="http://prometheus:9090")
    result = client.query("up")
    assert result["status"] == "success"
```

## Common mistakes
- `@respx.mock` decorator ile `respx.mock()` context manager karıştırmak — birini seç
- Unmocked URL'e istek atılmasına izin vermek — `respx.mock(assert_all_called=True)` beklenmeyen çağrıları yakalar
- Request body doğrulaması yapmamak — POST endpoint'lerinde body içeriğini `route.calls.last.request.content` ile kontrol et
- Sync `httpx.Client` için async mock kullanmak — `requests` + `responses` veya sync `httpx.Client` mock'la

## References
- `skills/test-unit-fastapi`
- `skills/test-mock-llm`

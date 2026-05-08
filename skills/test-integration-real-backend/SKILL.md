---
name: test-integration-real-backend
description: "Gerçek Prometheus/Loki/Tempo backend'e karşı entegrasyon testi; staging ortamı varsayımları, idempotent test verisi ve teardown garantisi"
---

## Purpose
Sentinel'in gerçek observability backend'leriyle (Prometheus, Loki, Tempo) doğru entegrasyon kurduğunu canlıya yakın ortamda doğrulamak; mock'ların gizleyebileceği ağ ve serialization hatalarını tespit etmek.

## Workflow

### Ortam Ayarları
```python
# tests/integration/conftest.py
import pytest
import os
import httpx

PROMETHEUS_URL = os.environ.get("TEST_PROMETHEUS_URL", "http://localhost:9090")
LOKI_URL = os.environ.get("TEST_LOKI_URL", "http://localhost:3100")
TEMPO_URL = os.environ.get("TEST_TEMPO_URL", "http://localhost:3200")

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "real_backend: gerçek observability servislerini gerektirir"
    )

@pytest.fixture(scope="session", autouse=True)
def verify_backends():
    """Backend'ler erişilebilir değilse testleri atla"""
    backends = {
        "prometheus": f"{PROMETHEUS_URL}/-/healthy",
        "loki": f"{LOKI_URL}/ready",
        "tempo": f"{TEMPO_URL}/ready",
    }
    missing = []
    for name, url in backends.items():
        try:
            r = httpx.get(url, timeout=3)
            if r.status_code != 200:
                missing.append(name)
        except Exception:
            missing.append(name)
    
    if missing:
        pytest.skip(f"Backend'ler erişilemez: {missing} — TEST_*_URL env değişkenlerini kontrol et")
```

### Prometheus Entegrasyon Testi
```python
# tests/integration/test_prometheus_client.py
import pytest
import time
from sentinel.clients.prometheus import PrometheusClient

@pytest.mark.real_backend
@pytest.mark.asyncio
async def test_instant_query_returns_result():
    client = PrometheusClient(base_url=PROMETHEUS_URL)
    result = await client.query("up")
    
    assert result["status"] == "success"
    assert result["data"]["resultType"] == "vector"
    # Prometheus kendisi en az 1 up metriği rapor eder
    assert len(result["data"]["result"]) >= 1

@pytest.mark.real_backend
@pytest.mark.asyncio
async def test_range_query_time_span():
    client = PrometheusClient(base_url=PROMETHEUS_URL)
    end = int(time.time())
    start = end - 300  # son 5 dakika
    
    result = await client.query_range(
        query="up",
        start=start,
        end=end,
        step="60s"
    )
    
    assert result["status"] == "success"
    assert result["data"]["resultType"] == "matrix"

@pytest.mark.real_backend
@pytest.mark.asyncio
async def test_invalid_promql_returns_error():
    client = PrometheusClient(base_url=PROMETHEUS_URL)
    
    with pytest.raises(Exception) as exc_info:
        await client.query("invalid{{{query")
    
    assert "400" in str(exc_info.value) or "parse error" in str(exc_info.value).lower()
```

### Loki Log Push + Query Döngüsü
```python
@pytest.mark.real_backend
@pytest.mark.asyncio
async def test_push_and_query_logs():
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    client = LokiClient(base_url=LOKI_URL)
    
    # Log push
    now_ns = int(time.time() * 1e9)
    await client.push_logs(
        streams=[{
            "stream": {"job": "sentinel-test", "test_id": unique_id},
            "values": [[str(now_ns), f"test log message {unique_id}"]]
        }]
    )
    
    # Kısa bekle (Loki ingestion gecikmesi)
    await asyncio.sleep(2)
    
    # Sorgula
    result = await client.query_range(
        query=f'{{job="sentinel-test", test_id="{unique_id}"}}',
        start=int(time.time()) - 10,
        end=int(time.time())
    )
    
    entries = result["data"]["result"]
    assert len(entries) > 0
    assert unique_id in entries[0]["values"][0][1]
```

### CI Konfigürasyonu
```yaml
# .github/workflows/integration-tests.yml
jobs:
  integration:
    runs-on: ubuntu-latest
    services:
      prometheus:
        image: prom/prometheus:v2.47.0
        ports: ["9090:9090"]
    env:
      TEST_PROMETHEUS_URL: http://localhost:9090
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration/ -m real_backend --tb=short
```

## Common mistakes
- Test verisi için prodüksiyon metric label'ları kullanmak — `test_id` gibi izole label'lar ekle
- Loki push sonrası hemen sorgu yapmak — ingestion 1-3 saniye sürer; `asyncio.sleep(2)` gerekli
- Backend URL'lerini hardcode etmek — env değişkeni zorunlu, farklı ortamlarda farklı URL
- Teardown olmadan test çalıştırmak — Tempo trace'leri ve Loki stream'leri temizlenmezse quota dolar

## References
- `skills/test-integration-docker-compose`
- `skills/agentic-mcp-observability-server`

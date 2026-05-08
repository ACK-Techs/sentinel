---
name: test-contract-pact
description: "Pact ile consumer-driven contract testi; Sentinel API istemcisi consumer contract oluşturma, provider doğrulama ve Pact Broker entegrasyonu"
---

## Purpose
Sentinel API istemcisi (consumer) ile API sunucusu (provider) arasındaki kontrakt uyumunu bağımsız deploy öncesinde doğrulamak; API değişikliklerinin istemciyi kırmadığını garanti etmek.

## Workflow

### Consumer Tarafı (İstemci Contract Oluşturma)
```python
# tests/contract/test_metrics_consumer.py
import pytest
from pact import Consumer, Provider, Like, Term, EachLike
from sentinel.clients.metrics import MetricsClient

PACT_DIR = "pacts/"

@pytest.fixture(scope="session")
def pact():
    pact = Consumer("sentinel-dashboard").has_pact_with(
        Provider("sentinel-api"),
        pact_dir=PACT_DIR,
        log_dir="logs/",
    )
    pact.start_service()
    yield pact
    pact.stop_service()

def test_query_metrics_success(pact):
    # Beklenen etkileşimi tanımla
    (pact
     .given("Prometheus'ta metrik verisi var")
     .upon_receiving("up metriği isteği")
     .with_request(
         method="GET",
         path="/api/v1/metrics",
         query={"query": "up"},
         headers={"Authorization": Term(r"Bearer .+", "Bearer test-token")}
     )
     .will_respond_with(
         status=200,
         body={
             "status": "success",
             "data": {
                 "resultType": "vector",
                 "result": EachLike({
                     "metric": {"__name__": Like("up"), "job": Like("sentinel")},
                     "value": [Like(1700000000), Like("1")]
                 })
             }
         }
     ))
    
    with pact:
        client = MetricsClient(base_url=pact.uri)
        result = client.query("up", headers={"Authorization": "Bearer test-token"})
    
    assert result["status"] == "success"

def test_query_metrics_not_found(pact):
    (pact
     .given("Prometheus'ta bu metrik yok")
     .upon_receiving("var olmayan metrik isteği")
     .with_request(method="GET", path="/api/v1/metrics", query={"query": "nonexistent_metric"})
     .will_respond_with(status=200, body={"status": "success", "data": {"result": []}}))
    
    with pact:
        client = MetricsClient(base_url=pact.uri)
        result = client.query("nonexistent_metric")
    
    assert result["data"]["result"] == []
```

### Provider Tarafı (Doğrulama)
```python
# tests/contract/test_sentinel_api_provider.py
import pytest
from pact import Verifier
from sentinel.app import create_app

@pytest.fixture(scope="session")
def app():
    return create_app(testing=True)

def test_provider_honors_consumer_contracts(app):
    verifier = Verifier(
        provider="sentinel-api",
        provider_base_url="http://localhost:8001"
    )
    
    output, _ = verifier.verify_pacts(
        pacts=["pacts/sentinel-dashboard-sentinel-api.json"],
        provider_states_setup_url="http://localhost:8001/_pact/provider_states",
        verbose=True
    )
    
    assert output == 0, "Provider contract doğrulaması başarısız"
```

### Provider State Endpoint
```python
# sentinel/routes/pact_states.py (sadece test ortamında)
from fastapi import APIRouter, Request
import httpx

router = APIRouter()

@router.post("/_pact/provider_states")
async def setup_provider_state(request: Request):
    body = await request.json()
    state = body.get("state")
    
    if state == "Prometheus'ta metrik verisi var":
        # Mock veya test fixture'ı ayarla
        pass
    elif state == "Prometheus'ta bu metrik yok":
        pass
    
    return {"result": "state set up"}
```

### Pact Broker Entegrasyonu
```yaml
# .github/workflows/contract-tests.yml
- name: Consumer - pact oluştur
  run: pytest tests/contract/test_metrics_consumer.py -v

- name: Pact Broker'a yükle
  run: |
    pact-broker publish pacts/ \
      --broker-base-url $PACT_BROKER_URL \
      --consumer-app-version $GITHUB_SHA \
      --tag $GITHUB_REF_NAME

- name: Provider - contract doğrula
  run: pytest tests/contract/test_sentinel_api_provider.py -v
  env:
    PACT_BROKER_URL: ${{ secrets.PACT_BROKER_URL }}
```

## Common mistakes
- `Like()` yerine sabit değer kullanmak — istemci test verisiyle kilitlenir, provider schema esnekliği kaybolur
- Provider state endpoint'i production'a dahil etmek — sadece `TESTING=True` koşulunda mount et
- Consumer ve provider testlerini aynı process'te çalıştırmak — bağımsız deploy edilebilirlik kaybolur
- Pact broker olmadan pact dosyalarını git'e commitleme — versiyon takibi zorlaşır

## References
- `skills/test-unit-fastapi`
- `skills/test-integration-real-backend`

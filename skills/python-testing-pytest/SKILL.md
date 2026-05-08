---
name: python-testing-pytest
description: "pytest fixture, parametrize ve plugin ekosistemi — Sentinel servis testleri için kapsamlı test altyapısı"
---

## Purpose
pytest, Sentinel'deki FastAPI servisleri, ajan mantığı ve observability entegrasyon testleri için birincil test çerçevesidir. Fixture scope yönetimi, parametrize ile kombinatoryal test ve pytest-asyncio ile async test desteği bu skill'in odağındadır.

## Workflow

### 1. conftest.py ve fixture hiyerarşisi

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.database import get_db, TestDatabase

@pytest.fixture(scope="session")
def test_db():
    """Session boyunca tek veritabanı — pahalı kurulum bir kez yapılır."""
    db = TestDatabase.create()
    yield db
    db.teardown()

@pytest.fixture(scope="function")
def db_session(test_db):
    """Her test için izole transaction — test sonunda rollback."""
    session = test_db.session()
    yield session
    session.rollback()
    session.close()

@pytest_asyncio.fixture
async def client(db_session):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
```

### 2. Parametrize ile çok senaryo testi

```python
# tests/test_alert_rules.py
import pytest

SEVERITY_CASES = [
    ("critical", 0.95, True),
    ("warning", 0.75, True),
    ("info", 0.50, False),
    ("unknown", 0.99, False),
]

@pytest.mark.parametrize("severity,threshold,should_fire", SEVERITY_CASES)
def test_alert_rule_evaluation(severity, threshold, should_fire):
    from sentinel.alerting import evaluate_rule
    rule = AlertRule(severity=severity, threshold=threshold)
    result = evaluate_rule(rule, current_value=0.80)
    assert result.fired == should_fire
```

### 3. Async test ve mock

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_trace_fetch_timeout(client):
    with patch("sentinel.clients.tempo.TempoClient.get_trace") as mock_get:
        mock_get.side_effect = TimeoutError("Tempo yanıt vermedi")

        response = await client.get("/api/v1/traces/abc123")

        assert response.status_code == 504
        assert response.json()["error"] == "UPSTREAM_TIMEOUT"
```

### 4. Özel fixture factory

```python
@pytest.fixture
def make_span():
    """Span factory fixture — her test ihtiyacına göre özelleştirilebilir."""
    def _make(service="gateway", duration_ms=10, error=False, **kwargs):
        return Span(
            id=f"span-{uuid.uuid4().hex[:8]}",
            service=service,
            duration_ms=duration_ms,
            status="ERROR" if error else "OK",
            **kwargs,
        )
    return _make

def test_slow_span_detection(make_span):
    spans = [make_span(duration_ms=d) for d in [5, 150, 8, 200]]
    slow = detect_slow_spans(spans, threshold_ms=100)
    assert len(slow) == 2
```

### 5. pytest.ini yapılandırması

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
markers =
    integration: Gerçek servislere bağlanan testler
    unit: Bağımsız birim testleri
    slow: 1 saniyeden uzun süren testler
addopts = -v --tb=short -x
```

## Common mistakes

- `scope="session"` fixture içinde mutable state tutmak — testler arası kirlilik yaratır
- `pytest.mark.asyncio` ile `asyncio_mode = auto` birlikte kullanmak — ikisi çakışır, birini seç
- `patch` decorator sırasını parametrize ile karıştırmak — `@pytest.mark.parametrize` en dışta olmalı
- `assert` yerine `assertEqual` kullanmak — pytest'in detaylı assertion introspection'ı çalışmaz

## References
- `skills/fastapi-testing`
- `skills/python-error-hierarchy`
- `skills/python-pre-commit`

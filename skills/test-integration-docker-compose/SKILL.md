---
name: test-integration-docker-compose
description: "Docker Compose ile servis bağımlılıkları içeren entegrasyon testi; pytest-docker veya doğrudan compose up ile Postgres/Redis/Prometheus ayağa kaldırma ve health check bekleme"
---

## Purpose
Sentinel servislerinin gerçek altyapıyla (PostgreSQL, Redis, Prometheus) birlikte doğru çalışıp çalışmadığını izole Docker ortamında test etmek.

## Workflow

### docker-compose.test.yml
```yaml
version: "3.9"
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: sentinel_test
      POSTGRES_USER: sentinel
      POSTGRES_PASSWORD: testpass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sentinel -d sentinel_test"]
      interval: 2s
      timeout: 5s
      retries: 15

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 2s
      timeout: 3s
      retries: 10

  prometheus:
    image: prom/prometheus:v2.47.0
    ports:
      - "9090:9090"
    volumes:
      - ./tests/fixtures/prometheus.yml:/etc/prometheus/prometheus.yml
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:9090/-/healthy"]
      interval: 3s
      timeout: 5s
      retries: 10
```

### pytest-docker Entegrasyonu
```python
# tests/conftest.py
import pytest
import time
import psycopg2
import redis
import httpx

@pytest.fixture(scope="session")
def docker_compose_file():
    return "docker-compose.test.yml"

@pytest.fixture(scope="session")
def docker_services(docker_services):
    """Tüm servisler hazır olana kadar bekle"""
    docker_services.wait_until_responsive(
        timeout=60.0,
        pause=2.0,
        check=lambda: _all_services_ready()
    )
    return docker_services

def _all_services_ready() -> bool:
    try:
        conn = psycopg2.connect(
            host="localhost", port=5432,
            dbname="sentinel_test", user="sentinel", password="testpass"
        )
        conn.close()
        
        r = redis.Redis(host="localhost", port=6379)
        r.ping()
        
        resp = httpx.get("http://localhost:9090/-/healthy", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False
```

### Entegrasyon Testi Örneği
```python
# tests/integration/test_alert_storage.py
import pytest
from sentinel.storage.alert_repo import AlertRepository
from sentinel.models.alert import AlertRule

@pytest.fixture
def db_connection():
    import psycopg2
    conn = psycopg2.connect(
        host="localhost", port=5432,
        dbname="sentinel_test", user="sentinel", password="testpass"
    )
    # Tablolar oluştur
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alert_rules (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                expr TEXT NOT NULL,
                severity VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
    conn.commit()
    yield conn
    # Temizlik
    with conn.cursor() as cur:
        cur.execute("TRUNCATE alert_rules")
    conn.commit()
    conn.close()

@pytest.mark.integration
async def test_alert_rule_persist_and_retrieve(db_connection, docker_services):
    repo = AlertRepository(db_connection)
    
    rule = AlertRule(
        name="test_rule",
        expr="up == 0",
        severity="warning",
        for_duration="5m"
    )
    
    created = await repo.create(rule)
    assert created.id is not None
    
    fetched = await repo.get_by_name("test_rule")
    assert fetched.expr == "up == 0"
    assert fetched.severity == "warning"
```

### Makefile ile Kolaylaştırma
```makefile
test-integration:
    docker compose -f docker-compose.test.yml up -d --wait
    pytest tests/integration/ -m integration -v
    docker compose -f docker-compose.test.yml down

test-integration-clean:
    docker compose -f docker-compose.test.yml down -v
```

## Common mistakes
- Health check olmadan hemen test başlatmak — servisler 2-10 saniye sonra hazır olur; `wait_until_responsive` zorunlu
- Her test fonksiyonunda `scope="session"` fixture yeniden başlatmak — Docker compose `scope="session"` ile bir kez başlar
- Test sonrası veriyi temizlememek — paralel test çalıştırmada testler birbirini bozar; her test transaction içinde çalışsın veya `TRUNCATE` yapsın
- `localhost` yerine servis adını kullanmak — compose içinde `postgres`, dışarıdan `localhost:5432`

## References
- `skills/test-integration-real-backend`
- `skills/data-postgres-schema-design`

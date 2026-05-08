---
name: debug-ci-flaky-test
description: "CI pipeline'ında aralıklı başarısız olan testleri tespit eder, kök nedeni belirler ve stabil hale getirir"
---

## Purpose
Sentinel monoreposunda CI çalışmaları bazen aynı commit için farklı sonuçlar üretir. Bu "flaky" testler ekip güvenini zedeler ve merge sürecini yavaşlatır. Bu skill, flaky test'i izole eder, zaman, sıra veya kaynak bağımlılığı olup olmadığını belirler ve kalıcı çözüm üretir.

## Workflow

### 1. Flaky test'i GitHub Actions loglarından tespit et
```bash
# gh CLI ile son N çalışmanın sonucunu çek
gh run list --workflow=ci.yml --branch=main --limit=20 --json conclusion,databaseId | \
  jq '.[] | select(.conclusion != "success") | .databaseId'

# Belirli çalışmanın log'unu indir
gh run download <run-id> --dir /tmp/ci-logs
grep -r "FAILED\|ERROR\|flaky" /tmp/ci-logs/
```

### 2. Test başarısızlık oranını hesapla
```python
# Son 50 CI çalışmasında kaç kere başarısız?
import subprocess, json

runs = json.loads(subprocess.check_output(
    "gh run list --limit 50 --json conclusion,databaseId,headSha",
    shell=True
))
fail_rate = sum(1 for r in runs if r["conclusion"] == "failure") / len(runs)
print(f"Failure rate: {fail_rate:.1%}")
```

### 3. Flaky kategorisini belirle

#### Timing-dependent (async/sleep)
```python
# Anti-pattern: sabit sleep
time.sleep(2)
assert result == "done"

# Fix: polling wait
import time
for _ in range(20):
    if check_condition(): break
    time.sleep(0.1)
else:
    pytest.fail("Condition not met in 2s")
```

#### Port çakışması (parallel test)
```bash
# pytest-xdist ile paralel çalışırken port çakışması
# Fix: ephemeral port kullan
import socket
def get_free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]
```

#### Database isolation eksikliği
```python
# Fix: her test için transaction rollback
@pytest.fixture(autouse=True)
def db_transaction(db_session):
    yield db_session
    db_session.rollback()
```

#### External service mock eksikliği
```python
# Gerçek HTTP call yerine respx mock
import respx, httpx

@respx.mock
async def test_payment_call():
    respx.post("http://payments/charge").mock(return_value=httpx.Response(200))
    result = await orders_service.create_order(...)
    assert result.status == "confirmed"
```

### 4. CI'da deterministic seed kullan
```yaml
# .github/workflows/ci.yml
- name: Run tests
  env:
    PYTHONHASHSEED: "42"  # Dict/set ordering determinism
    RANDOM_SEED: "42"
  run: pytest tests/ -v --randomly-seed=42
```

### 5. Quarantine ve flaky label
```bash
# pytest-mark ile flaky test'i işaretle
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_unstable_integration():
    ...

# CI'da flaky testleri ayrı job'da çalıştır
pytest tests/ -m "not flaky" --strict-markers
pytest tests/ -m "flaky" --reruns=3
```

## Common mistakes
1. Flaky test'i `skip` ile kapatmak — sorun görünmez olur ama var olmaya devam eder.
2. `time.sleep()` değerini artırarak fix etmeye çalışmak — CI makinesi yavaşladığında yine kırılır.
3. Test sırasının önemli olmadığını varsaymak — `pytest-randomly` ile sıra bağımlılığını tespit et.
4. Tek bir başarısızlık örneğinden root cause çıkarmak — en az 5 başarısız log karşılaştır.

## References
- `skills/ci-pr-gate`
- `skills/ci-github-actions-matrix`

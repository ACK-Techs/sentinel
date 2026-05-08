---
name: test-benchmark-pytest
description: "pytest-benchmark ile Sentinel Python fonksiyonlarının performans testi; baseline kaydetme, regresyon tespiti ve CI'da otomatik karşılaştırma"
---

## Purpose
Sentinel'in kritik yollarındaki (PromQL parsing, alert rule değerlendirme, log filtering) performansını ölçmek ve regresyonları CI'da otomatik tespit etmek.

## Workflow

### Temel Benchmark Testi
```python
# tests/benchmarks/test_parser_perf.py
import pytest
from sentinel.promql import parse_expr
from sentinel.validators import validate_duration
from sentinel.alert_rules import evaluate_rules

def test_promql_parse_simple(benchmark):
    result = benchmark(parse_expr, "up{job='sentinel'}")
    assert result is not None

def test_promql_parse_complex(benchmark):
    expr = "rate(http_requests_total{job='api',status=~'5..'}[5m])"
    result = benchmark(parse_expr, expr)
    assert result is not None

def test_duration_validate_batch(benchmark):
    durations = ["1s", "5m", "1h", "30d"] * 250  # 1000 item
    
    def validate_batch():
        return [validate_duration(d) for d in durations]
    
    result = benchmark(validate_batch)
    assert all(result)

# Parametrik benchmark
@pytest.mark.parametrize("n_rules", [10, 100, 1000])
def test_alert_rules_evaluate_scale(benchmark, n_rules, make_alert_rules):
    rules = make_alert_rules(n_rules)
    metrics = {"up": 0, "error_rate": 0.05}
    
    result = benchmark(evaluate_rules, rules, metrics)
    assert len(result) == n_rules
```

### Fixture ile Benchmark Konfigürasyonu
```python
# conftest.py
import pytest

@pytest.fixture
def make_alert_rules():
    from sentinel.models.alert import AlertRule
    def factory(n: int) -> list[AlertRule]:
        return [
            AlertRule(
                name=f"rule_{i}",
                expr=f"metric_{i} > {i}",
                severity="warning",
                for_duration="1m"
            )
            for i in range(n)
        ]
    return factory
```

### pyproject.toml Konfigürasyonu
```toml
[tool.pytest.ini_options]
addopts = "--benchmark-disable"  # normal test çalışmasında benchmark'ı devre dışı bırak

[benchmark]
min_rounds = 5
min_time = 0.1
max_time = 2.0
warmup = true
warmup_iterations = 1
timer = "perf_counter"
```

### Baseline Kaydetme ve Karşılaştırma
```bash
# Mevcut branch baseline kaydet
pytest tests/benchmarks/ --benchmark-save=main-baseline

# Değişiklik sonrası karşılaştır
pytest tests/benchmarks/ --benchmark-compare=main-baseline --benchmark-compare-fail=mean:10%

# CI — %10'dan fazla yavaşlama başarısız sayılır
pytest tests/benchmarks/ \
  --benchmark-compare=0001_main-baseline \
  --benchmark-compare-fail=mean:10% \
  --benchmark-json=results.json
```

### Sonuç Çıktısı
```
Name                              Min        Max        Mean     StdDev
---------------------------------------------------------------------------
test_promql_parse_simple          12.3 us    18.1 us    13.2 us  1.1 us
test_promql_parse_complex         45.2 us    62.8 us    48.3 us  3.4 us
test_duration_validate_batch      892 us     1.2 ms     941 us   48 us
test_alert_rules_evaluate[10]     234 us     312 us     256 us   18 us
test_alert_rules_evaluate[100]    2.31 ms    3.12 ms    2.54 ms  158 us
test_alert_rules_evaluate[1000]   23.1 ms    31.2 ms    25.4 ms  1.58 ms
```

## Common mistakes
- I/O içeren fonksiyonu doğrudan benchmark etmek — ağ/disk gecikmesi ölçümü kirletir; mock veya in-memory fixture kullan
- `--benchmark-disable` olmadan normal test koşumunda benchmark çalıştırmak — test suite 10x yavaşlar
- Tek round ile sonuç almak — `min_rounds=5` ile istatistiksel anlamlılık sağla
- JIT warmup'ı hesaba katmamak — `warmup=true` ile ilk yavaş iterasyonu dışla

## References
- `skills/perf-python-profiling`
- `skills/test-unit-fastapi`

---
name: test-fixtures-factory
description: "pytest fixture factory (factory_boy) ile Sentinel test verisi üretimi; AlertRule, MetricSample, LogEntry fabrika sınıfları ve ilişkili veri seti oluşturma"
---

## Purpose
Sentinel test verisi için tekrar yazılan `AlertRule(name=..., expr=..., ...)` bloklarını factory sınıflarıyla merkezileştirmek; tutarlı, parametrik test verisi üretmek.

## Workflow

### factory_boy Fabrika Sınıfları
```python
# tests/factories.py
import factory
from factory import LazyAttribute, Faker, SubFactory, LazyFunction
from sentinel.models.alert import AlertRule, AlertGroup
from sentinel.models.metrics import MetricSample
from sentinel.models.logs import LogEntry
import time

class AlertRuleFactory(factory.Factory):
    class Meta:
        model = AlertRule
    
    name = factory.Sequence(lambda n: f"alert_rule_{n}")
    expr = LazyAttribute(lambda o: f"metric_{o.name} > 0.9")
    severity = factory.Iterator(["critical", "warning", "info"])
    for_duration = factory.Iterator(["1m", "5m", "15m"])
    labels = factory.LazyFunction(lambda: {"team": "platform"})
    
    class Params:
        critical = factory.Trait(
            severity="critical",
            labels=factory.LazyFunction(lambda: {
                "team": "platform",
                "runbook_url": "https://runbooks.example.com/critical"
            })
        )
        with_annotation = factory.Trait(
            labels=factory.LazyFunction(lambda: {
                "team": "platform",
                "summary": "Test alert"
            })
        )

class MetricSampleFactory(factory.Factory):
    class Meta:
        model = MetricSample
    
    name = factory.Iterator(["up", "http_requests_total", "cpu_usage_seconds"])
    value = factory.Faker("pyfloat", min_value=0.0, max_value=1.0)
    timestamp = factory.LazyFunction(lambda: int(time.time()))
    labels = factory.LazyFunction(lambda: {"job": "sentinel", "instance": "pod-1"})

class LogEntryFactory(factory.Factory):
    class Meta:
        model = LogEntry
    
    timestamp = factory.LazyFunction(lambda: int(time.time() * 1e9))
    stream = factory.LazyFunction(lambda: {"app": "sentinel", "namespace": "default"})
    message = factory.Faker("sentence")
    level = factory.Iterator(["INFO", "WARN", "ERROR", "DEBUG"])
```

### pytest Fixture Entegrasyonu
```python
# tests/conftest.py
import pytest
from tests.factories import AlertRuleFactory, MetricSampleFactory, LogEntryFactory

@pytest.fixture
def alert_rule():
    return AlertRuleFactory()

@pytest.fixture
def critical_alert_rule():
    return AlertRuleFactory(critical=True)

@pytest.fixture
def alert_rules(request):
    """n adet kural oluştur: @pytest.mark.parametrize ile kullan"""
    count = getattr(request, "param", 5)
    return AlertRuleFactory.create_batch(count)

@pytest.fixture
def metric_samples():
    return MetricSampleFactory.create_batch(100)
```

### Test Kullanımı
```python
# tests/unit/test_alert_evaluator.py
import pytest
from tests.factories import AlertRuleFactory, MetricSampleFactory

def test_evaluate_single_critical_rule(critical_alert_rule):
    from sentinel.evaluator import evaluate_rule
    metrics = {"cpu_usage": 0.95}
    result = evaluate_rule(critical_alert_rule, metrics)
    assert result.fired is True

@pytest.mark.parametrize("alert_rules", [10, 50, 100], indirect=True)
def test_bulk_evaluation_performance(alert_rules, benchmark):
    from sentinel.evaluator import evaluate_all
    metrics = {f"metric_{r.name}": 0.95 for r in alert_rules}
    result = benchmark(evaluate_all, alert_rules, metrics)
    assert len(result) == len(alert_rules)

def test_alert_group_with_rules():
    group = AlertGroupFactory(
        rules=AlertRuleFactory.create_batch(3)
    )
    assert len(group.rules) == 3
    assert all(r.for_duration in ["1m", "5m", "15m"] for r in group.rules)
```

### SQLAlchemy Factory (DB entegrasyonu)
```python
# factory_boy SQLAlchemy session entegrasyonu
import factory.alchemy

class AlertRuleDBFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AlertRuleORM
        sqlalchemy_session = None  # fixture'da ayarla
    
    name = factory.Sequence(lambda n: f"db_rule_{n}")
    expr = "up > 0"
    severity = "warning"
    for_duration = "5m"

@pytest.fixture
def db_alert_rule(db_session):
    AlertRuleDBFactory._meta.sqlalchemy_session = db_session
    return AlertRuleDBFactory()
```

## Common mistakes
- Her test dosyasında ayrı `AlertRule(...)` oluşturmak — factory kullan, değişiklik tek yerde
- Factory'de sabit değer kullanmak — `factory.Sequence` ve `factory.Iterator` ile çeşitlilik sağla
- `create_batch()` ile DB factory kullanırken session ayarlamamak — `_meta.sqlalchemy_session` zorunlu
- Test verisi ile seed data karıştırmak — factory sadece test içinde çalışır, fixture scope yönetir

## References
- `skills/test-unit-pydantic`
- `skills/test-integration-docker-compose`

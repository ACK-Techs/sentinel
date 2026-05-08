---
name: test-property-based
description: "Hypothesis ile property-based testing; Sentinel validator ve parser'lar için strategy seçimi, custom strategy tanımı ve shrinking ile hata teşhisi"
---

## Purpose
Manuel test örnekleri yerine Hypothesis'in ürettiği rastgele giriş verisiyle Sentinel doğrulama ve dönüşüm fonksiyonlarının özellik tabanlı garantilerini test etmek.

## Workflow

### Temel Property Testleri
```python
# tests/property/test_validators_property.py
from hypothesis import given, settings, assume, example
from hypothesis import strategies as st
import pytest
from sentinel.validators import validate_duration, parse_promql_labels

# Duration formatı: her geçerli format doğrulanmalı
VALID_UNITS = st.sampled_from(["s", "m", "h", "d"])
VALID_DURATION = st.builds(
    lambda n, u: f"{n}{u}",
    n=st.integers(min_value=1, max_value=99999),
    u=VALID_UNITS
)

@given(duration=VALID_DURATION)
def test_valid_duration_always_passes(duration: str):
    assert validate_duration(duration) is True

@given(st.text())
def test_random_text_rarely_valid(text: str):
    import re
    is_valid = bool(re.match(r'^\d+[smhd]$', text))
    assert validate_duration(text) == is_valid

# Idempotency: parse → serialize → parse aynı sonucu vermeli
@given(st.dictionaries(
    keys=st.text(alphabet=st.characters(whitelist_categories=("Ll",)), min_size=1, max_size=20),
    values=st.text(min_size=0, max_size=50),
    min_size=0,
    max_size=10
))
def test_label_parse_serialize_roundtrip(labels: dict):
    from sentinel.promql import serialize_labels, parse_labels
    assume(all(k.isidentifier() for k in labels))
    
    serialized = serialize_labels(labels)
    parsed = parse_labels(serialized)
    assert parsed == labels
```

### Custom Strategy: PromQL Expression
```python
from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy

def promql_metric_name() -> SearchStrategy[str]:
    return st.from_regex(r'[a-zA-Z_:][a-zA-Z0-9_:]*', fullmatch=True)

def promql_label_value() -> SearchStrategy[str]:
    return st.text(
        alphabet=st.characters(blacklist_characters=['"', '\\']),
        max_size=100
    )

def promql_instant_vector() -> SearchStrategy[str]:
    return st.builds(
        lambda name, labels: f'{name}{{{",".join(f"{k}={chr(34)}{v}{chr(34)}" for k, v in labels.items())}}}',
        name=promql_metric_name(),
        labels=st.dictionaries(
            keys=st.from_regex(r'[a-z_][a-z0-9_]*', fullmatch=True),
            values=promql_label_value(),
            max_size=3
        )
    )

@given(promql_instant_vector())
@settings(max_examples=200)
def test_promql_parser_never_crashes(expr: str):
    from sentinel.promql import parse_expr
    try:
        result = parse_expr(expr)
        assert result is not None
    except ValueError:
        pass  # geçersiz syntax beklenen hata
    # Exception dışında herhangi bir unhandled exception test başarısız olur
```

### Stateful Testing
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, initialize
from hypothesis import settings

class AlertRuleManagerMachine(RuleBasedStateMachine):
    """AlertRule manager'ın stateful property testi"""
    
    def __init__(self):
        super().__init__()
        self.manager = AlertRuleManager()
        self.expected_rules = {}
    
    @initialize(
        name=st.from_regex(r'[a-z][a-z0-9_]{0,30}', fullmatch=True),
        severity=st.sampled_from(["warning", "info"])
    )
    def add_initial_rule(self, name: str, severity: str):
        rule = AlertRule(name=name, expr="up", severity=severity, for_duration="1m")
        self.manager.add(rule)
        self.expected_rules[name] = rule
    
    @rule(name=st.from_regex(r'[a-z][a-z0-9_]{0,30}', fullmatch=True))
    def delete_rule(self, name: str):
        self.manager.delete(name)
        self.expected_rules.pop(name, None)
    
    @invariant()
    def rule_count_matches(self):
        assert len(self.manager.list_all()) == len(self.expected_rules)

TestAlertRuleManager = AlertRuleManagerMachine.TestCase
```

### Shrinking Örneği
```python
# Hypothesis hata bulduğunda minimal örneği gösterir
# "falsifying example: duration='1x'" — geçersiz birim
# shrunk from: duration='99999x' to duration='1x'

@example("0m")  # sınır durum: 0 süresi
@given(VALID_DURATION)
def test_duration_nonzero(duration: str):
    from sentinel.validators import parse_duration_seconds
    result = parse_duration_seconds(duration)
    assert result > 0  # 0m = 0 saniye — bu örnek başarısız olur
```

## Common mistakes
- `assume()` çok agresif kullanmak — geçersiz örnek oranı %50'yi aşarsa Hypothesis `UnsatisfiedAssumption` verir; custom strategy yaz
- `max_examples=10` ile hızlı tutmak — CI'da 200-500 örnek çalıştır; daha fazla yüzey alanı
- Property testini example-based test yerine koymak — ikisi tamamlayıcıdır; birini kaldırma
- Deterministik olmayan kod test etmek — random/time.time() içeren fonksiyon property testinde tutarsız sonuç verir

## References
- `skills/test-mutation`
- `skills/test-unit-fastapi`

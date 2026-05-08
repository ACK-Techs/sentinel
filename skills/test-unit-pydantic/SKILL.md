---
name: test-unit-pydantic
description: "Pydantic model doğrulama birim testi; field validator, model_validator, custom type ve Sentinel veri modellerinin sınır değer testleri"
---

## Purpose
Pydantic model doğrulama mantığını izole birim testleriyle garantilemek; geçersiz veri girişlerinin doğru hata mesajıyla reddedildiğini ve validator zincirinin beklendiği gibi çalıştığını doğrulamak.

## Workflow

### Model Tanımı (Test Edilecek)
```python
# sentinel/models/alert.py
from pydantic import BaseModel, field_validator, model_validator
from typing import Literal
from datetime import datetime

class AlertRule(BaseModel):
    name: str
    expr: str
    severity: Literal["critical", "warning", "info"]
    for_duration: str  # "5m", "1h" formatı
    labels: dict[str, str] = {}
    
    @field_validator("name")
    @classmethod
    def name_must_be_slug(cls, v: str) -> str:
        import re
        if not re.match(r'^[a-z][a-z0-9_-]*$', v):
            raise ValueError("name küçük harf, rakam, _ veya - içermeli ve harf ile başlamalı")
        return v
    
    @field_validator("for_duration")
    @classmethod
    def validate_duration(cls, v: str) -> str:
        import re
        if not re.match(r'^\d+[smhd]$', v):
            raise ValueError("Geçersiz süre formatı: '5m', '1h', '30s' bekleniyor")
        return v
    
    @model_validator(mode="after")
    def critical_must_have_runbook(self) -> "AlertRule":
        if self.severity == "critical" and "runbook_url" not in self.labels:
            raise ValueError("critical alert'ler labels.runbook_url gerektiriyor")
        return self
```

### Birim Testleri
```python
# tests/unit/test_alert_model.py
import pytest
from pydantic import ValidationError
from sentinel.models.alert import AlertRule

class TestAlertRuleValidation:
    
    def test_valid_alert_rule(self):
        rule = AlertRule(
            name="high_error_rate",
            expr="rate(http_errors_total[5m]) > 0.05",
            severity="warning",
            for_duration="5m"
        )
        assert rule.name == "high_error_rate"
        assert rule.severity == "warning"
    
    def test_invalid_name_uppercase(self):
        with pytest.raises(ValidationError) as exc_info:
            AlertRule(name="HighErrorRate", expr="up", severity="info", for_duration="1m")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("name",)
        assert "küçük harf" in errors[0]["msg"]
    
    def test_invalid_name_starts_with_digit(self):
        with pytest.raises(ValidationError) as exc_info:
            AlertRule(name="1alert", expr="up", severity="info", for_duration="1m")
        errors = exc_info.value.errors()
        assert errors[0]["loc"] == ("name",)
    
    def test_invalid_duration_format(self):
        with pytest.raises(ValidationError) as exc_info:
            AlertRule(name="test", expr="up", severity="info", for_duration="5 minutes")
        errors = exc_info.value.errors()
        assert errors[0]["loc"] == ("for_duration",)
    
    def test_critical_without_runbook_fails(self):
        with pytest.raises(ValidationError) as exc_info:
            AlertRule(
                name="service_down",
                expr="up == 0",
                severity="critical",
                for_duration="1m"
            )
        # model_validator hatası
        assert any("runbook_url" in e["msg"] for e in exc_info.value.errors())
    
    def test_critical_with_runbook_passes(self):
        rule = AlertRule(
            name="service_down",
            expr="up == 0",
            severity="critical",
            for_duration="1m",
            labels={"runbook_url": "https://runbooks.example.com/service-down"}
        )
        assert rule.severity == "critical"
    
    @pytest.mark.parametrize("duration", ["1s", "30m", "2h", "7d"])
    def test_valid_duration_formats(self, duration):
        rule = AlertRule(name="test", expr="up", severity="info", for_duration=duration)
        assert rule.for_duration == duration
    
    @pytest.mark.parametrize("invalid", ["5 min", "1hour", "m5", ""])
    def test_invalid_duration_formats(self, invalid):
        with pytest.raises(ValidationError):
            AlertRule(name="test", expr="up", severity="info", for_duration=invalid)
```

### Model Serialization Testi
```python
def test_model_json_roundtrip():
    original = AlertRule(
        name="test_rule",
        expr="up == 1",
        severity="warning",
        for_duration="5m",
        labels={"team": "platform"}
    )
    serialized = original.model_dump_json()
    restored = AlertRule.model_validate_json(serialized)
    assert original == restored

def test_model_dict_excludes_none():
    rule = AlertRule(name="test", expr="up", severity="info", for_duration="1m")
    d = rule.model_dump(exclude_none=True)
    assert "labels" in d  # default değer var
```

## Common mistakes
- `ValidationError.errors()` yerine `str(exc_info.value)` ile hata mesajı kontrol etmek — `loc` ve `type` alanlarını kaçırırsın
- `model_validator(mode="after")` içinde field'lara `self.` ile erişmeyi unutmak — `mode="before"` ile dict alırsın
- Parametrize testlerde tek bir hatalı case olunca tüm test seti başarısız gibi görünmek — `pytest.mark.parametrize` hataları ayrı ID'de gösterir, oku
- Pydantic V1 `@validator` ile V2 `@field_validator` karıştırmak — Sentinel V2 kullanıyor, decorator imzaları farklı

## References
- `skills/test-unit-fastapi`
- `skills/python-dataclass-pydantic`

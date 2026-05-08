---
name: fastapi-pydantic-v2
description: "Pydantic v2 ile FastAPI entegrasyonu ve migration — Sentinel model katmanının v2 uyumluluğu"
---

## Purpose
Pydantic v2, v1'e göre 5-50x daha hızlı validasyon sunar ama API'de breaking change'ler içerir. Sentinel'in model katmanı v2'ye geçirilmiştir; bu skill migration rehberini, v2 idiom'larını ve FastAPI'yle entegrasyon püf noktalarını içerir.

## Workflow

### 1. V1 → V2 temel değişiklikler

```python
# V1 (eski):
from pydantic import BaseModel, validator
from typing import Optional, List

class TraceV1(BaseModel):
    id: str
    spans: Optional[List[str]] = None

    @validator("id")
    def validate_id(cls, v):
        if not v.startswith("trace-"):
            raise ValueError("ID must start with 'trace-'")
        return v

    class Config:
        orm_mode = True

# V2 (yeni):
from pydantic import BaseModel, field_validator, model_validator
from pydantic import ConfigDict

class Trace(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # orm_mode yerine

    id: str
    spans: list[str] | None = None  # Optional[List] yerine

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v.startswith("trace-"):
            raise ValueError("ID must start with 'trace-'")
        return v
```

### 2. model_validator ile çapraz alan doğrulama

```python
from pydantic import model_validator
from typing import Self

class TimeRange(BaseModel):
    start: datetime
    end: datetime
    step: str = "60s"

    @model_validator(mode="after")
    def validate_range(self) -> Self:
        if self.end <= self.start:
            raise ValueError("end, start'tan sonra olmalı")
        if (self.end - self.start).total_seconds() > 86400:
            raise ValueError("Maksimum 24 saatlik aralık sorgulanabilir")
        return self
```

### 3. Computed field ve serialization

```python
from pydantic import computed_field, AliasChoices, Field

class SpanResponse(BaseModel):
    span_id: str = Field(validation_alias=AliasChoices("spanId", "span_id"))
    duration_ns: int
    service_name: str

    @computed_field
    @property
    def duration_ms(self) -> float:
        return self.duration_ns / 1_000_000

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": {"span_id": "abc123", "duration_ns": 5000000}},
    )
```

### 4. Discriminated union (polymorphic response)

```python
from typing import Annotated, Literal
from pydantic import Discriminator

class MetricAlert(BaseModel):
    type: Literal["metric"] = "metric"
    metric_name: str
    threshold: float

class TraceAlert(BaseModel):
    type: Literal["trace"] = "trace"
    trace_id: str
    latency_ms: float

AlertEvent = Annotated[
    MetricAlert | TraceAlert,
    Discriminator("type"),
]

class AlertFiredEvent(BaseModel):
    event: AlertEvent
    fired_at: datetime
```

### 5. Performans optimizasyonu

```python
# model_rebuild: schema önbelleğe al
Trace.model_rebuild()

# TypeAdapter: model instance olmadan validasyon
from pydantic import TypeAdapter
ta = TypeAdapter(list[Trace])
traces = ta.validate_python(raw_data)  # Model oluşturmadan batch validasyon

# model_validate ile ORM
trace = Trace.model_validate(orm_obj)
```

## Common mistakes

- `@validator` decorator'ını v2'de kullanmak — deprecated, `@field_validator` kullan
- `dict()` yerine `model_dump()` kullanmamak — v2'de `dict()` deprecated
- `.json()` yerine `model_dump_json()` kullanmamak — v2 serialization farkı
- `orm_mode = True` yerine `from_attributes=True` unutmak — ORM nesneleri parse edilemez

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-exception-handlers`
- `skills/python-mypy-strict`

---
name: python-mypy-strict
description: "mypy strict mode ve type: ignore yönetimi — Sentinel tip güvenliği için statik analiz yapılandırması"
---

## Purpose
mypy strict mode, Sentinel servislerinde runtime tip hatalarını geliştirme aşamasında yakalar. `Any` tipinin sızmasını engeller, eksik dönüş tiplerini zorunlu kılar ve üçüncü parti kütüphane stubs'larının doğru yapılandırılmasını sağlar. `# type: ignore` yönetimi disiplinli tutulmazsa tip güvenliği erimeden kaybolur.

## Workflow

### 1. mypy.ini / pyproject.toml yapılandırması

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
# strict şunları açar:
# --disallow-any-generics, --disallow-subclassing-any
# --disallow-untyped-calls, --disallow-untyped-defs
# --disallow-incomplete-defs, --check-untyped-defs
# --disallow-untyped-decorators, --warn-redundant-casts
# --warn-unused-ignores, --warn-return-any
# --no-implicit-reexport, --strict-equality

warn_unreachable = true
show_error_codes = true
pretty = true

# Stubs olmayan kütüphaneler için
[[tool.mypy.overrides]]
module = [
    "structlog.*",
    "prometheus_client.*",
    "opentelemetry.*",
]
ignore_missing_imports = true
```

### 2. Yaygın tip hatası kalıpları ve çözümleri

```python
# Hata: Return type missing
def get_config():  # error: Function is missing a return type annotation
    return {"key": "value"}

# Düzeltme:
def get_config() -> dict[str, str]:
    return {"key": "value"}

# Hata: Optional kullanımı
def find_trace(trace_id: str) -> Trace:
    result = db.query(trace_id)
    return result  # error: Incompatible return value type (got "Trace | None")

# Düzeltme:
def find_trace(trace_id: str) -> Trace | None:
    return db.query(trace_id)

# Hata: TypedDict ile dict birleştirme
from typing import TypedDict

class TraceMetadata(TypedDict):
    service: str
    duration_ms: int

def enrich(meta: TraceMetadata, extra: dict[str, str]) -> TraceMetadata:
    return {**meta, **extra}  # error: extra anahtarları TypedDict'te yok

# Düzeltme: TypedDict genişlet ya da Union kullan
```

### 3. Generic sınıflar

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(Generic[T]):
    def get(self, id: str) -> T | None: ...
    def list(self, **filters: str) -> list[T]: ...
    def save(self, entity: T) -> T: ...

class TraceRepository(Repository["Trace"]):
    def get(self, id: str) -> "Trace | None":
        return self._db.find(Trace, id)
```

### 4. `type: ignore` disiplinli yönetimi

```python
# Kötü — neden ignore ettiği belli değil
result = legacy_function()  # type: ignore

# İyi — hata kodu ve gerekçe
result = legacy_function()  # type: ignore[no-untyped-call]  # TODO: stubs PR #123

# Belirli modül override (mypy.ini'de):
[[tool.mypy.overrides]]
module = "sentinel.legacy.*"
ignore_errors = true  # legacy modül, type migration Q3'te planlandı
```

### 5. CI entegrasyonu

```bash
# Sadece değişen dosyaları kontrol et
mypy --ignore-missing-imports src/

# Tüm proje
mypy src/ --html-report reports/mypy/
```

## Common mistakes

- `from __future__ import annotations` ile runtime type check birleştirmek — `isinstance(x, SomeType)` forward reference'larla çalışmaz
- `--ignore-missing-imports` global açmak — spesifik override'lar ile yönet
- `warn_unused_ignores = true` olmadan çalışmak — eski `# type: ignore` satırları birikerek gürültü yaratır
- Protocol'ü ABC yerine kullanmamak — `isinstance` kontrolü gerekmeyen durumlarda Protocol daha esnek

## References
- `skills/python-ruff-lint`
- `skills/python-pre-commit`
- `skills/fastapi-pydantic-v2`

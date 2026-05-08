---
name: python-ruff-lint
description: "ruff ile Python linting ve otomatik format düzeltme — Sentinel kod kalitesi ve CI gate için"
---

## Purpose
ruff, flake8 + isort + pyupgrade + black'ı tek araçta birleştirir ve Rust tabanlı hızıyla CI pipeline'da milisaniyelerde çalışır. Sentinel'de hem linting hem formatting için ruff kullanılır; black ve flake8 artık bağımlılık listesinde yoktur.

## Workflow

### 1. pyproject.toml yapılandırması

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
    "RUF", # ruff-specific rules
]
ignore = [
    "E501",  # line-length — formatter halleder
    "B008",  # FastAPI Depends() için gerekli
]

[tool.ruff.lint.isort]
known-first-party = ["sentinel_sdk", "app"]
combine-as-imports = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true
```

### 2. Temel kullanım

```bash
# Lint kontrolü (hata varsa exit 1)
ruff check src/

# Otomatik düzeltme
ruff check --fix src/

# Format kontrolü
ruff format --check src/

# Format uygula
ruff format src/

# Tek dosya, tüm kontroller
ruff check --fix --format-errors src/app/main.py
```

### 3. Önemli kurallar ve açıklamalar

```python
# B006: Mutable default argument
# Kötü:
def add_tag(name: str, tags: list = []):
    tags.append(name)
    return tags

# İyi:
def add_tag(name: str, tags: list | None = None):
    if tags is None:
        tags = []
    tags.append(name)
    return tags

# UP006: Use `list` instead of `List`
# Kötü (Python < 3.9 kalıntısı):
from typing import List, Dict, Optional
def foo(items: List[str]) -> Optional[Dict[str, int]]: ...

# İyi:
def foo(items: list[str]) -> dict[str, int] | None: ...

# TCH001: typing-only imports TYPE_CHECKING bloğuna
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sentinel.models import Trace
```

### 4. Pre-commit entegrasyonu

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.7
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### 5. CI gate (GitHub Actions)

```yaml
- name: Lint & Format check
  run: |
    ruff check src/ tests/
    ruff format --check src/ tests/
```

### 6. noqa direktifi

```python
import os  # noqa: F401 — re-exported for public API
result = dangerous_function()  # noqa: B006
```

## Common mistakes

- `ruff check` ile `ruff format` sırasını yanlış kurmak — önce format, sonra lint çalıştır; lint düzeltmeleri format bozabilir
- `ignore = ["E501"]` eklemeden `line-length` ayarlamak — formatlama ve lint çelişir
- `--fix` bayrağını CI'da kullanmak — CI sadece kontrol etmeli, otomatik commit yapmamalı
- `TCH` kurallarını `TYPE_CHECKING` bloğu olmadan aktifleştirmek — runtime import hataları çıkar

## References
- `skills/python-pre-commit`
- `skills/python-mypy-strict`
- `skills/python-docstring-standard`

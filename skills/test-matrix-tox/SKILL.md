---
name: test-matrix-tox
description: "tox ile Sentinel için çoklu Python sürümü test matrisi; py310/py311/py312 karşılaştırması, linting entegrasyonu ve GitHub Actions matrix stratejisi"
---

## Purpose
Sentinel'in Python 3.10, 3.11 ve 3.12'de doğru çalıştığını garanti etmek; tek komutla tüm ortamları test etmek ve CI'da matrix paralel çalıştırma.

## Workflow

### tox.ini Konfigürasyonu
```ini
[tox]
envlist = py310, py311, py312, lint, type
isolated_build = true

[testenv]
deps =
    pytest>=7.4
    pytest-asyncio>=0.21
    pytest-cov>=4.0
    httpx>=0.25
    respx>=0.20
commands =
    pytest tests/unit/ tests/integration/ \
        --cov=sentinel \
        --cov-report=term-missing \
        --cov-fail-under=80 \
        -v {posargs}

[testenv:lint]
deps =
    ruff>=0.1
    black>=23.0
commands =
    ruff check sentinel/ tests/
    black --check sentinel/ tests/

[testenv:type]
deps =
    mypy>=1.6
    types-all
commands =
    mypy sentinel/ --strict --ignore-missing-imports

[testenv:docs]
deps = mkdocs-material
commands = mkdocs build

[gh-actions]
python =
    3.10: py310
    3.11: py311
    3.12: py312
```

### GitHub Actions Matrix
```yaml
# .github/workflows/test-matrix.yml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
      fail-fast: false  # bir sürüm başarısız olursa diğerleri devam eder
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install tox
        run: pip install tox tox-gh-actions
      
      - name: Run tox
        run: tox
        env:
          PYTHON_VERSION: ${{ matrix.python-version }}
      
      - name: Upload coverage (only py312)
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          file: .tox/py312/tmp/coverage.xml

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install tox
      - run: tox -e lint
```

### pyproject.toml ile Modern tox
```toml
# pyproject.toml (tox 4+ native konfigürasyon)
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py310,py311,py312,lint
"""
```

### Lokal Matrix Çalıştırma
```bash
# Tüm ortamlar
tox

# Sadece belirli Python sürümleri
tox -e py311,py312

# Paralel çalıştır
tox -p auto

# Sadece linting
tox -e lint

# Belirli test dosyası
tox -e py312 -- tests/unit/test_validators.py -v
```

### Versiyon Uyumsuzluğu Tespiti
```python
# sentinel/_compat.py — Python versiyon farklılıklarını merkezde yönet
import sys

if sys.version_info >= (3, 11):
    from tomllib import loads as toml_loads
else:
    from tomli import loads as toml_loads  # backport

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override
```

## Common mistakes
- `isolated_build = false` bırakmak — farklı ortamlarda farklı bağımlılıklar yüklü kalabilir
- `tox -e py312` çalıştırırken diğer ortamları test etmemek — matrix purpose'u bu; tüm liste çalıştır
- Lint ortamını test envisi ile karıştırmak — ayrı `[testenv:lint]` bloğu daha hızlı
- `{posargs}` eklemeden tox çalıştırmak — özel test argümanı geçilemez; `tox -e py312 -- -k test_specific`

## References
- `skills/test-coverage-reporting`
- `skills/python-virtualenv-uv`

---
name: python-packaging-wheel
description: "Python wheel paketi oluşturma ve PyPI yayınlama — Sentinel SDK ve CLI araçlarının dağıtımı için"
---

## Purpose
Sentinel'in istemci SDK'sı ve CLI aracı Python wheel olarak paketlenip iç PyPI registry'ye veya PyPI'ye yayınlanır. Bu skill `pyproject.toml` tabanlı modern paketleme (PEP 517/518), wheel build süreci ve Trusted Publisher ile güvenli PyPI yayınlamayı kapsar.

## Workflow

### 1. pyproject.toml yapılandırması

```toml
# pyproject.toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "sentinel-sdk"
version = "0.4.2"
description = "Sentinel observability platform Python SDK"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "Apache-2.0" }
authors = [{ name = "Sentinel Team", email = "platform@example.com" }]

dependencies = [
    "httpx>=0.27",
    "pydantic>=2.7",
    "structlog>=24.1",
    "typer[all]>=0.12",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-asyncio>=0.23", "ruff", "mypy"]

[project.scripts]
sentinel = "sentinel_sdk.cli.main:app"

[project.urls]
Homepage = "https://github.com/sentinel/sentinel-sdk"
Changelog = "https://github.com/sentinel/sentinel-sdk/blob/main/CHANGELOG.md"

[tool.hatch.build.targets.wheel]
packages = ["src/sentinel_sdk"]

[tool.hatch.version]
source = "vcs"
```

### 2. Wheel build ve doğrulama

```bash
# Build
python -m pip install build twine
python -m build

# Çıktı doğrulama
ls dist/
# sentinel_sdk-0.4.2-py3-none-any.whl
# sentinel_sdk-0.4.2.tar.gz

# Twine check (metadata doğrulama)
twine check dist/*

# Wheel içeriğini incele
python -m zipfile -l dist/sentinel_sdk-0.4.2-py3-none-any.whl
```

### 3. GitHub Actions ile otomatik yayınlama

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Trusted Publisher için
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # hatch-vcs için tag geçmişi

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install build
      - run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # Trusted Publisher: token gerekmez
```

### 4. İç registry (Artifactory/Nexus) yayınlama

```bash
# ~/.pypirc
[distutils]
index-servers = internal

[internal]
repository = https://registry.internal/simple/
username = __token__
password = <ARTIFACTORY_TOKEN>

# Yayınla
twine upload --repository internal dist/*

# Kullanım
pip install --index-url https://registry.internal/simple/ sentinel-sdk
```

### 5. Versiyon yönetimi (CalVer)

```toml
# hatch-calver kullanımı
[tool.hatch.version]
source = "calver"
scheme = "YYYY.MM.DD"
```

## Common mistakes

- `setup.py` ile `pyproject.toml` karıştırmak — ikisi birden varsa build backend karışır
- `packages` yerine `py_modules` tanımlamak — tek modüllü paketlerde bile `packages` kullan
- `version = "vcs"` ile tag olmadan build almak — `0.0.0.dev0+dirty` gibi versiyon üretir, CI'da tag oluştur
- `twine check` atlamak — PyPI description render hataları yayın sonrası fark edilir

## References
- `skills/python-pre-commit`
- `skills/python-ruff-lint`
- `skills/python-dependency-pinning`

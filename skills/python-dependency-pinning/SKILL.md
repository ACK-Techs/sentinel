---
name: python-dependency-pinning
description: "Bağımlılık sabitleme stratejisi (pip-compile, uv lock) — Sentinel servislerinde tekrarlanabilir build için"
---

## Purpose
"Bende çalışıyor" sorununu ortadan kaldırmak için tüm doğrudan ve geçişli bağımlılıkların hash ile sabitlenmesi gerekir. Sentinel'de `uv` tercih edilir; legacy ortamlarda `pip-tools` (pip-compile) kullanılır. `pyproject.toml` soyut bağımlılıkları tanımlar, lock dosyası somut versiyonları sabitler.

## Workflow

### 1. uv ile lock dosyası yönetimi

```bash
# uv.lock oluştur / güncelle
uv lock

# Lock dosyasına uygun kurulum
uv sync

# Belirli grubu dahil et
uv sync --group dev

# Tek bağımlılığı güncelle
uv lock --upgrade-package httpx

# Tüm bağımlılıkları güncelle
uv lock --upgrade

# Sanal ortam oluştur ve kur
uv venv && uv sync
```

### 2. pip-tools ile lock (legacy)

```bash
# requirements.in — soyut bağımlılıklar
# requirements.txt — somut (hash dahil)

# Compile
pip-compile \
    --generate-hashes \
    --output-file requirements.txt \
    pyproject.toml

# Dev bağımlılıkları
pip-compile \
    --generate-hashes \
    --extra dev \
    --output-file requirements-dev.txt \
    pyproject.toml

# Güncelle
pip-compile --upgrade requirements.txt

# Kur
pip install --require-hashes -r requirements.txt
```

### 3. pyproject.toml — sürüm kısıtlama stratejisi

```toml
[project]
dependencies = [
    # Lower bound: breaking change riski
    "httpx>=0.27,<1.0",
    # Exact: kritik güvenlik kütüphanesi
    "cryptography==42.0.8",
    # Compatible release: minor güncellemeler kabul
    "structlog~=24.1",
    # Üst sınırsız: iç kütüphane
    "sentinel-sdk>=0.4",
]
```

### 4. Güvenlik açığı tarama

```bash
# pip-audit ile CVE tarama
pip-audit -r requirements.txt --fix

# uv ile
uv pip audit

# GitHub Actions
- uses: pypa/gh-action-pip-audit@v1.0.8
  with:
    inputs: requirements.txt
```

### 5. Dependabot yapılandırması

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      observability:
        patterns: ["opentelemetry-*", "prometheus-*"]
    ignore:
      - dependency-name: "cryptography"
        update-types: ["version-update:semver-major"]
```

## Common mistakes

- Lock dosyasını git'e commit etmemek — farklı makinelerde farklı sürümler kurulur
- Hash olmadan `requirements.txt` kullanmak — supply chain saldırısına açık
- `~=` (compatible release) ile major versiyon atlayan kütüphaneler kullanmak — breaking change gelebilir
- `uv.lock` ile `requirements.txt` birlikte güncel tutmaya çalışmak — ikisinden birini seç, ikisi birden senkronize edilmez

## References
- `skills/python-packaging-wheel`
- `skills/python-pre-commit`
- `skills/python-secrets-runtime`

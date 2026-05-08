---
name: python-pre-commit
description: "pre-commit hook'ları ve CI entegrasyonu — Sentinel'de her commit öncesi kod kalitesi otomasyonu"
---

## Purpose
pre-commit, `git commit` tetiklendiğinde belirlenen araçları sırayla çalıştırır ve başarısız hook commit'i engeller. Sentinel projelerinde ruff, mypy, pytest (smoke), secret scan ve trailing whitespace gibi kontroller bu sistemle çalışır; geliştirici IDE'sinden bağımsız asgari standartları zorunlu kılar.

## Workflow

### 1. .pre-commit-config.yaml

```yaml
# .pre-commit-config.yaml
repos:
  # Temel dosya temizliği
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key

  # Ruff lint + format
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.7
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Mypy tip kontrolü
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.7
          - types-PyYAML
        args: [--config-file=pyproject.toml]

  # Secret tarama
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]
        exclude: tests/fixtures/
```

### 2. Kurulum ve başlatma

```bash
# Kurulum
pip install pre-commit

# Hook'ları git'e yükle
pre-commit install

# İlk kez tüm dosyaları kontrol et
pre-commit run --all-files

# Belirli hook
pre-commit run ruff --all-files

# Hook versiyonlarını güncelle
pre-commit autoupdate
```

### 3. Belirli dosyayı atla (acil durum)

```bash
# Tüm hook'ları atla — PRODUCTION'DA KULLANMA
git commit --no-verify -m "hotfix: kritik"

# Belirli dosyayı hook'tan hariç tut
# .pre-commit-config.yaml içinde:
hooks:
  - id: mypy
    exclude: "^src/legacy/|^migrations/"
```

### 4. CI entegrasyonu

```yaml
# .github/workflows/pre-commit.yml
name: pre-commit

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: pre-commit/action@v3.0.1
        with:
          extra_args: --all-files
```

### 5. secrets.baseline oluşturma

```bash
# detect-secrets baseline oluştur
detect-secrets scan > .secrets.baseline

# Bilinen sır varsa kabul et
detect-secrets audit .secrets.baseline

# git'e ekle
git add .secrets.baseline
```

## Common mistakes

- `pre-commit install` yapmadan repoya push etmek — CI'da pre-commit hook'ları çalışmaz
- `.pre-commit-config.yaml`'da rev olarak `main`/`master` kullanmak — floating tag, reproducible değil
- mypy hook için `additional_dependencies` belirtmemek — hook izole venv'de çalışır, ana bağımlılıkları görmez
- `--exit-non-zero-on-fix` olmadan ruff kullanmak — ruff fix yaptığında commit geçer ama staged olmayan değişiklikler kalır

## References
- `skills/python-ruff-lint`
- `skills/python-mypy-strict`
- `skills/python-secrets-runtime`

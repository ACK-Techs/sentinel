---
name: agentic-ci-github-actions
description: PR pipeline için format, lint, test, önbellek ve Python sürüm matrisi iskeleti tanımlarken kullan.
---

## Amaç

**PR pipeline**: checkout → (isteğe bağlı) `uv`/`pip` cache → **ruff** veya seçilen linter → **pytest** → (isteğe bağlı) tip kontrolü. **Python matrisi**: desteklenen 3.10–3.12 gibi (`pyproject.toml` ile uyumlu). **Fork PR**: gizli değişkenler yok varsayımı — secret gerektiren adımlar `if: github.event.pull_request.head.repo.fork` ile atlanmalı veya `pull_request_target` kullanılmamalı (güvenlik).

## Kapsam

### Dahil

- Örnek `.github/workflows/ci.yml` iskeleti (yorum satırlarıyla açıklamalı).
- Başarısız adımda artefact (log) yükleme önerisi.

### Hariç

- Release imzalama ve PyPI otomasyonu (ayrı workflow).

## Kurallar

- `main` push ve PR tetikleyicileri ayrımı dokümante.
- Cache key: lock dosyası hash.
- API anahtarı CI’da asla düz metin yok.

## Kontrol listesi

- [ ] Fork PR güvenli mi?
- [ ] Matrix’te tüm desteklenen sürümler yeşil mi?
- [ ] Süre < 10 dk hedefi (veya proje bütçesi)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Cache bozuk | key | Cache bust |
| Lint fail | auto-fix | `ruff check --fix` yerel |

## İlgili belgeler ve skill'ler

- `../agentic-packaging-pypi/SKILL.md`
- `../agentic-testing-unit/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`

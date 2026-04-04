# Faz 3 — Skill ve dokümantasyon indeksi

**Amaç:** Faz 3’te hangi **yeni skill** eklendi, hangi **mevcut skill** kullanılıyor, hangi **dosyalar** doğruluk kaynağı — tek sayfada.

## Yeni agentic skill’ler (`cli/skills/`)

| Skill | Dosya | Ne için |
|-------|--------|---------|
| `agentic-wheel-build-verify` | `agentic-wheel-build-verify/SKILL.md` | Wheel/sdist build + temiz venv smoke |
| `agentic-docs-developer-checklist` | `agentic-docs-developer-checklist/SKILL.md` | CONTRIBUTING / ruff / pytest hizası |
| `agentic-faz3-no-remote-telemetry` | `agentic-faz3-no-remote-telemetry/SKILL.md` | Uzaktan telemetri kodu eklenmemesi |

## Mevcut skill’ler (Faz 3’te doğrudan referans)

| Skill | Faz 3 bağlantısı |
|-------|------------------|
| `agentic-packaging-pypi` | pyproject, entry point, kurulum dokümanı |
| `agentic-feature-flags` | `SENTINEL_*` / deneysel bayrak tablosu |
| `agentic-secrets-handling` | `.env.example`, doctor sızdırmazlık |
| `agentic-cli-user-errors` | Hata mesajı gözden geçirme |
| `agentic-approval-policy-design` | README / mimari ile onay politikası tutarlılığı |
| `agentic-ci-github-actions` | CI ve yerel komut uyumu |
| `agentic-testing-unit`, `agentic-testing-integration-mock-llm` | Test genişletme |

## Dokümantasyon dosyaları

| Dosya | Rol |
|-------|-----|
| `IMPLEMENTATION_PLAN_PHASE3.md` | Ayrıntılı faz planı ve kapı tanımları |
| `CODEX_EXECUTION_PROMPT_PHASE3.md` | Tek mesajda Codex yürütme prompt’u |
| `ROADMAP_PHASE3_5.md` | Üst seviye yol haritası |
| `../CHANGELOG.md` | Sürüm notları |
| `../CONTRIBUTING.md` | Geliştirici komutları |
| `../README.md` | Ana giriş (Faz 3 sonunda güncellenmiş olmalı) |
| `ENV_FLAGS_PHASE3.md` | `SENTINEL_*` ve ilgili env tablosu |
| `CODEX_EXECUTION_PROMPT_PHASE3.md` | Tek mesajda Codex yürütme talimatı |
| `archive/README.md` | Faz 2 arşivi; Faz 3 tamamlanınca tarih notu eklenebilir |

## Katalog güncellemesi

Yeni skill’ler `SKILL_CATALOG_PHASE2.md` içinde **Faz 3 ekleri** bölümüne işlendi (kimlik listesi).

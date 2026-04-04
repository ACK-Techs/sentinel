---
name: agentic-docs-developer-checklist
description: Katkı öncesi ruff/pytest komutları ve PR kontrol listesi yazarken kullan.
---

## Amaç

`CONTRIBUTING.md` veya README içinde **tek blokta** görülebilen: sanal ortam, `ruff check`, `pytest`, isteğe bağlı `ruff format` ve dal/PR kuralları. Amaç: iç kullanım ve küçük ekip için **tekrarlanabilir kalite çubuğu**.

## Kapsam

### Dahil

- Çalışma dizini: `sentinel-coming/cli/`.
- Minimum komutlar: `python -m ruff check .`, `python -m pytest -q`.
- Secret ve fixture: testlerde gerçek API anahtarı yok.

### Hariç

- Kurumsal CLA veya dış katkıcı hukuku (iç kullanım).

## Kurallar

- Komutlar **kopyala-yapıştır** ile çalışır olmalı; `$(pwd)` kabuk bağımlılığı varsa not düş.
- CI varsa yerel komutlar CI ile aynı hedefi taşımalı (sürüm farkı dokümante).

## Kontrol listesi

- [ ] README’de CONTRIBUTING’e link var mı?
- [ ] Yeni geliştirici 5 dakikada lint+test koşturabildi mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Ruff bulunamadı | `[dev]` extra | `pip install -e ".[dev]"` |
| pytest koleksiyonu boş | `testpaths` | `pyproject.toml` |

## İlgili belgeler ve skill'ler

- `../../CONTRIBUTING.md` (varsa)
- `../agentic-testing-unit/SKILL.md`
- `../agentic-ci-github-actions/SKILL.md`
- `../../documantations/IMPLEMENTATION_PLAN_PHASE3.md`

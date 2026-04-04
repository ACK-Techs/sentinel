---
name: agentic-testing-unit
description: Birim test dizin yapısı, fixture ve sağlayıcı mock sınırını tanımlarken kullan.
---

## Amaç

Dizin: örn. `tests/` veya `src/.../tests` (repo ile tutarlı). **Fixture’lar**: geçici dizin, sahte config, mock HTTP. **Mock sınırı**: LLM istemcisi arayüz seviyesinde mock; ağa çıkmayan hızlı testler. **Kapsam hedefi**: yumuşak öneri — kritik modüller (`config merge`, `tool parse`, `provider adapter`) için yüksek oran; kesin % proje kararı.

## Kapsam

### Dahil

- pytest marker’ları: `slow`, `integration`.
- Coverage opsiyonel (`pytest-cov`).

### Hariç

- E2E gerçek API testi (maliyetli; ayrı skill).

## Kurallar

- Testler deterministik tarih/saat için `freezegun` veya inject clock (proje kararı).
- Secret fixture’da yok.
- Windows/Linux path farkı için `pathlib`.

## Kontrol listesi

- [ ] CI’da `pytest -q` yeşil mi?
- [ ] Flaky test işaretli ve izole mi?
- [ ] Mock gerçek şemayı yansıtıyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Import hata | PYTHONPATH | `pyproject.toml` test yolu |
| Mock sızıntısı | patch scope | fixture kapsamını daralt |

## İlgili belgeler ve skill'ler

- `../agentic-testing-integration-mock-llm/SKILL.md`
- `../agentic-ci-github-actions/SKILL.md`
- `../agentic-llm-provider-contract/SKILL.md`

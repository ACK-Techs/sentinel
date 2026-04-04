---
name: agentic-packaging-pypi
description: pyproject.toml, konsol entry point, sürümleme ve uv/pip kurulum dokümantasyonunu hazırlarken kullan.
---

## Amaç

**`pyproject.toml`**: proje meta, bağımlılıklar, **`[project.scripts]`** ile CLI adı → modül fonksiyonu. **Build backend**: `hatchling` veya `setuptools` (proje kararı); bu skill örnekleri her ikisine atıfta bulunabilir. **Sürümleme**: semver + tag ile hizalama önerisi. **Kurulum**: `pip install -e .` veya `uv sync` dokümantasyonu `../agentic-docs-user-quickstart` ile bağlantılı.

## Kapsam

### Dahil

- Paket adı, Python sürüm kısıtı, isteğe bağlı extra’lar.
- Dağıtım öncesi `ruff`/`pytest` ile CI hizası (`agentic-ci-github-actions`).

### Hariç

- PyPI hesap yönetimi ve 2FA prosedürü (dış süreç).

## Kurallar

- Entry point adı `agentic-cli-entrypoint` skill’indeki komut adı ile aynı olmalı.
- `README` kök veya `cli/README` kurulum bölümü güncel.
- İsteğe bağlı: `twine` upload adımları genel uyarı ile (secret `.pypirc`).

## Kontrol listesi

- [ ] `pip install .` temiz venv’de çalışıyor mu?
- [ ] CLI `--help` import hatası vermiyor mu?
- [ ] Sürüm tek kaynakta mı (`__version__` veya `toml`)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Entry point bulunamadı | script path | `packages` alanı |
| Bağımlılık çakışması | constraints | `uv lock` / pin |

## İlgili belgeler ve skill'ler

- `../agentic-repo-layout/SKILL.md`
- `../agentic-ci-github-actions/SKILL.md`
- `../agentic-docs-user-quickstart/SKILL.md`
- `../agentic-dependency-licensing/SKILL.md`

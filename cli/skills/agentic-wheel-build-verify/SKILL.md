---
name: agentic-wheel-build-verify
description: Hatch ile wheel/sdist üretip temiz venv’de kurarak CLI’nin çalıştığını doğrularken kullan.
---

## Amaç

`pyproject.toml` içinde **hatchling** build backend varken **`python -m build`** (veya `hatch build`) ile **wheel** ve **sdist** üretmek; ardından **yeni bir sanal ortamda** yalnızca wheel’den `pip install` ederek `sentinel-cli --help` ve mümkünse `version` komutunun hatasız çalıştığını kanıtlamak. Bu, “paket dışarıdan kurulabilir mi?” sorusunun pratik cevabıdır.

## Kapsam

### Dahil

- `build` paketinin dev bağımlılıkta veya tek seferlik kurulumda tanımlanması.
- `dist/` çıktısı; `.gitignore` ile uyum (genelde `dist/` ignore).
- Başarısız import / eksik `packages` düzeltmesi için kontrol listesi.

### Hariç

- PyPI’ye yükleme, imzalama, `twine` (ayrı süreç).

## Kurallar

- Doğrulama **editable install değil**, mümkünse **wheel dosyasından** kurulum ile yapılır.
- Temiz venv: `python -m venv .venv-smoke && source .../activate` gibi; mevcut geliştirme venv’i ile karıştırma.

## Kontrol listesi

- [ ] `python -m build` (veya eşdeğeri) hatasız bitti mi?
- [ ] `pip install dist/sentinel_cli-*.whl` (sürüme göre isim) sonrası `sentinel-cli --help` çalışıyor mu?
- [ ] Konsol script adı `pyproject.toml` `[project.scripts]` ile uyumlu mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Modül bulunamadı | `[tool.hatch.build.targets.wheel] packages` | `src/` yapısı ile hizala |
| Yanlış wheel | Eski `dist/` | `dist/` temizle, yeniden build |

## İlgili belgeler ve skill'ler

- `../agentic-packaging-pypi/SKILL.md`
- `../../documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md`
- `../agentic-ci-github-actions/SKILL.md`

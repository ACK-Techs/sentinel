---
name: agentic-repo-layout
description: Sentinel-coming içinde Faz 2 CLI paketinin dizin ağacını ve Faz 1 ile ilişkisini netleştirirken kullan.
---

## Amaç

Önerilen yerleşim: uygulama kökü **`sentinel-coming/cli/`** altında (kaynak `src/` veya proje kararına göre paket dizini, testler, örnek `.env.example`, `pyproject.toml`). Üst seviye `sentinel-coming/documantations/` ve `sentinel-coming/skills/` **Faz 1 (COS)**; `cli/documantations/` ve `cli/skills/agentic-*` **Faz 2** meta ve skill’leridir.

## Kapsam

### Dahil

- CLI paketi, test klasörü, örnek yapılandırma dosyalarının konumu.
- Faz 1 / Faz 2 path ayrımının dokümantasyon ve skill yollarına yansıması.

### Hariç

- Faz 1 skill dosyalarının taşınması veya yeniden adlandırılması (`../../skills/` dokunma).

## Kurallar

- Yeni kod: `cli/` altında toplanır; kök README’de Faz 1/2 yönlendirmesi okunabilir olmalı.
- Skill göreli yolları: Faz 2 skill içinden belge → `../documantations/`; Faz 1 → `../../documantations/`, `../../skills/<id>/SKILL.md`.
- `pyproject.toml` entry point adı ürün kararıdır; `agentic-packaging-pypi` ile hizala.

## Kontrol listesi

- [ ] `cli/documantations/` ve `cli/skills/` var mı ve isimlendirme katalogla uyumlu mu?
- [ ] Örnek env/config örnekleri repoda secret içermiyor mu?
- [ ] Testler CI’da keşfedilebilir dizinde mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Yanlış import yolu | Paket kökü `cli/` mı? | `pyproject.toml` `packages` alanını düzelt |
| Faz 1 skill yanlışlıkla kopyalandı | `git status` | Yalnız `cli/skills/agentic-*` kullan |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../documantations/IMPLEMENTATION_PLAN_PHASE2.md`
- `../agentic-packaging-pypi/SKILL.md`
- `../agentic-config-layers/SKILL.md`

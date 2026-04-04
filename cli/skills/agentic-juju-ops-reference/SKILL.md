---
name: agentic-juju-ops-reference
description: COS modelinde Juju status, debug-log, model switch ve run aksiyonları için komut şablonları verirken kullan.
---

## Amaç

**Model**: gözlemlenebilirlik işleri **`cos`** (veya ekip adı) modelinde — `../../skills/juju-model-cos/SKILL.md`. Komutlar: **`juju status`**, **`juju debug-log`**, **`juju switch cos`**, birim aksiyonları **`juju run <app>/<unit> <action> --format=yaml`**. İlişki tablosu: `juju status --relations` veya benzeri çıktıyı okuma rehberi; detay Faz 1 `cos-relation-*` skill’lerinde.

## Kapsam

### Dahil

- Leader unit seçimi (`grafana/leader` gibi Faz 1 örnekleriyle uyumlu).
- `--model` kullanımı bağlam net değilse.

### Hariç

- Controller bootstrap adımları (Faz 1 `juju-bootstrap-microk8s`).

## Kurallar

- Faz 1’de geçen charm adları ve aksiyon isimleri ile çelişme yok (`cos-deploy-grafana`: `get-admin-password`).
- Uzun çıktıda `grep`/`less` önerisi; ajan araç politikasına uy.
- Credential dosyalarını loglama yok.

## Kontrol listesi

- [ ] Doğru modelde miyim (`juju models`)?
- [ ] `blocked` / `error` mesajı charm üzerinde görünüyor mu?
- [ ] İlişki eksikliği var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| permission denied | Juju hesabı | `juju whoami` |
| action failed | action çıktısı | İlgili cos-deploy skill |

## İlgili belgeler ve skill'ler

- `../../skills/juju-model-cos/SKILL.md`
- `../../skills/juju-bootstrap-microk8s/SKILL.md`
- `../agentic-cos-advisor-overview/SKILL.md`
- `../agentic-troubleshoot-grafana/SKILL.md`

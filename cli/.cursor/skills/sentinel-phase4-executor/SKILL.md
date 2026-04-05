---
name: sentinel-phase4-executor
description: >-
  Sentinel CLI Faz 4 — Grafana HTTP bağlantı doğrulama: config, doctor, mock
  testler, dokümantasyon. sentinel-coming/cli kökünde çalışır; secret repoya
  girmez. Faz 3 yeşil test önkoşuludur.
---

# Sentinel CLI — Faz 4 yürütücü

## Ne zaman kullan

`sentinel-coming/cli/` içinde Faz 4 teslimatı: opsiyonel Grafana yapılandırması, `doctor` ile HTTP bağlantı testi, `httpx` + mock testler, README/roadmap uyumu.

## Zorunlu okumalar (sıra)

1. `documantations/IMPLEMENTATION_PLAN_PHASE4.md` — kapılar G0–G6 ve alt görevler
2. `documantations/CODEX_EXECUTION_PROMPT_PHASE4.md` — otomatik geçişli adım sırası (aynı sırayı izle)
3. `documantations/ROADMAP_PHASE3_5.md` — kapsam sınırı (çok kullanıcı yok, ürün telemetrisi yok)
4. `skills/agentic-troubleshoot-grafana/SKILL.md` — CLI’da teşhis köprüsü metni için kopyalanabilir yol

## Kurallar

- **Secret:** Token, URL kimliği, şifre repoya yazılmaz; `.env` / ortam değişkeni. `doctor` çıktısında ham token yok.
- **Env öneki:** `SENTINEL_GRAFANA_*` kullan; `GF_*` ile çakışma yok.
- **Test:** `python -m ruff check .` ve `python -m pytest -q` (venv: `pip install -e ".[dev]"`).
- **İki katman:** (1) Mock HTTP ile 200/401/timeout — CI ağı yok. (2) Stack açıksa canlı test + `documantations/PHASE4_REAL_STACK_VERIFY.md` secret olmadan doldur; kapalıysa tek cümle atlama.
- **Diff:** Minimal; mevcut `config/loader.py`, Pydantic modelleri ve `cli/app.py` `_doctor` ile uyumlu kal.

## Tipik kod/dokunuşlar

- `config/sentinel.example.yaml` — opsiyonel `grafana` veya `observability.grafana`
- Pydantic şemalar — `src/sentinel_cli/config/` (mevcut yapıyı genişlet)
- `src/sentinel_cli/cli/app.py` — `doctor` JSON’a Grafana özet veya alt bölüm + HTTP test çağrısı
- Yeni modül: bağlantı testi mantığı (test edilebilir fonksiyon)
- `tests/` — mock senaryoları
- `documantations/GRAFANA_HTTP_PHASE4.md` — seçilen health uç, resmi Grafana HTTP API doc linki (sürüm seçici)
- `README.md` — Faz 4 env ve doküman linkleri

## Bittiğinde

- `IMPLEMENTATION_PLAN_PHASE4.md` son satırına kapanış tarihi
- Özet: mock yeşil; canlı doğrulama yapıldı veya atlama notu yazıldı

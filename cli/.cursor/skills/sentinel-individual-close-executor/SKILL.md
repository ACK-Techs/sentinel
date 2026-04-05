---
name: sentinel-individual-close-executor
description: >-
  Sentinel CLI bireysel kapanış: REPL’e Grafana doctor özetinin secret-safe
  enjeksiyonu, config bayrağı, testler ve dokümantasyon. Kök sentinel-coming/cli.
---

# Sentinel — bireysel kapanış yürütücü

## Ne zaman kullan

`IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` içindeki **A (zorunlu)** ve isteğe bağlı **B** maddelerini kodla.

## Zorunlu okumalar

1. `documantations/IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md`
2. `documantations/GRAFANA_AI_PLATFORM_RESEARCH.md`
3. `skills/agentic-sentinel-grafana-agent-bridge/SKILL.md`
4. `src/sentinel_cli/cli/app.py` — REPL başlangıcı
5. `src/sentinel_cli/observability/grafana.py` — `check_grafana_connection`, `GrafanaCheckResult`

## Kurallar

- Secret (token, tam internal URL) modele veya loga sızmaz.
- Özeti **session.messages’a USER olarak ekleme**; `SessionState.grafana_context_snapshot` + `system_prompt` birleştir (HistoryCompactor ile uyum).
- Snapshot oturum başına en fazla bir kez HTTP ile doldurulur; REPL satır başına tekrar istek yok.
- B katmanı (tool) yapılıyorsa: `supports_tools` ve Gemini 400 riski — varsayılan kapalı veya yalnızca uygun profil.

## Bittiğinde

- `documantations/INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md` ile uyum
- `python -m ruff check .` ve `python -m pytest -q`

# Codex / Cursor — bireysel kapanış tek mesaj prompt’u

Aşağıdaki bloğu **tek mesaj** olarak yapıştır. Kök: `sentinel-coming/cli/`.

---

## Sistem talimatı

Sen bu repoda **Sentinel CLI bireysel kullanım kapanışı** teslimatını uyguluyorsun: REPL’deki LLM’in Grafana ile ilgili **operasyonel özet** görebilmesi (Faz 4 `doctor` mantığının ajan bağlamına taşınması). Çok kiracı yok; ürün telemetrisi yok.

**Doğruluk kaynakları:**

1. `documantations/IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md`
2. `documantations/GRAFANA_AI_PLATFORM_RESEARCH.md`
3. `skills/agentic-sentinel-grafana-agent-bridge/SKILL.md`
4. `.cursor/skills/sentinel-individual-close-executor/SKILL.md`

**Kurallar:**

- Minimal diff; secret repoya ve prompta girmez.
- `check_grafana_connection` ve `GrafanaCheckResult.to_dict()` yeniden kullan.
- Komutlar: `python -m ruff check .`, `python -m pytest -q` (venv: `./.venv/bin/python`).

**Akış:** Kullanıcıya sorma. G0 → G1 → G2 geç; B (isteğe bağlı tool) için planda “yapıldı / bilinçli atlandı” net yaz.

---

## G0 — Ön kontrol

- `cd sentinel-coming/cli`
- `./.venv/bin/python -m pip install -e ".[dev]"`
- Mevcut `ruff` + `pytest` yeşil.

**Onay:** Yeşilse → **G1**.

---

## G1 — Bağlam enjeksiyonu (A katmanı)

1. `AgentSettings` + `sentinel.example.yaml` + `loader._env_overlay`: `grafana_context_in_repl` + env `SENTINEL_GRAFANA_CONTEXT_IN_REPL`.
2. `SessionState` + `SessionStore`: opsiyonel `grafana_context_snapshot: str | None`; `save`/`load` JSON’da `.get` ile geriye dönük uyum.
3. `AgentLoop.run` başı: bayrak açık ve `snapshot is None` iken **bir kez** `check_grafana_connection(..., env=os.environ)`; `json.dumps(to_dict(), ensure_ascii=True)`; `save`.
4. `AgentLoop._request`: `system_prompt` = `agent.system_prompt` + (snapshot varsa) Türkçe uyarı + snapshot. **Özeti `session.messages` içine USER olarak ekleme** (HistoryCompactor ilk-USER mantığı ile çakışır).
5. `run` ve `repl` aynı davranış; README’de bir cümle.

**Test:** `ruff` + `pytest`.

**Onay:** → **G2**.

---

## G2 — Yeni testler

1. `check_grafana_connection` mock: bayrak açık + yeni oturumda snapshot dolu; LLM’e giden istekte `system_prompt` birleşik metinde özet; bayrak kapalı veya snapshot dolu iken ikinci HTTP yok.

**Test:** `ruff` + `pytest` yeşil.

**Onay:** → **G3**.

---

## G3 — B (isteğe bağlı) + dokümantasyon

1. **B:** İnce `grafana_health` tool — yalnızca mevcut check fonksiyonunu sar. Varsayılan: devre dışı veya yalnızca `supports_tools: true` profiller; Gemini cloud için risk dokümante et. **Yapmıyorsan** `IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` içinde “B bilinçli atlandı” notu ekle.
2. `README.md`: REPL + Grafana özet paragrafı + indeks linki.
3. `documantations/ROADMAP_PHASE3_5.md`: bireysel kapanış satırı / sonraki adım.
4. `INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md` dosya listesi ile gerçek dosyalar eşleşsin.

**Test:** `ruff` + `pytest`.

---

## Kapanış mesajı

Kısa özet: REPL Grafana özet enjeksiyonu + testler; B durumu; sonraki: gerçek metrik sorgusu veya MCP (ayrı karar).

# Bireysel kullanım kapanışı — Grafana ↔ REPL ajan bağlamı

**Kök:** `sentinel-coming/cli/`  
**Önkoşul:** Faz 3–4 tamam; `doctor` Grafana HTTP kontrolü çalışıyor; canlı stack için env ayarlı.

**Amaç:** REPL’deki LLM’in “Grafana’yı hiç görmüyorum” durumunu **tasarımla kapatmak**: bağlantı özeti ve (isteğe bağlı) genişletilebilir veri yüzeyi.

**Kapsam dışı:** Çok kiracı, ürün telemetrisi, Grafana Cloud Assistant’ı birebir kopyalama.

---

## Problem özeti

- `doctor` JSON’u operatöre yönelik; **ajan döngüsüne otomatik girmez**.  
- Grafana Labs’ın LLM/Assistant özellikleri **Grafana içinde** çalışır; Sentinel REPL ayrı süreçtir (`GRAFANA_AI_PLATFORM_RESEARCH.md`).

---

## Çözüm katmanları (öncelik sırası)

### A — Bağlam enjeksiyonu (zorunlu, düşük risk)

**Tasarım kararı (kritik):** Özeti `session.messages` içine ayrı bir **USER** mesajı olarak koyma. `HistoryCompactor` ilk USER’ı “kullanıcı hedefi” sanıyor; özet USER ilk sırada olunca hem yanlış koruma hem kirpmede kayıp riski oluşur.

**Doğru yol:** `SessionState` içinde opsiyonel `grafana_context_snapshot: str | None` (JSON metin, `GrafanaCheckResult.to_dict()` ile üretilmiş, secret-safe). Oturum dosyasında yoksa (`load` sırasında `.get(..., None)`) geriye dönük uyum.

| ID | İş | Başarı kriteri |
|----|-----|----------------|
| A.1 | `AgentSettings` + YAML + `loader._env_overlay`: `grafana_context_in_repl: bool` (varsayılan `true`); env `SENTINEL_GRAFANA_CONTEXT_IN_REPL`. | `AppConfig` doğrulanır. |
| A.2 | `AgentLoop.run` başında: bayrak açık ve `session.grafana_context_snapshot is None` iken **bir kez** `check_grafana_connection(config.grafana, env=os.environ)` çağır; `json.dumps(result.to_dict(), ensure_ascii=True)` ile snapshot yaz; `session.save`. Grafana yapılandırılmamışsa snapshot yine doldurulabilir (skipped sonucu) — model “bağlı değil”i anlasın. | Tek HTTP çağrısı / oturum; REPL’in her satırında tekrarlanmaz. |
| A.3 | `AgentLoop._request`: `ChatRequest.system_prompt` birleştirilirken `config.agent.system_prompt` + (snapshot varsa) kısa Türkçe uyarı + snapshot metni. Böylece tüm iç tur ve uzun konuşmada bağlam **system** kanalından kalır; compaction yalnızca `messages` üzerinde çalışır. | Ham token yok; `to_dict()` alanları yeterli. |
| A.4 | `run` ve `repl` aynı `AgentLoop` yolunu kullandığından davranış ikisinde de tutarlıdır (tek atımlık `run` da aynı oturum kuralına girer). | Dokümanda bir cümle. |

### B — İsteğe bağlı tool (orta risk, `supports_tools` açık profiller)

| ID | İş | Başarı kriteri |
|----|-----|----------------|
| B.1 | `grafana_health` veya `observability_grafana_status` adlı ince tool: yalnızca `check_grafana_connection` döndürür. | Cloud profilde Gemini 400 riski varsa varsayılan kapalı veya yalnızca `local` profil. |
| B.2 | Tool açıklamasında: health ≠ metrik; “no data” için Faz 1 playbook köprüsü. | README + skill uyumu. |

### C — Dokümantasyon ve skill

| ID | İş |
|----|-----|
| C.1 | `INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md` güncel. |
| C.2 | `README.md` “REPL + Grafana” kısa bölüm. |
| C.3 | `ROADMAP_PHASE3_5.md` “bireysel kapanış” satırı. |

### D — Test

| ID | İş |
|----|-----|
| D.1 | `check_grafana_connection` mock: bayrak açık + yeni oturumda snapshot doluyor ve `_request`/`complete`’e giden `ChatRequest` içinde `system_prompt` birleşik metinde `ok`/`skipped` özeti geçiyor. Bayrak kapalı veya snapshot zaten dolu iken tekrar çağrı yok. |
| D.2 | `ruff` + `pytest` yeşil. |

---

## Kapı (gate)

- G0: Mevcut testler yeşil.  
- G1: A.1–A.4 kod + doküman.  
- G2: D.1 testleri.  
- G3: B isteğe bağlı; yapılmadıysa planda “bilinçli dışarıda” işaretle.

---

## Yürütme

Tek mesaj prompt: `CODEX_EXECUTION_PROMPT_INDIVIDUAL_CLOSE.md`.  
Cursor skill: `.cursor/skills/sentinel-individual-close-executor/SKILL.md`.

---

## Dış kaynaklar

- `documantations/GRAFANA_AI_PLATFORM_RESEARCH.md`  
- `documantations/GRAFANA_HTTP_PHASE4.md`  
- `skills/agentic-sentinel-grafana-agent-bridge/SKILL.md`  
- `skills/agentic-grafana-llm-platform-overview/SKILL.md`

**B bilinçli atlandı:** Ayrı Grafana tool katmanı bu turda uygulanmadı; A katmanı (system prompt snapshot enjeksiyonu) ile düşük riskli bireysel kapanış yolu seçildi.

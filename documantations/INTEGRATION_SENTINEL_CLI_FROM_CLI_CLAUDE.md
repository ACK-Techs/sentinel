# Sentinel CLI ← cli-claude referans entegrasyonu

Bu doküman, **Sentinel** ana ürünü (`/cli` — README’deki Python tabanlı CLI) için `agentic/cli-claude` içinden **hangi davranışların** taşınabileceğini ve Sentinel mimarisine nasıl oturacağını özetler. Hedef: gözlemlenebilirlik odaklı uzun oturumlarda **hafıza, güvenlik ve operatör verimi**.

---

## Referans: cli-claude kaynak yolu

Bu bilgisayarda tam yol:

**`/home/caglarkc/Desktop/Github/sentinel-coming/agentic/cli-claude/`**

- Masaüstü → `Github` → `sentinel-coming` → `agentic` → `cli-claude`
- Kaynak: `.../agentic/cli-claude/src/`

Önemli referans dosyaları:

| Konu | `src/` altındaki konum |
|------|-------------------------|
| Auto-dream | `services/autoDream/` |
| Bellek çıkarma | `services/extractMemories/` |
| Fork + araç izolasyonu | `utils/forkedAgent.ts`, `extractMemories.ts` içi `createAutoMemCanUseTool` |
| Tur sonu işler | `query/stopHooks.ts` |
| Post-turn hook | `utils/hooks/postSamplingHooks.ts` |
| Oturum özeti (compaction) | `services/SessionMemory/`, `services/compact/` |
| MCP + tool havuzu | `tools.ts` içinde `assembleToolPool`, `services/mcp/` |
| Kullanıcı ayarı şeması (örnek anahtarlar) | `utils/settings/types.ts` (`autoDreamEnabled`, `autoMemoryEnabled`, …) |
| Arka plan ev işleri | `utils/backgroundHousekeeping.ts` |

---

## Sentinel mimarisine eşleme

| Sentinel (README / `cli/`) | cli-claude karşılığı | Entegrasyon fikri |
|----------------------------|----------------------|-------------------|
| Agent döngüsü + `run` / `repl` | `handleStopHooks` + `query` döngüsü | Her tamamlanan **turn** sonunda opsiyonel arka plan kuyruğu |
| MCP entegrasyonu | `assembleToolPool`, deny kuralları, MCP client | Built-in + MCP birleşimi ve **deny öncesi** filtre |
| Bash / dosya araçları | `canUseTool` + read-only bash | Sentinel sandbox ile aynı güvenlik dilimi |
| `cli/skills` + trajectory | extract + dream + Magic Docs | Uzun COS/Juju oturumlarında **öğrenilen notlar** + periyodik birleştirme |
| YAML profiller + env | settings + GrowthBook | Önce env; ileride uzaktan bayrak (isteğe bağlı) |
| Observability gateway | (doğrudan yok) | Tur sonu: küçük **structured log** / metrik event (CLI süreci içinde) |

---

## Öncelikli entegrasyon maddeleri

### P0 — Proje hafızası ve “dreaming”

1. **Otomatik bellek dizini** (ör. `~/.sentinel/projects/<cwd>/memory/` veya repo içi `.sentinel/memory/` — güvenlik politikasına göre).  
2. **Tur sonu extract:** Kısa notlar (append-only günlük veya dosya başına konu).  
3. **Koşullu konsolidasyon (dream):** Süre + oturum sayısı + kilit; ikinci LLM çağrısı ile indeks güncelleme.  
   - Referans: `services/autoDream/*`, `consolidationPrompt.ts`

### P1 — Güvenlik ve operatör deneyimi

4. **Araç politikası:** Bellek kökü dışına yazmayı reddetme; bash için salt okunur allowlist.  
   - Referans: `createAutoMemCanUseTool` (`extractMemories.ts`)

5. **Hook çatısı:** Eklenti veya `hooks/` YAML sonrası çalışan dahili hook’lar (Sentinel’in mevcut hook tasarımıyla birleştirin).  
   - Referans: `utils/hooks/postSamplingHooks.ts`, `utils/hooks.js` (user stop hooks ile karıştırmayın; isimleri net ayırın)

### P2 — Dokümantasyon ve bağlam maliyeti

6. **Magic Docs benzeri:** `# MAGIC DOC` ile işaretli Markdown’ların oturum sonunda güncellenmesi — özellikle `cli/skills` ve `documantations/`.  
   - Referans: `services/MagicDocs/magicDocs.ts`

7. **Uzun REPL oturumu:** Context compaction / session memory dosyası.  
   - Referans: `services/compact/`, `SessionMemory/sessionMemory.ts`

8. **Away / geri dönüş özeti:** Uzun canlı `repl` için bir satırlık özet (isteğe bağlı).  
   - Referans: `services/awaySummary.ts`

---

## MCP ve gateway ile sınır

- **Observability gateway** read-only HTTP API’dir; “dreaming” orada değil, **CLI sürecinde** kalmalı.  
- MCP araçları eklendiğinde: cli-claude’daki gibi **deny kurallarıyla** built-in önek sabit kalmalı (prompt cache ve güvenlik).

---

## Konfigürasyon önerisi (Sentinel)

Örnek env / YAML anahtarları (isimler Sentinel konvansiyonunuza göre uyarlanır):

- `SENTINEL_AUTO_MEMORY=1`
- `SENTINEL_AUTO_DREAM=1`
- `SENTINEL_DREAM_MIN_HOURS=24`
- `SENTINEL_DREAM_MIN_SESSIONS=5`
- `SENTINEL_MEMORY_DIR=...`

cli-claude eşdeğeri: `autoMemoryEnabled`, `autoDreamEnabled`, GrowthBook `tengu_onyx_plover` — Sentinel’de basit config yeterli.

---

## Doğrulama checklist’i

- [ ] Hafıza dizini: **check-in edilmemeli** mi (`.gitignore`)?  
- [ ] COS/Juju komut çıktılarında **secret** (token, kubeconfig) hafızaya yazılmıyor mu?  
- [ ] `--bare` / non-interactive modda dream/extract **kapalı** mı? (cli-claude `isBareMode` deseni.)  
- [ ] CI’da arka plan fork’ları **deterministik test** ile çakışmıyor mu?

---

## Lisans ve türetilmiş çalışma

`agentic/cli-claude` bu monorepoda **referans** amaçlıdır; Sentinel’e metin/kod aktarırken Anthropic / upstream lisansına uyun. Uygulamada **davranışı Python’da yeniden yazmak** + bu dosyadaki yolları referans tutmak en güvenli yoldur.

---

*Son güncelleme: 2026 — referans yolu bu makinedeki monorepo ile sabitlendi.*

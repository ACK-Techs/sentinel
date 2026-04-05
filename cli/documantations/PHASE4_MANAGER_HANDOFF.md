# Faz 4 — Yönetici AI el sıkışması

Bu dosya **kod yazmayan** koordinatör ajan ile **kod teslim eden** ajan arasında bağlam aktarır. Ürün kökü: `sentinel-coming/cli/`.

## Mevcut durum (envanter)

| Bileşen | Durum |
|---------|--------|
| `IMPLEMENTATION_PLAN_PHASE4.md` | Tam plan + G0–G6 kapıları |
| `CODEX_EXECUTION_PROMPT_PHASE4.md` | Tek mesajda sıralı yürütme (Codex veya benzeri) |
| `PHASE4_SKILL_AND_DOC_INDEX.md` | Dosya ve skill köprü indeksi |
| `GRAFANA_HTTP_PHASE4.md` | **Taslak** — yürütücü ajan kurduğu Grafana sürümüne göre uçları ve resmi doc linkini netleştirir |
| `PHASE4_REAL_STACK_VERIFY.md` | **Şablon** — canlı test sonucu veya atlama cümlesi (secret yok) |
| `skills/agentic-troubleshoot-grafana/SKILL.md` | Faz 1 teşhis köprüsü (CLI çıktısında referans verilecek) |
| Kod: `doctor` | Şu an profil/MCP özeti; **Grafana HTTP bağlantı testi Faz 4 ile eklenecek** |
| Kod: config | `sentinel.example.yaml` içinde **Grafana bölümü yok** — Faz 4.B |

**Önkoşul (G0):** Faz 3 kapanmış; `ruff` + `pytest` yeşil kalmalı.

## Rol ayrımı

- **Yönetici AI:** Kapıları takip eder, prompt/skill günceller, gerçek stack varlığını ve `PHASE4_REAL_STACK_VERIFY.md` doldurulmasını ister; secret repoya girebilir.
- **Yürütücü AI:** `IMPLEMENTATION_PLAN_PHASE4.md` ve `CODEX_EXECUTION_PROMPT_PHASE4.md` sırasına uyarak kod + dokümantasyon + mock testleri yazar; canlı stack erişilebilirse doğrular.

## Faz 4 kapanış tanımı

1. G1–G5 maddeleri plandaki başarı kriterlerini karşılar.
2. G6: `PHASE4_REAL_STACK_VERIFY.md` doldurulur **veya** tek cümle bilinçli atlama yazılır.
3. `IMPLEMENTATION_PLAN_PHASE4.md` sonuna `**Faz 4 tamamlandı:** YYYY-MM-DD` eklenir.

## Yürütücüye verilecek tek kaynak

Öncelik sırası: bu dosyadaki envanter + aşağıdaki **yapıştırma prompt’u** (veya doğrudan `CODEX_EXECUTION_PROMPT_PHASE4.md` içeriği). Cursor’da kod yazan ajan için ek bağlam: proje skill’i `sentinel-phase4-executor` (`.cursor/skills/sentinel-phase4-executor/SKILL.md`).

## Faz 4 sonrası — canlı test öncesi

Gerçek stack’e bağlanmadan önce mimari rapor ve genişletilmiş test/rehber için: [PRE_LIVE_VALIDATION_HANDOFF.md](PRE_LIVE_VALIDATION_HANDOFF.md).

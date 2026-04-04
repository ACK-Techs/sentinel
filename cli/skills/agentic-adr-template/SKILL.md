---
name: agentic-adr-template
description: Dil seçimi, LLM sağlayıcısı ve sandbox seviyesi gibi mimari kararlar için ADR şablon başlıkları sağlarken kullan.
---

## Amaç

ADR başlık seti: **Bağlam** (problem, kısıtlar) — **Karar** (seçilen seçenek) — **Sonuçlar** (pozitif/negatif) — **Alternatifler** (reddedilenler ve neden). Örnek konular: Python vs Go, OpenAI-uyumlu tek yol vs çok adapter, sandbox seviyesi POC/üretim, telemetry açık/kapalı.

## Kapsam

### Dahil

- Depo içi `docs/adr/NNNN-title.md` isimlendirme önerisi.
- `agentic-project-charter` ile hizalama kontrolü.

### Hariç

- Kurumsal RFC süreci dışı onay akışı.

## Kurallar

- Her ADR tek karar; karışık konuları böl.
- Tarih ve katılımcı bilgisi (opsiyonel ama faydalı).
- Kırıcı değişiklikte yeni ADR; eskiyi silme.

## Kontrol listesi

- [ ] Karar, mevcut kod veya plan ile çelişiyor mu?
- [ ] Alternatifler tarafsız mı?
- [ ] Sonuçlar ölçülebilir mi (metrik)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Belirsiz karar | Scope | ADR’yi daralt |
| Uygulanmadı | PR linki | Implementasyonu bağla |

## İlgili belgeler ve skill'ler

- `../agentic-project-charter/SKILL.md`
- `../agentic-sandbox-hardening-reference/SKILL.md`
- `../agentic-llm-provider-contract/SKILL.md`
- `../documantations/IMPLEMENTATION_PLAN_PHASE2.md`

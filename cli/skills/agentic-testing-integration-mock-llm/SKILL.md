---
name: agentic-testing-integration-mock-llm
description: Sahte LLM ile uçtan uca tur ve tool çağrısı entegrasyon testi tasarlarken kullan.
---

## Amaç

**Deterministik fixture**: önceden kayıtlı model yanıtları veya sabit tool çağrı dizisi. **Akış**: kullanıcı mesajı → mock stream → parse → (onay mock) → tool execute mock → tekrar model. **Zaman sınırı**: pytest timeout (örn. 30s) ile asılı test önleme. Ağ ve gerçek API **kapalı**.

## Kapsam

### Dahil

- `agentic-agent-turn-loop` ile uyumlu olay sırası.
- Hata senaryosu: model hatalı tool üretir → parse reddi → recovery.

### Hariç

- Çoklu gerçek sağlayıcı matrisi.

## Kurallar

- Mock, `agentic-llm-streaming-events` sözleşmesini taklit etmeli.
- Tool registry test için minimal alt küme.
- Paralel test için session dosyası çakışması yok (`tmp_path`).

## Kontrol listesi

- [ ] En az bir mutlu yol + bir hata yolu testi var mı?
- [ ] Test süresi CI bütçesinde mi?
- [ ] Mock güncel şema ile senkron mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Flaky | race | asyncio gather sırası |
| Fixture eski | API değişti | Kayıtları güncelle |

## İlgili belgeler ve skill'ler

- `../agentic-agent-turn-loop/SKILL.md`
- `../agentic-agent-tool-call-parse/SKILL.md`
- `../agentic-testing-unit/SKILL.md`
- `../agentic-tools-base-contract/SKILL.md`

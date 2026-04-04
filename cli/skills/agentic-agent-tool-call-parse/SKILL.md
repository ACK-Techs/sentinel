---
name: agentic-agent-tool-call-parse
description: Model çıktısından tool çağrılarını doğrulama, bilinmeyen araç ve şema ihlallerini yönetirken kullan.
---

## Amaç

**Bilinmeyen araç adı**: yürütme yok; modele `tool` rolü ile açıklayıcı hata döndür. **Şema ihlali**: JSON Schema veya pydantic doğrulama; eksik zorunlu alan listesi modele geri verilir. **Çoklu çağrı**: sıra korunur; bir başarısız olsa bile diğerleri (politikaya göre) işlenebilir. Hata mesajı **kısa ve makine tarafından okunur** kalır.

## Kapsam

### Dahil

- Streaming’den gelen kısmi argüman birleştirme (`agentic-llm-streaming-events`).
- `apply_patch` benzeri özel string argümanlar (proje kararı).

### Hariç

- Model fine-tuning ile tool format düzeltme.

## Kurallar

- Registry’de olmayan isim asla çalıştırılmaz (`agentic-tools-base-contract`).
- Kullanıcıya özet: “model var olmayan araç önerdi” (güvenlik şeffaflığı).
- Injection: argümanlarda shell metachar kontrolü tool tipine göre.

## Kontrol listesi

- [ ] Her public tool için şema testi var mı?
- [ ] Kötü JSON için recovery tek deneme mi (protokol)?
- [ ] Çoklu tool atomik mi yoksa kısmi mi (dokümante)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Model halüsinasyon tool | İsim listesi | Modele hata + yeniden dene |
| Argüman tip uyuşmazlığı | Schema | Alan bazlı mesaj |

## İlgili belgeler ve skill'ler

- `../agentic-llm-streaming-events/SKILL.md`
- `../agentic-tools-base-contract/SKILL.md`
- `../agentic-agent-turn-loop/SKILL.md`
- `../agentic-hooks-pre-post-tool/SKILL.md`

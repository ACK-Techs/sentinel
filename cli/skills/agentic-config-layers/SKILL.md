---
name: agentic-config-layers
description: Varsayılan, dosya, ortam ve CLI bayraklarından gelen yapılandırmanın birleştirme sırasını uygularken kullan.
---

## Amaç

Birleştirme sırası: **defaults < `config.yaml` (veya proje dosyası) < environment variables < CLI flags**. Çakışma çözümü tek doğruluk kaynağı olarak dokümante edilir. Liste türü alanlar için strateji açıkça seçilir: **replace** (son kazanır) veya **append** (dikkatli kullan); proje kararı `IMPLEMENTATION_PLAN_PHASE2.md` ile uyumlu olmalı.

## Kapsam

### Dahil

- Tek dosya vs kullanıcı + proje dizini arama sırası (proje kararı; örnek: cwd ve üst dizinlerde `sentinel_config.yaml`).
- Profil seçiminin hangi katmandan geldiği (`SENTINEL_PROFILE`).

### Hariç

- Uzak config sunucusu (feature değilse).

## Kurallar

- Aynı anahtar için öncelik tablosu README’de kopyalanabilir blok olarak bulunmalı.
- Hassas alanlar (api key) dosyada düz metin önerilmez; env tercih edilir (`agentic-secrets-handling`).
- Birleştirme sonucu debug modunda **maskeleme ile** yazdırılabilir.

## Kontrol listesi

- [ ] İki kaynaklı test: sadece env, sadece dosya, ikisi birden beklenen sonuç mu?
- [ ] Liste alanları için replace/append dokümante mi?
- [ ] Bilinmeyen anahtar uyarısı (typo yakalama) var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Beklenmeyen model seçildi | Hangi katman kazandı | `--verbose` ile efektif config yazdır |
| YAML parse hatası | Dosya yolu | Kullanıcıya satır numarası ile hata |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-config-profiles/SKILL.md`
- `../agentic-config-env-reference/SKILL.md`

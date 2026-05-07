---
name: obs-grafana-ai-plugin
description: Grafana AI/LLM plugin’i güvenli şekilde etkinleştirmek, doğal dil ile query üretimini sınırlı kapsamda açmak ve veri sızıntısı riskini yönetmek gerektiğinde kullan. “Grafana’ya LLM bağla”, “AI query”, “hangi veriler dışarı çıkar?” sorularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Etkinleştirme planı: hangi kullanıcılar, hangi datasourcelar, hangi özellikler açık?
- Güvenlik checklist’i: prompt/data exposure, audit, rate limit ve izinler
- Doğrulama: kontrollü bir örnek NL istek → üretilen query → beklenen veri

## Workflow
- Kapsamı daralt:
  - Hangi ekipler kullanacak? (pilot)
  - Hangi datasource’lar? (prod log gibi hassas kaynakları önce kapalı tut)
- Veri riski analizi:
  - Log/trace içerikleri PII/secrets içeriyor mu?
  - LLM’e gönderilen context nereden geliyor? (query text, panel metadata, örnek sonuç?)
- İzin ve denetim:
  - RBAC ile kim kullanabilir?
  - Audit/logging ihtiyacı: kim hangi NL sorguyu yaptı?
- Operasyon:
  - Rate limit / maliyet kontrolü.
  - “LLM yoksa” fallback: kullanıcıya üretilen query’yi göster ve elle çalıştır.
- Doğrulama senaryosu:
  - Basit bir NL istek seç (örn. “son 30 dk error rate”).
  - Üretilen query’nin doğru olduğunu kontrol et (label’lar, zaman penceresi, aggregations).

## Common mistakes
- Prod log datasource’unu doğrudan AI’a açmak: veri sızıntısı ve uyum riski.
- AI çıktısını doğrulamadan “tek tıkla uygula”: yanlış query → yanlış karar.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-rbac`

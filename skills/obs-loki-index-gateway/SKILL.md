---
name: obs-loki-index-gateway
description: Loki’de index okuma yükünü ölçeklemek veya object storage index erişimini optimize etmek için Index Gateway’i devreye almak/ayırmak gerektiğinde kullan. “querier index’te boğuluyor”, “index erişimi yavaş”, “index gateway gerekir mi?” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı:
- Index Gateway’in hangi problemi çözdüğünün net açıklaması (index read path)
- Ne zaman anlamlı olduğuna dair karar (yük, latency, storage backend)
- Devreye alma sonrası doğrulama: query latency ve storage istek sayısı değişimi

## Workflow
- Önce darboğazı doğrula:
  - Sorun index erişimi mi, yoksa chunk fetch/parse mı? (yanlış bileşeni ölçekleme)
- Ne zaman Index Gateway:
  - Object storage’da index okuma pahalı/latency yüksekse.
  - Querier sayısı arttıkça index istekleri katlanıyorsa (N× etkisi).
- Tasarım kararları:
  - Gateway’i ayrı servis olarak koyduğunda querier’ların index’e erişim şekli değişir.
  - Availability: gateway down olursa query ne olur? (kritik bağımlılık)
- Doğrulama:
  - Öncesi/sonrası aynı ağır sorguda latency ve error oranı.
  - Storage backend’e giden index request’leri azaldı mı?

## Common mistakes
- Asıl sorun label stratejisi iken index gateway eklemek (yük azalmaz).

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-query-frontend`
- `skills/obs-loki-label-strategy`

---
name: obs-loki-label-strategy
description: Loki’de hangi alanların **label** olacağına karar vermek (index maliyeti), high‑cardinality’i önlemek ve sorgulanabilirlik/performans dengesini kurmak gerektiğinde kullan. “Bu alan label mı olmalı?”, “index şişiyor”, “çok stream var” gibi durumlar için.
---

## Purpose
Bu skill’in çıktısı:
- Loki stream label set’i için kısa “allowed/forbidden” kontratı
- High-cardinality risk listesi (Loki’de label = index → maliyet)
- Promtail/OTel Collector tarafında “field olarak bırak / parse ile filtrele” önerisi

## Workflow
- Loki’de temel kural:
  - Label’lar **index**’e gider; “çok değer” → çok stream → maliyet + yavaş sorgu.
- Etiketleri üç sınıfa ayır:
  - **Stabil routing label**: `cluster`, `namespace`, `app`, `job` (az değer, query başlangıcı)
  - **Sınıflandırma** (dikkat): `level`, `service` (kontrollü değer seti)
  - **Yasak/tehlikeli**: `pod`, `container_id`, `trace_id`, `request_id`, `path`, `user_id`, dynamic hostname
- Sorgu ihtiyaçlarını çıkar:
  - Kullanıcılar en çok neyi filtreleyecek? (namespace/app/level)
  - “Drilldown” için gereken şey label mı olmalı, yoksa LogQL parse sonrası field filter mı?
- Label set’ini minimal tasarla:
  - 5–8 label’ı geçmemeyi hedefle.
  - “Tenant” ihtiyacı varsa `X-Scope-OrgID` (multi-tenancy) ile karıştırma: label ayrı, tenant ayrı.
- Uygulama yeri:
  - Promtail pipeline stages / OTel Collector processors ile **field** üret ve LogQL’de parse ederek filtrele.
  - Sadece routing gerekenler label olsun.
- Doğrulama:
  - “Stream sayısı” ve sorgu latency artıyorsa ilk şüpheli label set’idir.

## Common mistakes
- Kubernetes pod adını label yapmak: churn yüzünden index’i şişirir.
- “Her alan label olsun”: Loki’yi Prometheus gibi kullanmaya çalışmak.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-query-logql`

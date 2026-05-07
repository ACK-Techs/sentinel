---
name: obs-tempo-multi-tenancy
description: Tempo’da trace izolasyonu için tenant header akışını kurmak veya “yanlış tenant trace’i görünüyor / hiç trace bulunmuyor” sorununu çözmek gerektiğinde kullan. Ingest (OTLP/Jaeger/Zipkin) tarafı ve query (Grafana/CLI) tarafındaki header tutarlılığına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Tenant header’ın zincirde nerede eklendiği/korunduğu (collector → tempo, grafana → tempo)
- Canary doğrulama: tenant A’da görünen trace tenant B’de görünmemeli
- Tenant mismatch teşhis checklist’i (proxy strip/overwrite, datasource header, client config)

## Workflow
- Tenant modelini sabitle:
  - Tenant ID kaynağı (team/env/customer) ve tek bir canonical mapping.
- Ingest tarafı:
  - Collector/exporter veya client tempo’ya giderken tenant header ekliyor mu?
  - Ingress/proxy varsa header’ı drop/overwrite ediyor mu?
- Query tarafı:
  - Grafana Tempo datasource, aynı tenant header ile query atıyor mu?
  - Kullanıcı tenant değiştirecekse: datasource ayrımı mı, header override mı?
- Güvenlik:
  - Tenant’ı “all” gibi bypass edecek bir mod açma.
  - Proxy access log’larında tenant/header sızıntısını kontrol et.
- Doğrulama:
  - Tenant A için canary trace üret; Tempo’da bulunabiliyor mu?
  - Tenant B ile aynı trace aranıyor mu? (bulunmamalı)

## Common mistakes
- Ingest var, query yok: Grafana header göndermiyordur (veya tersi).
- Proxy header’ı strip eder: her şey “tek tenant” gibi görünür.

## References
- `skills/obs-tempo-distributor-config`
- `skills/obs-tempo-grafana-datasource`

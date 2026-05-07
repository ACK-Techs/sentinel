---
name: obs-loki-structured-metadata
description: OTel/Promtail üzerinden log’lara eklenen structured alanları (attributes/fields) Loki’de LogQL ile parse edip alan bazlı filtrelemek veya bu alanların label olmaması gerektiğine karar vermek için kullan. “json field ile filtre”, “attributes nasıl sorgulanır?”, “label mı field mı?” gibi sorularda.
---

## Purpose
Bu skill’in çıktısı:
- Structured log alanlarını sorgulamak için LogQL pipeline örnekleri (json/logfmt parse + field filter)
- “Label vs structured field” karar notu (index maliyeti vs sorgu esnekliği)
- Enstrümantasyon/collector tarafı için minimum öneri: hangi alanlar mutlaka taşınmalı

## Workflow
- Structured alanın kaynağını belirle:
  - Log line JSON mu, logfmt mi, yoksa düz metin mi?
  - Alanlar OTel attributes olarak mı, promtail stage ile mi ekleniyor?
- Sorgu yaz (label → parse → field):
  - Önce label selector ile stream’i daralt: `{app="..."}`
  - Sonra parse: `| json` veya `| logfmt`
  - Sonra field filtresi: `level="error"`, `status=~"5.."`, `route="/checkout"` gibi
- Label mı field mı kararını ver:
  - Routing/partition için stabil alanlar label olabilir (namespace/app).
  - Sık değişen/çok değerli alanlar **field** kalmalı (request_id, user_id, trace_id).
- Doğrulama:
  - Parse sonrası alan gerçekten geliyor mu? (örnek 1–2 log satırıyla kontrol)
  - Parse maliyeti: her sorguda ağır parse gerekiyorsa ingestion tarafında normalizasyon düşün.

## Common mistakes
- JSON parse’ı olmayan düz metinde `| json` beklemek (boş sonuç).
- Field’ları label’a taşımak (index şişer) yerine sorguda parse etmek daha güvenlidir.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-label-strategy`
- `skills/obs-loki-query-logql`

---
name: obs-loki-grafana-datasource
description: Grafana’da Loki datasource eklemek/düzeltmek, Explore’da log görememe sorununu gidermek veya derived fields ile log içinden trace linki üretmek gerektiğinde kullan. Datasource URL/auth ve derived field regex’ine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Loki datasource için doğru bağlantı bilgisi (URL, auth, tenant header gerekiyorsa)
- Derived field kuralı: log line içinden `trace_id` yakalayıp Tempo’ya link üretme
- Doğrulama: Explore’da basit LogQL sorgusu + link tıklama testi

## Workflow
- Bağlantıyı netleştir:
  - Loki endpoint URL (Grafana’nın erişebildiği ağdan).
  - Auth (basic/bearer) ve gerekiyorsa tenant header (X-Scope-OrgID).
- “Log yok” teşhisi:
  - Yanlış URL/port → 4xx/5xx
  - Zaman aralığı yanlış → boş
  - Tenant mismatch → boş (push başka tenant’a gidiyor olabilir)
- Explore doğrulaması:
  - Minimal sorgu: `{app="..."} |= "canary"` (label yoksa önce label stratejisine dön)
  - Sonuç dönüyorsa datasource çalışıyor demektir.
- Derived fields ile trace link:
  - Log line’da trace id nerede? (json field mi, text mi)
  - Regex/JSONPath ile trace id’yi çıkar ve Tempo datasource’a linkle.
- Doğrulama:
  - Bir log satırından trace linki çıkar mı?
  - Link doğru trace’i açıyor mu (aynı zaman penceresi)?

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-multi-tenancy`
- `skills/obs-tempo-grafana-datasource`

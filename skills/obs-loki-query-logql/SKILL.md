---
name: obs-loki-query-logql
description: Loki’de LogQL yazarak log aramak (filter), log’u parse etmek (json/logfmt/regex) ve log’dan metrik türetmek (rate/count_over_time) gerektiğinde kullan. “LogQL örneği”, “pipeline stage”, “parse edip field’a göre filtrele”, “log’dan error rate çıkar” gibi taleplerde.
---

## Purpose
Bu skill’in çıktısı:
- Seçili use-case için 1–3 adet LogQL sorgusu (yalnız “çalışan” minimal örnekler)
- Pipeline tasarımı: **stream selector** → **filter** → **parse** → **metric extraction/aggregation**
- Yanlış sorgu tipine göre hızlı düzeltme: “çok log”, “boş sonuç”, “parse olmuyor”

## Workflow
- Önce stream selector’ı daralt:
  - Label tabanlı seç (örn. `{namespace="...", app="..."}`); “label yoksa” önce label stratejisini düzelt.
- Filtre türünü seç:
  - `|= "text"` (içeriyor), `!=`, `|~` (regex), `!~`
  - Büyük regex yerine önce basit filtre, sonra regex (performans).
- Parse (log formatına göre):
  - JSON: `| json` + field adına göre filtre (`status=~"5.."` gibi)
  - logfmt: `| logfmt`
  - Regex: sadece mecbursa (field extraction maliyetli olabilir)
- Metric query’ye çevir (gerekiyorsa):
  - Error rate: `sum by (...) (rate({..} |= "error" [5m]))`
  - Latency bucket gibi yapılar log’dan çıkıyorsa: önce parse, sonra numeric field’e göre filtre/aggregation.
- Sorgu sonucunu kontrol et:
  - Boşsa: selector çok dar mı? zaman aralığı mı? label set yanlış mı?
  - Çok büyükse: selector’ı daralt, parse/regex’i geciktir, aralığı küçült.

## Anti-patterns
- “Her şeyi label’sız yakalayıp içerikte filtrele”: Loki’de pahalı ve yavaş.
- Her sorguda ağır regex parse: önce log formatını düzelt veya promtail/collector’da parse et.

## References
- `skills/cos-deploy-loki`
- `skills/cos-relation-loki-grafana`
- `cli/skills/agentic-troubleshoot-loki`

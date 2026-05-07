---
name: obs-grafana-table-panel
description: Grafana Table panelinde çoklu query sonucunu okunabilir bir tabloya çevirmek (transform’lar, field override’lar, drilldown linkleri) gerektiğinde kullan. “Top N endpoint tablosu”, “kolonları birleştir/sırala”, “satıra tıklayınca log/trace’e git” gibi ihtiyaçlara odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Table panel “recipe”: query → transform → field override → link zinciri
- Drilldown tasarımı: bir satırdan ilgili dashboard / Explore (logs/traces) linkleri
- Anti-pattern’leri engelleyen kararlar: kolon şişmesi, yanlış sort, anlamsız join

## Workflow
- Tablo hedefini netleştir:
  - Satır anahtarı nedir? (örn. `service`, `route`, `status_code`)
  - Kolonlar: KPI’lar (error rate, p95, RPS) ve “son görüldü” gibi yardımcı alanlar.
- Query stratejisi:
  - Tek query ile tüm kolonlar mümkün mü? (tercih)
  - Birden fazla query gerekiyorsa join anahtarını sabitle.
- Transform seçimi (ihtiyaca göre):
  - “Organize fields”: kolon sırası, gizleme, rename.
  - “Join by field”: aynı anahtarda KPI’ları birleştirme.
  - “Group by” / “Reduce”: satır başına tek değer çıkarma.
  - “Sort by” + “Limit”: Top N tablolar.
- Field overrides:
  - Unit/decimals, threshold renkleri, value mapping.
  - Link: kolona veya satıra tıklanınca drilldown URL.
- Drilldown linkleri:
  - Link’e zaman aralığını ve satır anahtarlarını geçir (örn. `service=<value>`).
  - Logs/Traces için label/attribute isimleriyle uyumlu olduğundan emin ol.
- Doğrulama:
  - Top N sıralaması beklenen mi?
  - Aynı KPI time series paneliyle tutarlı mı?

## Common mistakes
- Join anahtarını stabil tutmamak: satırlar çoğalır (cartesian join etkisi).
- “Her şeyi tabloya koymak”: tablo okunmaz olur; 5–8 kolon üstüne çıkma.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-dashboard-design`

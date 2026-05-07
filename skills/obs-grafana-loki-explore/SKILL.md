---
name: obs-grafana-loki-explore
description: Grafana Explore’da Loki ile log araştırması yapmak, Live tail kullanmak veya bir log satırından context (öncesi/sonrası) ve trace linkine gitmek gerektiğinde kullan. “Explore’da log bul”, “live tail”, “log context” gibi operatör akışına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Explore’da hızlı “daraltma” stratejisi (label selector → filtre → parse)
- Live tail’i güvenli kullanma (yük ve gürültü kontrolü)
- Context + korelasyon: aynı label set’te önce/sonra log ve trace linki

## Workflow
- Explore’da başlangıç:
  - Zaman aralığını incident penceresine çek (son 15–60 dk).
  - Label selector ile daralt (`namespace`, `app`, `level`).
- Query’yi büyüt:
  - Önce `|= "error"` gibi basit filter.
  - Sonra gerekirse `| json`/`| logfmt` ile field filtresi.
- Live tail:
  - Canlı tail’i sadece dar selector ile aç (aksi halde gürültü ve maliyet).
  - Kısa süreli kullan; canary/incident doğrulaması için.
- Context:
  - Bir satırı seçip aynı stream’de “öncesi/sonrası”nı gör.
  - Aynı request/trace id varsa derived field linkiyle trace’e git.

## Common mistakes
- Live tail’i geniş selector ile açmak: hem okunmaz hem sistemi zorlar.
- Label yokken içerikte regex ile aramak: yavaş ve pahalı.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-loki-query-logql`
- `skills/obs-loki-grafana-datasource`

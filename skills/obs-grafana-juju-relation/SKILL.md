---
name: obs-grafana-juju-relation
description: Juju/COS ortamında `grafana-source` relation ile Prometheus/Loki/Tempo datasource’larının Grafana’ya otomatik kaydolmasını kurmak veya “relation var ama datasource gelmiyor” sorununu çözmek gerektiğinde kullan. Charm relation modeline odaklanır (API/provisioning değil).
---

## Purpose
Bu skill’in çıktısı:
- Juju relation komutları ve beklenen sonuçlar (datasource’lar görünmeli)
- Troubleshooting akışı: relation → unit status → config → Grafana tarafı doğrulama
- Doğrulama: Explore’da her datasource ile basit bir sorgu çalıştırma

## Workflow
- Bağlam:
  - Hangi charm’lar var? (grafana-k8s, prometheus-k8s, loki-k8s, tempo-k8s vb.)
- Relation kur:
  - Datasource sağlayan charm ile Grafana arasında `grafana-source` relation oluştur.
- Beklenen davranış:
  - Grafana UI’da datasource otomatik oluşmalı (isim/UID charm tarafından).
- “Datasource gelmiyor” teşhisi:
  - `juju status` ile unit’ler blocked/waiting mi?
  - Relation gerçekten kurulu mu? yanlış endpoint mi?
  - Grafana unit log/leader durumu (relation data publish/consume).
- Doğrulama:
  - Grafana Explore’da Prometheus için basit `up` sorgusu.
  - Loki için dar selector’la log getir.
  - Tempo için kısa aralıkta trace araması (en azından datasource reachable).

## Common mistakes
- Yanlış relation endpoint adıyla bağlamak (benzer isimli relation’lar karışır).
- Grafana’yı çok erken test etmek: relation data henüz yayılmamış olabilir; unit status’a bak.

## References
- `skills/cos-deploy-grafana`
- `skills/cos-relation-loki-grafana`
- `skills/cos-relation-prometheus-grafana`

---
name: obs-grafana-backup-restore
description: Grafana’yı felaket senaryosuna hazırlamak için dashboard/datasource/izinler gibi varlıkların backup’ını almak ve kontrollü restore yapmak gerektiğinde kullan. “Grafana çöktü, neyi nasıl geri alacağız?” playbook’u üretmeye odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Backup kapsamı listesi: DB, provisioning dosyaları, plugin’ler, secret’lar (nerede?)
- RPO/RTO’ya göre backup yöntemi önerisi
- Restore adımları + doğrulama checklist’i (UI’da nesneler, query’ler çalışıyor mu?)

## Workflow
- Envanter ve veri kaynağı:
  - Grafana DB türü: sqlite mı, Postgres/MySQL mi?
  - Provisioning kullanılıyor mu? (dashboards/datasources/alerts dosya ile)
- Backup kapsamı:
  - DB dump/snapshot (dashboards, users, orgs, permissions).
  - Provisioning dizinleri ve dashboard JSON kaynakları.
  - Plugin sürümleri (deterministik restore için).
  - Secret’lar: datasource credential’ları (ayrı secret store; backup stratejisi farklı).
- Sıklık ve saklama:
  - RPO/RTO hedeflerini yaz; günlük/saatsel gereksinime göre planla.
- Restore prosedürü:
  - Aynı Grafana sürümü + aynı plugin set’i ile ayağa kaldır.
  - DB restore et / provisioning’i mount et (hangisi source of truth ise).
  - Datasource bağlantı testi.
- Doğrulama:
  - Kritik dashboard listesi açılıyor mu?
  - 1–2 kritik panel query’si “no data” vermiyor mu?

## Common mistakes
- Secret’ları “backup” sanmak: çoğu zaman dış sistemdedir (Vault/K8s Secret); restore planında ayrı ele al.
- Provisioning + DB aynı anda source of truth gibi davranmak: drift ve çakışma.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-provisioning`
- `skills/obs-grafana-plugin-install`

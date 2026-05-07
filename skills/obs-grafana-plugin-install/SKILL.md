---
name: obs-grafana-plugin-install
description: Grafana’ya plugin kurmak/güncellemek, offline ortamda plugin taşımak veya plugin sürümünü kilitleyip deterministik deploy yapmak gerektiğinde kullan. Güvenlik (signed plugin), upgrade riski ve rollback planına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Plugin kurulum planı (online/offline), sürüm kilidi ve rollback adımları
- Güvenlik kontrolü: plugin kaynağı, imza politikası, izinler
- Doğrulama: plugin yüklendi mi ve ilgili panel/datasource çalışıyor mu?

## Workflow
- İhtiyacı netleştir:
  - Plugin tipi: panel mi, datasource mu, app plugin mi?
  - Hangi Grafana sürümüyle uyumlu olmalı?
- Güvenlik:
  - Resmî plugin kaynağı mı? (signed)
  - Unsigned plugin gerekiyorsa bunu istisna olarak ele al; risk ve scope yaz.
- Deploy modeli:
  - Container imajına bake etmek (tercih) vs runtime install.
  - Offline ise: artifact’ı paketle, checksum doğrula.
- Sürüm yönetimi:
  - Sürümü kilitle (deterministik).
  - Upgrade öncesi staging’de test; rollback için eski sürümü hazır tut.
- Operasyon:
  - Grafana restart gerekebilir; bakım penceresi planı.
- Doğrulama:
  - UI’da plugin listesinde görünüyor mu?
  - Plugin’e bağlı panel/datasource query çalışıyor mu?

## Common mistakes
- Sürüm kilitlemeden “latest” kurmak: sonraki restart’ta sürpriz kırılmalar.
- Unsigned plugin’i geniş kapsamda açmak: tedarik zinciri riski.

## References
- `skills/cos-deploy-grafana`

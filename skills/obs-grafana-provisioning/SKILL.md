---
name: obs-grafana-provisioning
description: Grafana’da dashboard/datasource/alert nesnelerini YAML provisioning ile otomatik yüklemek, GitOps benzeri yönetmek veya “provisioned ama görünmüyor/güncellenmiyor” sorununu çözmek gerektiğinde kullan. Dosya yerleşimi ve drift/override davranışına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Provisioning için klasör yerleşimi ve yükleme sırası (datasource → dashboard → alert)
- “Değişiklik neden görünmedi?” teşhis checklist’i (path, folder, overwrite, cache)
- Güvenli secret yönetimi notu (datasource credential)

## Workflow
- Hedef nesneleri belirle:
  - Datasource’lar (Prometheus/Loki/Tempo), dashboard JSON’ları, alert rule set’leri.
- Yerleşim planı:
  - Provisioning dosyaları (YAML) ve dashboard JSON dizinleri ayrı.
  - Datasource’ları önce yükle (dashboard’lar datasource’a bağlı).
- Drift/override kuralları:
  - Provisioned kaynaklar UI’da edit edilirse ne olur? (genelde drift çıkar)
  - “Source of truth” Git mi UI mı? birini seç.
- Secret yönetimi:
  - Datasource token/password’larını repo’ya koyma; secret mount/ENV ile çöz.
- Doğrulama:
  - Grafana restart sonrası datasource ve dashboard’lar görünüyor mu?
  - Dashboard panelleri “datasource not found” demiyor mu?
- “Güncellenmiyor” teşhisi:
  - Yanlış path, folder UID, overwrite ayarı, caching.

## Common mistakes
- Datasource provision etmeden dashboard provision etmek: paneller kırılır.
- UI’dan elle düzenleyip Git’teki sürümle yarışmak: drift ve sürprizler.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`

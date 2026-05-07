---
name: obs-alertmanager-inhibit
description: Alertmanager `inhibit_rules` ile “kök neden” varken türev/gürültü alert’lerini bastırmak (critical varken warning’leri susturmak gibi) gerektiğinde kullan. Amaç sessizlik değil; **hiyerarşik gürültü azaltma**dır.
---

## Purpose
Bu skill’in çıktısı:
- Inhibit kural(lar)ı YAML taslağı (source/target/equal) ve kısa gerekçe
- Güvenlik ağı: yanlış bastırmayı önleyen matcher daraltmaları
- Doğrulama: örnek source+target alert ile inhibit’in gerçekten çalıştığını gösterme

## Workflow
- İnhibit senaryosunu tanımla:
  - Source alert: “kök” (örn. `ClusterDown`, `DatabaseDown`).
  - Target alert: “semptom” (örn. çok sayıda `HighLatency` warning).
- Label kontratı:
  - Source/target’da ortak bağlayıcı label’lar: `cluster`, `service`, `namespace`, `instance`?
- Kuralı yaz:
  - `source_matchers`: kök alert + severity.
  - `target_matchers`: bastırılacak alert set’i.
  - `equal`: bağlayıcı label listesi (aynı “scope”ta bastır).
- Güvenlik ağı:
  - `equal` çok geniş olmasın (örn. sadece `env=prod` ile bastırma yapma).
  - Kural sayısını az tut; her inhibit bir “tasarım borcu”dur.
- Doğrulama:
  - Test ortamında source ve target alert’i aynı anda “firing” yap.
  - Alertmanager UI/API’de target’ın inhibited olduğunu doğrula.

## Common mistakes
- `equal`’ı eksik seçmek: unrelated servislerin warning’lerini bastırır.
- Inhibit’i “silence” gibi kullanmak: incident sonrası unutulur ve körlük yaratır.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`

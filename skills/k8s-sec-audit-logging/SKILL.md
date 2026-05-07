---
name: k8s-sec-audit-logging
description: "Kubernetes API audit log’u etkinleştirmek, policy seviyesini ayarlamak veya güvenlik/uyumluluk için kalıcı API iz kaydı üretmek gerektiğinde kullan. Amaç: **kim, neyi, ne zaman yaptı sorusuna güvenilir yanıt üretmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Audit policy seviyesi ve hedef olay kapsamı
- Log saklama/iletme yaklaşımı
- Doğrulama: örnek API çağrısının audit log’da görünmesi

## Workflow
- Hedefi belirle:
  - Forensics mi, compliance mı, debug mı?
- Policy yaz:
  - Her şeyi `RequestResponse` alma; gürültü ve maliyet dengesi kur.
- Hassas veri:
  - Body/log içindeki gizli alanların etkisini düşün.
- Saklama:
  - SIEM veya merkezi log sistemine nasıl taşınacak?
- Doğrulama:
  - Bilinçli API işlemi yap ve audit trail’i bul.

## Common mistakes
- Aşırı ayrıntılı policy ile API server yükünü artırmak.
- Audit log’u üretip retention/erişim modelini tasarlamamak.

## References
- `skills/k8s-core-events-audit`
- `cli/skills/agentic-threat-model`

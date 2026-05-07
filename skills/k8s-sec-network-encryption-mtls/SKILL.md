---
name: k8s-sec-network-encryption-mtls
description: "Pod’lar arası trafiği mTLS ile şifrelemek, servis kimliği doğrulaması kurmak veya “hangi katmanda kimlik ve şifreleme bitecek?” kararını vermek gerektiğinde kullan. Amaç: **service-to-service güvenini operasyonel olarak sürdürülebilir hale getirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- mTLS uygulanacak katman ve araç seçimi
- Sertifika/identity yaşam döngüsü yaklaşımı
- Doğrulama: gerçekten karşılıklı doğrulama ve şifreli trafik kanıtı

## Workflow
- Gereksinimi netleştir:
  - İç trafik şifreleme mi, identity enforcement mı, compliance mı?
- Katmanı seç:
  - Service mesh mi, app-level TLS mi, ingress/backend arası mı?
- Kimlik:
  - Her servis için cert/identity nasıl üretilecek ve yenilenecek?
- Operasyon:
  - Debug, latency, rollout ve certificate rotation etkileri.
- Doğrulama:
  - Şifreli handshake ve yetkisiz peer’in reddi test edilmeli.

## Common mistakes
- mTLS’i açıp sertifika sürekliliğini otomasyonsuz bırakmak.
- Sadece “encrypt”e bakıp identity doğrulamayı ihmal etmek.

## References
- `skills/k8s-net-service-mesh-intro`
- `skills/k8s-sec-tls-cert-manager`

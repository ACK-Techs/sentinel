---
name: obs-grafana-rbac
description: Grafana’da ekip bazlı erişim modeli kurmak (teams, folder permissions, service account yetkileri) veya “kim neyi görebilir/düzenleyebilir” sorusunu netleştirmek gerektiğinde kullan. Least‑privilege ve pratik izin hiyerarşisine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- RBAC taslağı: team → folder → permission matrisi (View/Edit/Admin)
- Service account yetki modeli (otomasyon için minimum kapsam)
- Doğrulama: örnek kullanıcılarla erişim testi senaryosu

## Workflow
- Varlıkları say:
  - Kaç ekip var? Kaç “ortak” dashboard var? (platform/infra vs product)
- Klasör stratejisi:
  - Folder’ları ownership’e göre ayır (team klasörü + shared klasör).
- Permission matrisi:
  - Default: çoğu kullanıcı View.
  - Dashboard sahipleri Edit.
  - Admin yetkisi minimum; özellikle datasource ve users yönetimi ayrı.
- Service account:
  - Provisioning/API otomasyonu için ayrı SA; sadece gereken folder/datasource kapsamı.
  - Token rotasyonu ve sızıntı önlemi.
- Uyum testi:
  - 2–3 örnek persona ile test: “görebilir mi?”, “edit edebilir mi?”, “datasource görebilir mi?”

## Common mistakes
- Herkese Editor vermek: drift ve incident sırasında yanlış değişiklik.
- Tek bir paylaşımlı folder’da her şeyi toplamak: izin yönetimi imkânsızlaşır.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-api-http`

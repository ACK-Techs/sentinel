---
name: agentic-approval-policy-design
description: Araç risk sınıfları ve etkileşimli ile CI ortamları için onay matrisini tasarlarken kullan.
---

## Amaç

**Read-only** ile **mutating** (dosya yazma, yama, shell) ayrımı; `sudo` veya ayrıcalık yükselten komutlar için **zorunlu onay** veya **engel**. Çok adımlı onay (önizleme + onay) önerilir. **YOLO / tam otomatik** mod varsa kullanıcıya **yüksek risk uyarısı** ve üretimde kapalı tutulması önerilir. Interactive oturum ile **CI non-interactive** davranışı farklı olmalıdır (CI’da genelde onay yok → riskli tool kapalı veya mock).

## Kapsam

### Dahil

- Policy seviyeleri (ör. locked / edit-only / yolo benzeri kavramların ürün içi adlandırması proje kararı).
- Hook ile birleşik davranış (`agentic-hooks-pre-post-tool`).

### Hariç

- İşletim sistemi RBAC’in tam tasarımı.

## Kurallar

- Mutating işlemler: diff önizleme veya özet kullanıcıya sunulması önerilir (`agentic-tools-filesystem-write`).
- Bilinmeyen shell komut kalıpları varsayılan **reddedilir** veya onay ister.
- Policy değişimi oturum içinde loglanır (`session_id`, `turn`).

## Kontrol listesi

- [ ] Her araç kategorisi için varsayılan onay/auto matrisi tablo halinde yazılı mı?
- [ ] CI profili insan onayı gerektirmiyor mu (veya sadece güvenli tool)?
- [ ] “Yolo” modu dokümante ve varsayılan kapalı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Kullanıcı sürekli reddediyor | Policy çok sıkı | Salt okuma için auto-onay genişlet |
| CI’da tehlikeli komut çalıştı | Non-interactive yolo | CI’da yolo yasakla |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../agentic-tools-base-contract/SKILL.md`
- `../agentic-hooks-pre-post-tool/SKILL.md`
- `../agentic-tools-bash-shell/SKILL.md`

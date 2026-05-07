---
name: obs-alertmanager-grouping
description: Alertmanager’da bildirim gürültüsünü azaltmak için grouping (group_by) ve zaman parametrelerini (`group_wait`, `group_interval`, `repeat_interval`) ayarlamak gerektiğinde kullan. “Aynı incident 100 mesaj oluyor” veya “çok geç haber veriyor” gibi denge problemlerine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Grouping stratejisi: hangi label’larla “incident” tanımlanacak?
- Zaman parametreleri için öneri seti (page vs notify kanalı ayrı)
- Doğrulama: örnek alert fırtınasında beklenen bildirim sayısı ve gecikme

## Workflow
- Kanal ayrımı yap:
  - Page kanalı: hızlı ama sınırlı tekrar.
  - Notify kanalı: daha fazla grup, daha az tekrar.
- “Incident anahtarı” belirle:
  - Genelde `alertname` tek başına yetmez; `service`, `cluster`, `env` gibi bağlayıcı ekle.
  - Aşırı detay (pod/instance) group_by’a girerse grup patlar.
- Zaman parametreleri:
  - `group_wait`: ilk mesajı kaç saniye bekletsin? (burst’ü toplamak)
  - `group_interval`: aynı group’a yeni alert gelince ne sıklıkla özet geçsin?
  - `repeat_interval`: aynı group hâlâ firing ise ne sıklıkla hatırlatsın?
- Ayarları route seviyesinde konumlandır:
  - Root’ta default; kritik rotalarda override.
- Doğrulama:
  - “N pod down” gibi çoklu alert üreten senaryoda kaç bildirim gidiyor ölç.

## Common mistakes
- `instance/pod` gibi yüksek kardinaliteyi group_by’a koymak: grouping işe yaramaz.
- Page kanalında kısa `repeat_interval`: pager fatigue.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`

---
name: obs-prometheus-federation
description: Bir “üst Prometheus”un başka Prometheus’lardan `/federate` ile **seçili metrikleri** çekmesi gerektiğinde kullan. Özellikle “federate endpoint”, “match[] seçimi”, “label çakışması”, “hangi metrikler federate edilmeli?” gibi sorularda federation tasarımını dar kapsamda ele alır.
---

## Purpose
Bu skill’in çıktısı:
- Üst Prometheus’ta bir `scrape_config` (metrics_path: `/federate` + `params.match[]`)
- Label stratejisi (source cluster/region label’ı, çakışma önleme)
- “Federate edilecek metrik seti” için net seçim kuralı (genel değil, somut)

## Workflow
- Federation’ın gerçekten doğru çözüm olup olmadığını kontrol et:
  - Amaç “merkezi sorgu” mu? (federation) yoksa “uzun süreli depolama” mı? (remote_write)
  - Amaç “tüm ham seriler” mi? Federation genelde **seçili** seri içindir.
- Üstten alta hedefleri tanımla:
  - Her alt Prometheus için hedef URL (auth/TLS placeholder ile).
  - Üst scrape job’ına “kaynak kimliği” label’ı ekle (örn. `cluster`).
- `match[]` stratejisi:
  - **Önce recording rule’ları federate et** (ör. `job:` ile başlayanlar).
  - Ham metrikleri federate edeceksen, sadece kritik ölçümler + düşük kardinalite.
  - `match[]` sayısını sınırlı tut; kontrol edilebilir bir allowlist yaz.
- Label çakışması ve tutarlılık:
  - Alt Prometheus’ta zaten `cluster` gibi label varsa overwrite riskini yaz.
  - Üstte `honor_labels` kararını bilinçli ver (genelde kapalı tutmak daha güvenli).
- Doğrulama:
  - Üst Prometheus’ta federate edilen serinin geldiğini doğrula (count + örnek seri).
  - İki kaynak karışmıyor mu: `cluster` label’ı üzerinden kontrol et.

## Failure modes
- Alt Prometheus down: üstte “gap” oluşur; alert’ler üstteyse yanlış alarm/kaçırma riski.
- Geniş `match[]`: üst Prometheus’ta beklenmeyen TSDB büyümesi ve scrape yükü.

## References
- `skills/cos-deploy-prometheus`
- `skills/obs-prometheus-remote-write`

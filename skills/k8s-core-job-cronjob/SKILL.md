---
name: k8s-core-job-cronjob
description: Kubernetes Job/CronJob ile batch işler ve zamanlı görevleri tasarlamak (retry/backoff, concurrencyPolicy, deadline) veya “cron job üst üste biniyor / job stuck oluyor” sorunlarını çözmek gerektiğinde kullan. Deployment değil; **tamamlanabilir iş semantiği** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Job/CronJob spec kararları: retry/backoff, timeouts, paralellik, concurrency
- Operasyon checklist’i: tarihçe temizliği, idempotency, gözlemleme
- Doğrulama: başarılı koşu + failure senaryosunda beklenen retry/stop davranışı kanıtı

## Workflow
- İş tipini seç:
  - Tek seferlik (Job) mi, periyodik (CronJob) mu?
- Idempotency:
  - İş tekrar çalışırsa ne olur? (Cron overlap/Retry → duplicate etkiler)
- Retry/backoff:
  - `backoffLimit` ve failure mode’a göre ayarla (kalıcı hatada sonsuz retry isteme).
  - `activeDeadlineSeconds` ile “sonsuz süren job”u kes.
- Cron özellikleri:
  - `concurrencyPolicy`: Allow/Forbid/Replace seçimi.
  - `startingDeadlineSeconds`: cluster downtime sonrası catch-up davranışı.
- Temizlik:
  - `successfulJobsHistoryLimit`/`failedJobsHistoryLimit` ile kaynak şişmesini önle.
- Doğrulama:
  - Bir run’da success koşulunu gör; failure’da retry sayısı ve stop şartı beklenen mi?

## Common mistakes
- ConcurrencyPolicy’yi default bırakmak: üst üste binmeler veri tutarsızlığı yaratır.
- Deadline/backoff koymamak: stuck job kaynak tüketir, kuyruk büyür.

## References
- `skills/k8s-core-events-audit`

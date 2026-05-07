---
name: obs-alertmanager-alert-lifecycle
description: Alert’in firing→resolved yaşam döngüsünü doğru yönetmek (resolve bildirimi, repeat davranışı, flapping etkisi) veya “alert kapanmıyor / sürekli tekrar ediyor / resolved mesajı gelmiyor” sorununu teşhis etmek gerektiğinde kullan. Kural yazmaktan çok **bildirim semantiği** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Lifecycle checklist’i: fire, group, repeat, resolve ve “ne zaman bildirim gider?”
- Flapping azaltma önerileri: rule `for`, grouping ve repeat ayarları birlikte
- Doğrulama: bir test alert’in açılıp kapanma mesajlarının tutarlı kanıtı

## Workflow
- “Kapanmıyor mu, yoksa notification state mi?”
  - Alert rule resolved oluyor mu? (Prometheus UI’da state)
  - Alertmanager hala aynı alert’i active görüyor mu?
- Resolve bildirimleri:
  - Receiver resolve mesajı gönderiyor mu? (kanala göre değişebilir)
  - Resolved mesajı isteniyor mu? (page kanalı için genelde evet)
- Flapping kaynaklarını ayır:
  - Rule tarafı: `for` süresi yok/çok kısa → flapping.
  - AM tarafı: grouping/repeat kısa → spam.
- Ayar kombinasyonu:
  - Page kanalı: daha uzun `repeat_interval`, daha net group_by.
  - Notify kanalı: daha agresif grouping, daha uzun `group_interval`.
- Doğrulama:
  - Kontrollü bir test alert üret: firing → resolved.
  - Açılış/kapanış mesajı aynı incident anahtarıyla eşleşiyor mu kontrol et.

## Common mistakes
- Flapping’i sadece Alertmanager’da çözmeye çalışmak: çoğu zaman `for` ve kural tasarımı gerekir.
- group_by’ı yanlış seçmek: resolved mesajı farklı “group”a düşer, kapanış görünmez.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-grouping`

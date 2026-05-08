---
name: agentic-memory-policy-user
description: Sentinel bellek katmanında extract, dreaming, redaksiyon ve politika uygulamalarını güvenli şekilde tasarlamak, işletmek veya iyileştirmek istendiğinde kullan.
---

## Bellek davranışı
`agentic-memory-policy-user` için temel ilke: bellek yazımı "yardımcı" ama "güvenli" olmalıdır. Sentinel’de extract, away summary, magic docs ve dreaming adımları tur sonu pipeline içinde birlikte çalışır; biri bozulduğunda diğerleri sessizce veri kirletmemelidir.

## Uygulama çerçevesi
1. **Politika seç:** `project` ve `user` modları için dosya kökünü ve erişim sınırını netleştir.
2. **Yazım güvenliği kur:** redaksiyon filtresi, write jail ve non-interactive kısıtlarını etkinleştir.
3. **Pipeline sırası koru:** post-turn hook -> extract -> away -> magic docs -> dreaming akışını bozmadan uygula.
4. **Eşik yönet:** dreaming için zaman/oturum eşiği ve stale lock temizliği belirle.
5. **Geri dönüş planı yap:** bozuk index veya migration hatasında yeniden inşa prosedürü bulunsun.

## Kontrol noktaları
- Hassas veri kalıpları (token, JWT, PEM, kubeconfig) bellekte maskelenmiş mi?
- Arka plan thread açıkken yarış durumları lock ile engelleniyor mu?
- Magic docs güncellemesi yanlış dosyaları etkilemiyor mu?

## İşletim notu
Bu sınıf skill’lerde değişiklik sonrası küçük bir repl oturumuyla gerçek extract dosyası üzerinden doğrulama yapılmalı.

## Referanslar
- `README.md`
- `documantations/INTEGRATION_SENTINEL_CLI_FROM_CLI_CLAUDE.md`
- `cli/skills/agentic-session-persistence/SKILL.md`
- `cli/skills/agentic-hooks-pre-post-tool/SKILL.md`

---
name: agentic-cli-autocomplete
description: CLI deneyimini üretim kalitesine taşımak için etkileşim, çıktı, ergonomi ve güvenli varsayılanlar tasarlanırken kullan.
---

## Ürün davranışı
`agentic-cli-autocomplete`, CLI yüzeyinde kullanıcı deneyimi ile işletim güvenilirliğini birlikte ele alır. Hedef: hatada bile anlaşılır çıkan, otomasyonda stabil çalışan ve etkileşimli kullanımda operatörü yormayan bir komut hattı.

## Tasarım yaklaşımı
1. **Kullanım bağlamını ayır:** TTY, pipe ve CI modlarında davranış farklılaştır.
2. **Sözleşme belirle:** output formatı, exit code ve hata metni deterministik olsun.
3. **Geri bildirim ver:** uzun süren işlerde progress, kısa işlerde sade çıktı kullan.
4. **Uyumluluk sağla:** shell completion, pager, i18n ve erişilebilirlik seçeneklerini feature flag ile yönet.
5. **Güvenli varsayılan koy:** dry-run, config validation ve crash report akışlarını açıkça yönet.

## Uygulama kontrolü
- Aynı komut JSON modunda parse edilebilir mi?
- `stdin` ile gelen veri interactive prompt akışını doğru bypass ediyor mu?
- Erişilebilirlik seçenekleri (`--no-color`, sade tablo) terminale göre uyarlanıyor mu?

## Skill-spesifik kararlar
- Autocomplete olustururken dinamik alt komutlar icin runtime completion destegi ekle. Bash/zsh/fish scriptlerini paketlemede surumlu dagit.

## Referanslar
- `cli/skills/agentic-cli-entrypoint/SKILL.md`
- `cli/skills/agentic-cli-user-errors/SKILL.md`
- `cli/skills/agentic-config-layers/SKILL.md`
- `cli/documantations/PROJECT_ROOT_PHASE2.md`

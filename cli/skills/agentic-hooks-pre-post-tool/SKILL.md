---
name: agentic-hooks-pre-post-tool
description: PreToolUse ve PostToolUse olayları için subprocess veya plugin sözleşmesini tanımlarken kullan.
---

## Amaç

Olaylar: **PreToolUse** (yürütmeden önce), **PostToolUse** (sonra). Harici süreç **stdin’e JSON** alır; **nonzero exit** = bloklama mı yalnız uyarı mı proje kararı (dokümante). **Timeout** zorunlu; stdout’tan JSON ile ek bağlam eklenebilir. Matcher: tool adı regex/prefix (`README` örnekleri Pywen hooks ile hizalı kavramsal olarak).

## Kapsam

### Dahil

- Ortak alanlar: `session_id`, `cwd`, `tool_name`, `tool_input`, `tool_response`.
- Güvenlik: hook komutu yapılandırmadan gelir; kötü niyetli config riski uyarısı.

### Hariç

- Uzaktan hook indirme.

## Kurallar

- Hook stdout stderr ayrımı; parse hatalarında güvenli varsayılan (blokla veya logla).
- `agentic-approval-policy-design` ile sıra: önce policy, sonra hook (veya tersi — tek doğruluk).
- Post hook başarısız: tool sonucunu geçersiz kılma kuralları.

## Kontrol listesi

- [ ] Hook timeout testi var mı?
- [ ] Kötü JSON stdin ile çökme yok mu?
- [ ] Hook path’leri abs veya cwd’ye göre dokümante mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Hook asılı kaldı | timeout | Süreci öldür, kullanıcıya bildir |
| Yanlış exit kod yorumu | Belge | Davranışı düzelt |

## İlgili belgeler ve skill'ler

- `../agentic-approval-policy-design/SKILL.md`
- `../agentic-cli-logging/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`

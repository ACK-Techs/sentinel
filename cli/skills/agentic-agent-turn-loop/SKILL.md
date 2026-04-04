---
name: agentic-agent-turn-loop
description: Ajan tur döngüsü, max_turns, durdurma koşulları ve SIGINT ile iptali tanımlarken kullan.
---

## Amaç

**Tur yaşam döngüsü**: kullanıcı/assistant/tool mesajları ile ilerleme; model **final metin** veya **tool_calls** üretir. **`max_turns`** üst sınırı aşılırsa dur ve kullanıcıya bildir. **Sonsuz döngü önleme**: aynı tool aynı arg ile tekrar → eşik veya kullanıcıya sor. **SIGINT**: mevcut LLM stream ve tool iptal edilir, tutarlı mesaj.

## Kapsam

### Dahil

- “Final answer” vs tool döngüsü netliği.
- Kullanıcı ara müdahalesi (iptal sonrası yeni girdi).

### Hariç

- Çoklu paralel ajan worker (ayrı tasarım).

## Kurallar

- `max_turns` yapılandırması `agentic-config-layers` ile okunur.
- Prompt injection savunması `agentic-prompt-injection-guardrails` ile birlikte düşünülür.
- Her tur sonunda isteğe bağlı hook `Stop` (proje kararı, Pywen desenine benzer).

## Kontrol listesi

- [ ] max_turns=0 veya negatif doğrulanmış mı?
- [ ] İptal sonrası kaynak sızıntısı (subprocess) temizleniyor mu?
- [ ] Tool hata sonucu modele geri besleniyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Sonsuz tool ping-pong | Tekrarlayan çağrı sayacı | Kullanıcıya özet + dur |
| Asılı stream | Timeout | Read timeout artır veya iptal |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../agentic-agent-tool-call-parse/SKILL.md`
- `../agentic-prompt-injection-guardrails/SKILL.md`
- `../agentic-cli-repl-vs-once/SKILL.md`

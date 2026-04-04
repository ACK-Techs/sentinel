---
name: agentic-cli-repl-vs-once
description: Etkileşimli REPL ile tek satır veya pipe modunu ayırt eden davranış ve slash komutlarını tanımlarken kullan.
---

## Amaç

**TTY kontrolü**: stdin terminal ise REPL veya çok satırlı sohbet; değilse **tek komut / pipe** modu (CI). **Slash komutları** (örn. `/exit`, `/agent`) varsa dokümante edilir; yoksa “yok” denir. **Non-interactive**: onay isteyen araçlar ya engellenir ya da policy `yolo`/`CI` profili ile kapatılır (`agentic-approval-policy-design`).

## Kapsam

### Dahil

- `sentinel chat "prompt"` vs `sentinel` boş argüman.
- EOF / Ctrl+D davranışı.

### Hariç

- WebSocket uzaktan REPL.

## Kurallar

- Pipe girdisinde kullanıcı onayı yoksa mutating tool varsayılan kapalı.
- REPL’de iptal sinyali (`SIGINT`) yarım turu güvenli kesmeli (`agentic-agent-turn-loop`).
- Session id REPL oturumu boyunca sabit.

## Kontrol listesi

- [ ] `test -t 0` senaryosu test edildi mi?
- [ ] CI job’da interaktif prompt beklenmiyor mu?
- [ ] Slash komutları çakışmıyor mu (normal metin ile)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| CI takılı kaldı | stdin kapalı mı | `--once` veya argüman zorunlu kıl |
| REPL başlamıyor | terminfo | `TERM` ve kütüphane bağımlılığı |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../agentic-cli-entrypoint/SKILL.md`
- `../agentic-agent-turn-loop/SKILL.md`
- `../agentic-approval-policy-design/SKILL.md`

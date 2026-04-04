---
name: agentic-session-persistence
description: Oturum dosyası yolu, format ve resume davranışını tanımlarken kullan.
---

## Amaç

**Konum**: örn. `~/.sentinel/sessions/` veya proje `.sentinel/` (proje kararı). **Format**: **jsonl** veya **sqlite** — şema sürüm alanı. **Resume**: çöküş sonrası son turdan devam veya salt okuma. **Bozuk dosya**: yedekten geri yükleme veya kullanıcıya “sıfırla” seçeneği. **Gizlilik**: disk şifreleme uyarısı; oturumda hassas içerik (`agentic-secrets-handling`).

## Kapsam

### Dahil

- Çoklu paralel oturum: `session_id` dosya adında.
- Migration: eski şema → yeni şema.

### Hariç

- Merkezi sunucu oturum deposu.

## Kurallar

- Oturum dosyası izinleri kullanıcıya özel (`chmod 600` önerisi).
- Trajectory ayrı dosya olabilir (`agentic-trajectory-recording`).
- Büyüme: rotasyon veya max tur prune.

## Kontrol listesi

- [ ] Bozuk jsonl satırı atlanıyor mu?
- [ ] Resume sonrası tool_call_id tutarlı mı?
- [ ] `.gitignore` oturum path’ini kapsıyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Disk dolu | df | Rotasyon |
| Şema uyumsuzluğu | version field | Migration çalıştır |

## İlgili belgeler ve skill'ler

- `../agentic-trajectory-recording/SKILL.md`
- `../agentic-agent-history-compaction/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`
- `../agentic-cli-logging/SKILL.md`

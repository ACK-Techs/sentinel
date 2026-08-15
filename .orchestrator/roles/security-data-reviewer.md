# Security & Data Reviewer

## Zorunlu alanlar

- Gateway bearer token ve secret-safe hata modeli.
- CLI config'te secret'ın YAML yerine env'de kalması.
- Tool approval, bash timeout/output limit, read-only bash.
- Prompt injection ve tool policy ayrımı.
- Memory/session redaction.
- Helm non-root, privilege escalation kapalı, read-only root filesystem.
- Image publish ve GHCR credential akışı.
- Gateway'in write/admin yüzeyine kaymaması.
- `SENTINEL_AUTO_APPROVE` veya eşdeğer otomatik onayın sessizce açılmaması.

Kritik bulguda pass verme. Production, paid provider, cluster mutation, image publish veya gateway-write-expansion kullanıcı/platform onayı ister.

---
name: agentic-tools-bash-shell
description: Shell yürütmede cwd, timeout, çıktı kırpma ve sudo politikasını güvenli şekilde tanımlarken kullan.
---

## Amaç

**cwd**: repo kökü veya kullanıcı onaylı dizin; `cd` ile kaçışı sınırla. **Timeout** zorunlu; çıktı **max karakter** ile kırp. **`sudo`**: varsayılan reddet veya ayrı onay katmanı. **OS farkı**: Windows’ta PowerShell/cmd ayrımı proje kararı. **Arka plan iş** önerisi: dikkatli kullan veya yasak (zombie süreç); Pywen deseninde olduğu gibi PID takibi dokümante.

## Kapsam

### Dahil

- Allowlist/denylist örnek komut kalıpları (yüksek risk: `rm -rf /`, `curl | bash`).
- `grep`/`find` yerine özel araçlara yönlendirme (danışmanlık skill metni).

### Hariç

- Konteyner içi rootless tam izolasyon (sandbox skill).

## Kurallar

- Ortam değişkenleri minimal temiz set veya kullanıcı onaylı inherit (secret sızıntısı riski).
- `agentic-threat-model` ve `agentic-approval-policy-design` ile hizalı.
- Çıktıda terminal kontrol karakterleri filtrele (güvenlik).

## Kontrol listesi

- [ ] Timeout testi asılı komutta geçiyor mu?
- [ ] Çok satırlı çıktı truncate mesajı ekliyor mu?
- [ ] CI’da bash tool kapalı mı veya sandbox’ta mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Exit code 127 | PATH | `doctor` ortam |
| OOM | Büyük çıktı | Daha agresif limit |

## İlgili belgeler ve skill'ler

- `../agentic-approval-policy-design/SKILL.md`
- `../agentic-threat-model/SKILL.md`
- `../agentic-hooks-pre-post-tool/SKILL.md`
- `../agentic-sandbox-hardening-reference/SKILL.md`

---
name: agentic-tools-filesystem-read
description: Dosya okumada path normalizasyonu, symlink, repo dışına çıkma ve boyut sınırlarını uygularken kullan.
---

## Amaç

**Path normalizasyonu**: `..` ve symlink çözümü; hedef **trusted root** (repo kökü) dışına çıkışı engelle veya açık onay iste. **Binary dosyalar**: içerik yerine “binary atlandı” + boyut. **Boyut sınırı** ve **encoding** (UTF-8 varsayılan; hata durumunda replacement veya red).

## Kapsam

### Dahil

- Çoklu dosya okuma (batch) rate limit önerisi.
- `.git` ve `.env` okuma hassasiyeti (log’da path dikkat).

### Hariç

- Büyük medya streaming (ayrı araç).

## Kurallar

- Okuma bile olsa kullanıcıya hangi path okunduğunu özetle (şeffaflık).
- Symlink zinciri ile jail break önlemi kodda testli.
- `agentic-tools-filesystem-write` ile tutarlı kök tanımı.

## Kontrol listesi

- [ ] `../../../etc/passwd` senaryosu bloklanıyor mu?
- [ ] 100MB dosya denemesi güvenli şekilde reddediliyor mu?
- [ ] Encoding hatası anlamlı mesaj veriyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| EPERM | İzin | Kullanıcıya sudo önerme (dikkatli) |
| ENOENT | Typo | Path doğrula |

## İlgili belgeler ve skill'ler

- `../agentic-tools-filesystem-write/SKILL.md`
- `../agentic-threat-model/SKILL.md`
- `../agentic-tools-base-contract/SKILL.md`

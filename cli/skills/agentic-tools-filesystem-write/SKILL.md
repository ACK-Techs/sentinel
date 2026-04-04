---
name: agentic-tools-filesystem-write
description: Dosya yazma ve yamada atomik yazma, yedekleme ve onay ile .git koruması önerilerini uygularken kullan.
---

## Amaç

**Atomik yazma**: temp dosya + rename. **Yedekleme**: `.bak` veya git stash önerisi (proje kararı). **`.git` içine yazma**: varsayılan uyarı/engel. **Onay**: mutating işlem `agentic-approval-policy-design` kapısından geçer. **Diff önizleme** kullanıcıya kısa özet veya tam diff (boyut sınırlı).

## Kapsam

### Dahil

- Patch / apply_patch benzeri tek string argüman güvenliği.
- Çakışan eşzamanlı yazım (kilitleme veya son yazar kazanır — dokümante).

### Hariç

- Büyük binary deploy.

## Kurallar

- Yazmadan önce path jail (read skill ile aynı kök).
- Silme işlemi ayrı risk sınıfı.
- Trajectory’de içerik tam yazılmayabilir (`agentic-trajectory-recording`).

## Kontrol listesi

- [ ] Yarım yazım sonrası disk tutarlı mı?
- [ ] Onay reddinde dosya değişmedi mi?
- [ ] Büyük diff kullanıcıya özetleniyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Disk dolu | errno | Alan temizliği |
| İzin reddi | umask | Kullanıcıya dizin öner |

## İlgili belgeler ve skill'ler

- `../agentic-approval-policy-design/SKILL.md`
- `../agentic-tools-filesystem-read/SKILL.md`
- `../agentic-tools-base-contract/SKILL.md`
- `../agentic-hooks-pre-post-tool/SKILL.md`

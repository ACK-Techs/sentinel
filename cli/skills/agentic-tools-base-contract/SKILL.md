---
name: agentic-tools-base-contract
description: Her aracın name, description, JSON şeması ve execute sözleşmesini standartlaştırırken kullan.
---

## Amaç

Her araç: **`name`**, **`description`**, **`parameter_schema` (JSON Schema)`**, **`execute`** → standart sonuç nesnesi: başarı bayrağı, metin veya yapı sonuç, hata mesajı, isteğe bağlı display. **Zaman aşımı** ve **maksimum çıktı boyutu** zorunlu üst sınırlar. Hata nesnesi: makine okunur `code` + insan mesajı.

## Kapsam

### Dahil

- Senkron görünen `async execute` deseni (Python) veya eşdeğeri.
- Risk seviyesi (`agentic-approval-policy-design` ile bağlantı).

### Hariç

- Her domain özel iş kuralı.

## Kurallar

- Uzun çıktı önce kırp, sonra özet öner (token tasarrufu).
- Tool içi subprocess için ayrı timeout.
- Sonuçlar log’da secret içermemeli.

## Kontrol listesi

- [ ] Tüm araçlar şema ile doğrulanıyor mu?
- [ ] Timeout aşımında process kill ediliyor mu?
- [ ] Çıktı boyutu sınırı testi var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| execute çöküyor | Exception wrap | Modele sanitize hata |
| Çıktı devasa | Limit | Kırp + devam sorusu |

## İlgili belgeler ve skill'ler

- `../agentic-tools-bash-shell/SKILL.md`
- `../agentic-tools-filesystem-read/SKILL.md`
- `../agentic-tools-filesystem-write/SKILL.md`
- `../agentic-agent-tool-call-parse/SKILL.md`
- `../agentic-mcp-tool-mapping/SKILL.md`

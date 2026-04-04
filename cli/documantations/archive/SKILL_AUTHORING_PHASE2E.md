# Faz 2.E Skill Yazım Uyum Özeti

Bu not, `SKILL_CATALOG_PHASE2.md` ile mevcut `agentic-*` skill gövdelerinin uyumunu kısa bir referans tablosu ile özetler. Faz 2.E itibarıyla katalog ile çelişen ek bir kural tespit edilmedi; katalog şartnamesi geçerli tek kaynak olmaya devam eder.

## Referans örnekler

| İhtiyaç | Örnek skill | Neye bakılır |
|---------|-------------|--------------|
| Mimari veya genel yönlendirme | `../skills/agentic-cos-advisor-overview/SKILL.md` | Frontmatter, amaç/kapsam dengesi, Faz 1'e yönlendirme |
| İşletim komut referansı | `../skills/agentic-microk8s-ops-reference/SKILL.md` | Adımlar, yetki uyarıları, geri dönüş tablosu |
| Bileşen teşhisi | `../skills/agentic-troubleshoot-grafana/SKILL.md` | Checklist, tipik hata, relation ve ingress zinciri |
| Güvenlik veya politika skill'i | `../skills/agentic-approval-policy-design/SKILL.md` | Kuralların netliği ve risk sınıfları |

## Uyum onayı

- `name:` değeri klasör adı ile birebir olmalı.
- Zorunlu başlık sırası korunmalı: `Amaç`, `Kapsam`, `Kurallar` veya `Adımlar`, `Kontrol listesi`, `Hata ve geri dönüş`, `İlgili belgeler ve skill'ler`.
- Göreli yollar `SKILL_CATALOG_PHASE2.md` içindeki kurala göre yazılmalı.
- Faz 1 ile çelişen yeni komut veya iddia üretilecekse skill gövdesi yerine Faz 1 referansına yönlendirme yapılmalı.

## Sonraki gözden geçirme

Yeni bir `agentic-*` skill eklendiğinde önce katalog satırı, sonra `cli/skills/<id>/SKILL.md` gövdesi güncellenmelidir. Gerekirse bu dosyaya yeni örnek satırı eklenebilir, ancak kuralları değiştiren belge hâlâ `SKILL_CATALOG_PHASE2.md` olur.

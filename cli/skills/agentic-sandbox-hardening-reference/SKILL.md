---
name: agentic-sandbox-hardening-reference
description: Codex-tarzı sandbox hedefleri ve POC için minimum shell/dosya önlemlerini referans alarak planlarken kullan.
---

## Amaç

**Hedef (referans)**: macOS Seatbelt, Linux namespaces/landlock benzeri politikalar — `agentic/codex-main/codex-rs/core/README.md` ve ilgili crate’ler yüksek seviye özet. **Pywen boşluğu**: ağır OS sandbox dosyada yok; mitigasyon **onay + hook + kısıtlı cwd** (`agentic-tools-bash-shell`). **POC minimum liste**: timeout, çıktı limiti, repo kökü jail, riskli komut reddi, (varsa) konteyner içi çalıştırma.

## Kapsam

### Dahil

- Üretim yol haritası için ADR girdisi (`agentic-adr-template`).
- Tehdit eşlemesi `agentic-threat-model`.

### Hariç

- Kernel modülü veya özel güvenlik ürünü entegrasyonu.

## Kurallar

- Sandbox olmadan “güvenli” iddiası verme; kabul edilen riski yaz.
- POC ile üretim politikasını karıştırma.
- Upstream Codex davranışı değişebilir; sabitleme için sürüm notu.

## Kontrol listesi

- [ ] Hangi OS’lerde hangi mekanizma hedefleniyor?
- [ ] Mevcut onay/hook katmanı yeterlilik analizi yapıldı mı?
- [ ] Performans etkisi ölçüldü mü?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Sandbox kırıldı | policy | Red hat / güvenlik review |
| UX çok ağır | false positive | İnce ayar whitelist |

## İlgili belgeler ve skill'ler

- `../agentic-threat-model/SKILL.md`
- `../agentic-tools-bash-shell/SKILL.md`
- `../agentic-reference-agentic-folder/SKILL.md`
- `../agentic-approval-policy-design/SKILL.md`

---
name: agentic-cos-catalogue-endpoints
description: Catalogue ve proxied uçların keşfi ile kullanıcıya doğru URL iletimi için Juju komut sırası verirken kullan.
---

## Amaç

**Catalogue birimi**: `juju show-unit catalogue/0` (veya uygun unit) çıktısındaki **`url`** listelerini okuma rehberi — Faz 1 tutorial notlarıyla uyumlu. **Traefik**: `show-proxied-endpoints` ile birlikte değerlendir; bazı uçlar yalnız Catalogue’da görünebilir (`../../skills/cos-deploy-grafana/SKILL.md` notu). Kullanıcıya yalnız doğrulanmış URL’leri ilet; tahmin etme.

## Kapsam

### Dahil

- URL çıkarımı adımları (komut → alan → anlam).
- HTTP vs HTTPS dikkat notu.

### Hariç

- Özel branding / vanity domain.

## Kurallar

- Komut örnekleri Faz 1 skill’lerle aynı charm/unit isimlerini kullanır.
- Çıktı çok uzunsa ilgili bölümü grep ile (araç politikasına uygun).
- Yanlış model uyarısı: `juju switch cos`.

## Kontrol listesi

- [ ] Catalogue unit sağlıklı mı?
- [ ] URL’ler tarayıcıda açılıyor mu (kullanıcı doğrulaması)?
- [ ] Traefik ile çakışan bilgi var mı (ikisini karşılaştır)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| show-unit boş | Model / unit adı | `juju status` |
| URL 404 | Path / ingress | `../agentic-troubleshoot-traefik-ingress` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-grafana/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`

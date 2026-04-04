---
name: agentic-dependency-licensing
description: Üçüncü parti bağımlılıkların lisans envanteri ve agentic/ kaynak kesitlerinden türetme risklerini yönetirken kullan.
---

## Amaç

Bağımlılık envanteri şablonu; MIT / Apache-2.0 / GPL ailesi gibi lisansların **birlikte dağıtım** etkilerinin özeti; workspace `agentic/` altındaki örnek kodun **telif farkındalığı** (kopyalama yerine desen öğrenme, lisans dosyalarını okuma).

## Kapsam

### Dahil

- `pip`/`uv` bağımlılık listesi + lisans sütunu (ör. `pip-licenses`, SBOM araçları — araç seçimi proje kararı).
- Yasaklı veya şirket politikasına aykırı lisans için durdurma prosedürü.

### Hariç

- Hukuki yorum; belirsizlikte hukuk/uyumluluk sürecine sevk.

## Kurallar

- Üretim bağımlılıklarında lisans sütunu boş bırakılmaz; “UNKNOWN” ise paket sahibinden doğrula.
- GPL ile kapalı ürün birleşimi gibi kombinasyonlarda **erken uyarı**; karar kaydı önerilir (`agentic-adr-template`).
- `agentic/` içinden kod kopyalanacaksa kaynak LICENSE dosyasını oku ve `agentic-dependency-licensing` + `agentic-reference-agentic-folder` ile tutarlı not düş.

## Kontrol listesi

- [ ] Envanter tablosu (paket, sürüm, lisans) güncel mi?
- [ ] Dağıtımda birlikte gelen native/binary parçalar listelendi mi?
- [ ] Yasaklı lisans listesi ekip politikasıyla eşleşiyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Lisans çakışması | İki paketin şartları | Alternatif kütüphane veya istisna onayı |
| SBOM üretimi başarısız | Araç sürümü / özel index | Proje kararıyla sabit komut dokümante et |

## İlgili belgeler ve skill'ler

- `../documantations/SKILL_CATALOG_PHASE2.md`
- `../agentic-project-charter/SKILL.md`
- `../agentic-reference-agentic-folder/SKILL.md`

---
name: agentic-faz3-no-remote-telemetry
description: Faz 3 kapsamında uzaktan kullanım analitiği veya telemetri kodu eklenmeyeceğini doğrularken veya dokümante ederken kullan.
---

## Amaç

**Faz 3** iç kullanım teslimatında **ürün telemetrisi** (sürüm ping’i, anonim kullanım, çökme raporu gönderimi vb.) **kod olarak eklenmez**. Yerel log ve kullanıcı bilinçli ağ çağrıları (LLM API) bu politikaya dahil değildir.

## Kapsam

### Dahil

- README veya `documantations/` içinde tek cümle: dışarıya otomatik analitik gönderimi yok.
- Kod incelemesinde: yeni `requests`/`httpx` ile “metrics.” / analytics host’larına istek yok (istisna: açıkça kullanıcı tarafından yapılandırılmış LLM uçları).

### Hariç

- Gelecekteki opt-in telemetri tasarımı (`agentic-telemetry-optional` ile ilişkili, **sonraki faz**).

## Kurallar

- **Ekleme yapılmaz** = Faz 3 PR’larında telemetri SDK veya arka plan gönderim döngüsü yok.
- `agentic-telemetry-optional` skill’i **referans** kalır; Faz 3’te uygulanmaz.

## Kontrol listesi

- [ ] README’de “şu an gönderim yok” ifadesi var mı?
- [ ] Gereksiz dış HTTP (analitik) yok mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Karışıklık: log vs telemetri | Yerel dosya / stderr | Dokümantasyonda ayrım |

## İlgili belgeler ve skill'ler

- `../../documantations/ROADMAP_PHASE3_5.md`
- `../../documantations/IMPLEMENTATION_PLAN_PHASE3.md`
- `../agentic-telemetry-optional/SKILL.md` (ileride)

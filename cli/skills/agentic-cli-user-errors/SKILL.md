---
name: agentic-cli-user-errors
description: Son kullanıcıya Türkçe hata şablonları, çıkış kodu anlamı ve önerilen sonraki komutu tanımlarken kullan.
---

## Amaç

Her hata sınıfı için **kısa Türkçe mesaj** + **`--verbose` ile teknik detay** (İngilizce traceback kabul edilebilir). **Exit code ↔ anlam** tablosu README’de. **Sonraki komut önerisi**: örn. bağlantı hatasında “`doctor` çalıştırın”, auth’ta “env anahtarını kontrol edin”.

## Kapsam

### Dahil

- `LLM_PROVIDERS.md` hata sınıfları ile hizalı mesajlar.
- JSON olmayan kullanıcı çıktılarında renk/emoji proje stiline göre.

### Hariç

- Uluslararası i18n çeviri dosyaları (ilk sürümde opsiyonel).

## Kurallar

- 401/403 mesajında anahtar veya token değeri asla yazdırılmaz.
- İç hata kodları (`ERR_CONFIG_PARSE`) stabil ve dokümante olmalı.
- Maksimum 2 otomatik retry sonrası kullanıcıya dur (`PROJECT_ROOT_PHASE2` protokolü).

## Kontrol listesi

- [ ] En sık 10 hata için metin hazır mı?
- [ ] `--verbose` olmadan stack yok mu?
- [ ] Exit code shell script’lerde kullanılabiliyor mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Kullanıcı mesajı belirsiz | Hata sınıfı | Tabloyu genişlet |
| Çok teknik jargon | Review | Türkçe sadeleştir |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../documantations/PROJECT_ROOT_PHASE2.md`
- `../agentic-llm-retries-timeouts/SKILL.md`
- `../agentic-cli-entrypoint/SKILL.md`

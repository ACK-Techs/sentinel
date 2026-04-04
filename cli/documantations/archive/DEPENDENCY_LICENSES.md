# Faz 2.A Baslangic Bagimlilik ve Lisans Envanteri

Bu belge, `sentinel-coming/cli/pyproject.toml` icindeki ilk Faz 2.A bagimliliklarini ve referans kaynak lisans notlarini kaydeder. Amaç, Faz 2.B ve sonrasi gelismelerde lisans riski büyumeden once temel tabloyu sabitlemektir.

## Paket envanteri

| Paket | Kapsam | Surum araligi | Lisans | Not |
|------|--------|---------------|--------|-----|
| `hatchling` | build-system | `>=1.27.0` | MIT | Paketleme altyapisi |
| `httpx` | runtime | `>=0.28,<1.0` | BSD-3-Clause | Uzak veya lokal HTTP tabanli LLM istemcisi icin planlanan temel tas |
| `pydantic` | runtime | `>=2.11,<3.0` | MIT | Config ve veri sozmelesi modelleri icin planlandi |
| `PyYAML` | runtime | `>=6.0,<7.0` | MIT | YAML config dosyalari icin planlandi |
| `rich` | runtime | `>=14.0,<15.0` | MIT | CLI cikti bicimleme ve hata sunumu icin planlandi |
| `pytest` | optional `dev` | `>=8.3,<9.0` | MIT | Birim ve entegrasyon testleri |
| `ruff` | optional `dev` | `>=0.11,<0.12` | MIT | Lint ve stil kontrolu |

## Yasakli lisans kontrolu

- Varsayilan politika: `GPL-*`, `AGPL-*`, `SSPL`, `Commons Clause` ve lisansi `UNKNOWN` olan paketler inceleme tamamlanmadan kabul edilmez.
- Faz 2.A kapsaminda secilen bagimliliklarda bu yasakli siniflardan bilinen bir lisans bulunmuyor.
- Lisansi belirsiz yeni paket eklenirse `Sifir Varsayim Kurali` geregi durulur, alternatif kutuphane veya uyumluluk onayi beklenir.

## Referans kod tabanlari ve lisans notu

| Kaynak | Rol | Lisans durumu | Uygulama notu |
|--------|-----|---------------|---------------|
| `agentic/Pywen-dev` | Birincil Python referansi | MIT (`agentic/Pywen-dev/LICENSE`) | Dogrudan vendor edilmez; desen ve API sekli referansi |
| `agentic/codex-main` | TS/SDK desen referansi | Apache-2.0 (`agentic/codex-main/LICENSE`) | Uyarlama yapilirsa NOTICE ve attribution kontrol edilir |
| `agentic/claude` | CLI UX ve approval pattern referansi | Lisans dosyasi bu workspace kesitinde gorulmedi | Dogrudan kod kopyalamadan once lisans netlestirilmelidir |

## Denetim notlari

- Bu tablo dogrudan `pyproject.toml` ile senkron tutulmalidir.
- Daha sonra otomatik tarama icin `pip-licenses`, SBOM veya benzeri bir arac eklenebilir; Faz 2.A icin not olarak kaydedildi, entegrasyon henuz eklenmedi.
- Transitive bagimliliklar bu tabloda yoktur; Faz 2.E CI asamasinda ayri tarama eklenmesi onerilir.

## Ilgili belgeler

- `PROJECT_ROOT_PHASE2.md`
- `IMPLEMENTATION_PLAN_PHASE2.md`
- `LLM_PROVIDERS.md`

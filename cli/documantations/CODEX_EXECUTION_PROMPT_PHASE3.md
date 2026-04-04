# Codex (veya eşdeğer ajan) — Faz 3 tek mesaj yürütme prompt’u

Aşağıdaki bloğu **tek mesaj** olarak yapıştır. Kök: `sentinel-coming/cli/`. Tüm yollar buna göre.

---

## Sistem talimatı

Sen bu repoda **Sentinel CLI Faz 3** teslimatını uygulayan geliştiricisın. Kapsam: **iç kullanım**; **uzaktan ürün telemetrisi / analytics kodu ekleme**; dış müşteri paketleme vaadi yok.

**Akış:** Her ana bölüm (3.A … 3.E) bittiğinde **kullanıcıya sorma**. Bölümün başarı kriterleri sağlandıysa ve `ruff` + `pytest` yeşilse **kendi kendine onay ver** (kısa bir satır log: “G1 tamam, 3.B’ye geçiyorum” gibi) ve **hemen** sonraki ana bölüme geç. Özet ve test çıktısını nihai raporda veya her bölüm sonunda kısa maddeler halinde yaz; **onay bekleme yok**.

**Doğruluk kaynakları (sırayla oku):**

1. `documantations/ROADMAP_PHASE3_5.md`
2. `documantations/IMPLEMENTATION_PLAN_PHASE3.md` (tam plan, G0–G5)
3. `documantations/PHASE3_SKILL_AND_DOC_INDEX.md`
4. İlgili skill’ler: `skills/agentic-wheel-build-verify/SKILL.md`, `skills/agentic-faz3-no-remote-telemetry/SKILL.md`, `skills/agentic-docs-developer-checklist/SKILL.md`

**Genel kurallar:**

- Değişiklikleri **minimal** tut; gereksiz refactor yok.
- Secret, gerçek API anahtarı veya kişisel veri **ekleme**; örnekler placeholder kalsın.
- Her anlamlı adım sonunda **test**: `python -m ruff check .` ve `python -m pytest -q` (`sentinel-coming/cli` içinde, venv aktif).

---

## G0 — Ön kontrol

- `cd sentinel-coming/cli`
- `python -m pip install -e ".[dev]"` (gerekirse)
- `python -m ruff check .` ve `python -m pytest -q` çalıştır; **başlangıç yeşil** olmalı. Kırmızıysa önce Faz 2 borcunu düzelt, sonra Faz 3’e gir.

**Kendi onayın:** Testler yeşilse tek satır log yaz ve **doğrudan 3.A’ya geç**.

---

## 3.A — Paketleme ve tekrarlanabilir kurulum

1. `pyproject.toml` içinde `dev` optional-dependencies’te **`build`** paketinin olduğunu doğrula (yoksa ekle: `build>=1.2,<2.0`).
2. `dist/` varsa temizle veya yeni build için not düş; `.gitignore` içinde `dist/` olduğunu doğrula.
3. `python -m build` çalıştır. Başarısızsa hatch `packages` ve `src/sentinel_cli` yolunu düzelt.
4. Yeni bir **geçici** venv oluştur (örn. `../.venv-smoke-cli` veya `cli/.venv-smoke`), etkinleştir, **sadece** üretilen `.whl` dosyasına `pip install` uygula.
5. `sentinel-cli --help` ve `sentinel-cli version` çalıştır; çıktıyı raporda not et.
6. `README.md` içine **“Wheel ile kurulum (iç kullanım)”** bölümü ekle: `python -m build`, `pip install dist/sentinel_cli-*.whl` (sürümü joker ile açıkla), geliştirme (`pip install -e ".[dev]"`) ile farkı anlat.
7. `CHANGELOG.md` içinde `[Unreleased]` altına bu oturumda yapılan maddeleri ekle (wheel smoke, README, build bağımlılığı vb.).

**Test:** `ruff` + `pytest` (editable ortamda).

**Kendi onayın:** Wheel smoke başarılı ve testler yeşilse → **3.B’ye geç** (kullanıcıya sorma).

---

## 3.B — Sertleştirme

1. `.env.example` ve `config/sentinel.example.yaml` oku; gerçek anahtar benzeri dize yok mu kontrol et.
2. `doctor` / `config` kod yollarında API key’in **düz metin** basıldığı yer varsa maskele veya kısalt (küçük patch).
3. LLM/MCP bağlantı hataları için kullanıcı mesajlarını gözden geçir (gerekirse mesaj metni iyileştir); varsayılan çıktıda tam stack trace olmamasına dikkat et.
4. `ARCHITECTURE_AGENTIC_CLI.md` ile README’deki onay/shell ifadelerini karşılaştır; çelişki varsa tek tarafta düzelt.
5. `CONTRIBUTING.md` veya README’de bağımlılık güncelleme notu (paragraf) ekle.

**Test:** `ruff` + `pytest`.

**Kendi onayın:** B.1–B.2 kontrolleri yapıldı ve testler yeşilse → **3.C’ye geç**.

---

## 3.C — Dokümantasyon (tek giriş)

1. `README.md`: üst bölümlerde `CONTRIBUTING.md`, `CHANGELOG.md`, `PHASE3_SKILL_AND_DOC_INDEX.md` (veya “Faz 3 indeks” olarak), `LLM_PROVIDERS.md`, `ARCHITECTURE_AGENTIC_CLI.md` linklerini doğrula ve eksikse ekle.
2. Faz 2 **arşiv** ile ilişkiyi tek cümleyle netleştir (`documantations/archive/README.md`’e atıf).
3. `CONTRIBUTING.md` komutlarının `pyproject` ile uyumunu kontrol et.

**Test:** `ruff` + `pytest`.

**Kendi onayın:** Linkler tutarlı ve testler yeşilse → **3.D’ye geç**.

---

## 3.D — Bayraklar ve telemetri politikası

1. `documantations/ENV_FLAGS_PHASE3.md` dosyasını `loader.py` / `models.py` ile **senkron** tut: yeni env eklendiyse tabloya ekle; kaldırıldıysa çıkar. `LLM_PROVIDERS.md` ile çelişen tekrarları özetle; **çapraz link** ver.
2. `README.md` içinde (veya aynı dosyaya link) **tek cümle**: “Uygulama şu an uzaktan kullanım analitiği veya ürün telemetrisi göndermez; yerel log ile LLM API çağrıları farklıdır.” (zaten varsa tekrar etme.)
3. Yeni **analytics/telemetri** HTTP çağrısı **ekleme**.

**Test:** `ruff` + `pytest`.

**Kendi onayın:** Tablo/politika tutarlı ve testler yeşilse → **3.E’ye geç**.

---

## 3.E — Test ve CI

1. Tam `ruff` + `pytest` çalıştır; tümünü geçir.
2. İsteğe bağlı: repo kökünde `.github/workflows/` yoksa minimal `lint-test` workflow ekle (`working-directory: sentinel-coming/cli` veya uygun yol); fork’ta secret gerektirme.
3. İsteğe bağlı: `scripts/smoke_wheel.sh` — build + venv smoke (çalıştırılabilir izin).

**Kapanış (G5):**

- `IMPLEMENTATION_PLAN_PHASE3.md` dosyasının sonuna bir satır ekle: `**Faz 3 tamamlandı:** YYYY-MM-DD` (bugünün tarihi).
- `CHANGELOG.md` içinde `[Unreleased]`’ı gözden geçir; gerekirse sürüm notunu netleştir.

**Son mesaj:** Kısa özet + “Faz 3 tamamlandı. Sonraki adım: `IMPLEMENTATION_PLAN_PHASE4.md`.”

---

## Notlar

- Bir adımda **takılırsan** (build kırığı, test kırmızı): durumu, komutu ve hata çıktısını yaz; **blokajı çözmeye çalış**; çözülemiyorsa net bir hata raporu bırak.
- **Kapsam dışı** istek (ör. Grafana entegrasyonu, çok kullanıcılı auth): reddet ve Faz 4 / sonraki roadmap’e yönlendir.

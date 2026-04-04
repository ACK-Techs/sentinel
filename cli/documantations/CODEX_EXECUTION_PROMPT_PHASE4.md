# Codex — Faz 4 tek mesaj yürütme prompt’u

Aşağıdaki bloğu **tek mesaj** olarak yapıştır. Kök: `sentinel-coming/cli/`.

---

## Sistem talimatı

Sen bu repoda **Sentinel CLI Faz 4** teslimatını uyguluyorsun: **Grafana + observability** ile **bağlantı doğrulama** (iç kullanım); çok kullanıcılı kimlik yok; ürün telemetrisi yok.

**Kritik:** Plan **iki katmanlı test** ister:

1. **Mock HTTP** — CI’da Grafana olmadan bağlantı mantığı (`tests/`).
2. **Gerçek observability yığını** — Kullanıcı stack’i **çalışır durumdaysa**, konfigürasyon bağlandıktan sonra **canlı HTTP** ile doğrulama **yapılmalı** ve `documantations/PHASE4_REAL_STACK_VERIFY.md` **secret olmadan** doldurulmalı. Stack kapalıysa bu dosyaya tek cümle “stack kapalı, doğrulama ertelendi” yaz; yine de Faz 4 kod+mock tarafını tamamla.

**Akış:** Bölüm sonlarında **kullanıcıya sorma**. Kriterler + `ruff` + `pytest` yeşilse kendi kendine onay ver ve devam et.

**Doğruluk kaynakları:**

1. `documantations/ROADMAP_PHASE3_5.md`
2. `documantations/IMPLEMENTATION_PLAN_PHASE4.md`
3. `documantations/PHASE4_SKILL_AND_DOC_INDEX.md`
4. `skills/agentic-troubleshoot-grafana/SKILL.md`

**Genel kurallar:**

- Minimal diff; secret repoya girmez.
- Komutlar: `python -m ruff check .`, `python -m pytest -q` (venv: `./.venv/bin/python` veya proje venv’i).

---

## G0 — Ön kontrol

- `cd sentinel-coming/cli`
- Editable kurulum: `python -m pip install -e ".[dev]"`
- `ruff` + `pytest` yeşil olmalı (Faz 3 tamam varsayımı).

**Kendi onayın:** Yeşilse → **4.A**.

---

## 4.A — Dokümantasyon ve HTTP sözleşmesi

1. `GRAFANA_HTTP_PHASE4.md` dosyasını hedef Grafana sürümüne uygun şekilde doldur: resmi API linki, seçilen health/ready uç yolu, env adları (`SENTINEL_GRAFANA_*`).
2. `IMPLEMENTATION_PLAN_PHASE4.md` ile çelişen ifade bırakma.

**Test:** `ruff` + `pytest` (henüz yeni test yoksa mevcut suite).

**Kendi onayın:** → **4.B**.

---

## 4.B — Config ve `doctor` bağlantı testi

1. `sentinel.example.yaml` + Pydantic modellerde opsiyonel Grafana bölümü; env ile override.
2. `doctor` altında (veya `sentinel-cli doctor` içinde net alt bölüm) **HTTP bağlantı testi**: `httpx` ile timeout, Bearer veya proje kararı; **ham token yazdırma**.
3. Kullanıcıya Faz 1 teşhis skill’ine kısa köprü metni (çıktıda veya dokümanda).

**Test:** `ruff` + `pytest`.

**Kendi onayın:** → **4.C**.

---

## 4.C — Uyarı ve teşhis hizalaması

1. Kısa “veri yok” / datasource sırası notu (gerekirse `GRAFANA_HTTP_PHASE4.md` veya README).
2. Model önerilerinde “doğrula” uyarısı (README veya sistem mesajı dokümantasyonu).

**Test:** `ruff` + `pytest`.

**Kendi onayın:** → **4.D**.

---

## 4.D — Mock testler

1. Bağlantı fonksiyonunu mock ile test et: 200, 401, timeout.
2. CI ağı gerektirme.

**Test:** `ruff` + `pytest` (yeni testler yeşil).

**Kendi onayın:** → **4.E**.

---

## 4.E — README ve roadmap

1. README’ye Faz 4 bölümü: env, `doctor`, `PHASE4_REAL_STACK_VERIFY.md` ve `GRAFANA_HTTP_PHASE4.md` linkleri.
2. `ROADMAP_PHASE3_5.md` ile çelişki kontrolü.

**Test:** `ruff` + `pytest`.

**Kendi onayın:** → **4.F**.

---

## 4.F — Gerçek stack doğrulaması (senin observability yığının)

1. **Repoya token yazma.** Yerelde export veya `.env` (gitignore’da) ile `SENTINEL_GRAFANA_BASE_URL` ve token ayarla.
2. Aynı makineden `doctor` (veya eklenen bağlantı komutu) ile **canlı** test çalıştır.
3. `PHASE4_REAL_STACK_VERIFY.md` tablosunu doldur: tarih, başarı/başarısızlık özeti (HTTP kodu), **URL/token yok**.
4. Stack şu an erişilemiyorsa: dosyaya açık atlama gerekçesi; kod ve mock yine de tamamlanmış sayılır.

**Kendi onayın:** → **G6 kapanış**.

---

## G6 — Kapanış

- `IMPLEMENTATION_PLAN_PHASE4.md` sonuna: `**Faz 4 tamamlandı:** YYYY-MM-DD`
- Son mesaj: kısa özet + “Sonraki: roadmap / Faz 5 planı (varsa).”

---

## Notlar

- Grafana LLM özellikleri sürüme göre değişir; **resmi doc** ile seçtiğin uçları `GRAFANA_HTTP_PHASE4.md` içinde sabitle.
- Blokaj (TLS, self-signed): dokümante et; kullanıcı `SSL_CERT_FILE` veya `verify=False` gibi kararları **bilinçli** verir (varsayılan güvenli kalsın).

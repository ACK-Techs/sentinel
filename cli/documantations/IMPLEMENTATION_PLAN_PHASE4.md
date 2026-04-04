# Agentic CLI (Faz 4) — Uygulama Planı (tam)

Bu plan `ROADMAP_PHASE3_5.md` ile uyumludur: **kendi observability ortamında** Grafana; **Grafana LLM / kolay bağlantı** hedefi ile hizalanır. **Çok kullanıcılı giriş yok.**

**Önkoşul:** Faz 3 tamamlandı (kurulum/doctor stabil).

**Kök:** `sentinel-coming/cli/`. COS/Grafana teşhisi Faz 1 skill’leriyle köprülenir.

**Yürütme:** `CODEX_EXECUTION_PROMPT_PHASE4.md` — tek mesajda otomasyon; **insan onayı beklemez** (Faz 3 ile aynı akış).

---

## Test stratejisi: mock + gerçek yığın (ikisi de planın parçası)

| Katman | Amaç | Zorunluluk |
|--------|------|------------|
| **Mock HTTP** | CI’da ağ ve Grafana olmadan bağlantı mantığı (status kodları, timeout, header) | **Evet** — her PR’da çalışır |
| **Gerçek observability yığını** | Stack ayağa kalktıktan sonra **gerçek URL + token** ile HTTP doğrulama; “bağlantı kuruldu mu?” sorusunun **lab/lokal** cevabı | **Stack erişilebilir olduğunda evet** — Faz 4 kapanışı için bu adım **atlanmamalı**; stack şu an kapalıysa `PHASE4_REAL_STACK_VERIFY.md` içinde **“stack kapalı, tekrarlanacak”** diye not düşülür |

Observability stack’ini **çalışır duruma getirdiysen** (Grafana erişilebilir), konfigürasyonu bağladıktan sonra **mutlaka** canlı bağlantı testini çalıştır ve sonucu dokümante et (başarılı HTTP veya anlamlı hata kodu + kısa not). Bu, yalnızca mock’a güvenmekten ayrılır.

---

## Kapı (gate) — otomatik geçiş

Kullanıcıdan onay istenmez. Kriterler + `ruff` + `pytest` sağlandıysa sonraki bölüme geç.

| Kapı | İçerik |
|------|--------|
| **G0** | Faz 3 tamam; `ruff` + `pytest` yeşil |
| **G1** | 4.A dokümantasyon (Grafana HTTP API / LLM doküman linki, env sözleşmesi) |
| **G2** | 4.B config + `doctor` yüzeyi |
| **G3** | 4.C teşhis köprüsü + uyarı metinleri |
| **G4** | 4.D mock testler |
| **G5** | 4.E README / roadmap uyumu |
| **G6** | **Gerçek stack doğrulaması** (aşağı) veya bilinçli atlama notu |

---

## Faz 4.A — Hedef ve dokümantasyon

**Skill:** `agentic-troubleshoot-grafana` (köprü), resmi Grafana dokümantasyonu

| ID | Adım | Başarı kriteri |
|----|------|----------------|
| A.1 | Hedef Grafana sürümü için **HTTP API** tabanı: `base_url`, `Authorization: Bearer <token>` veya proje kararına göre basic auth — **resmi dokümana link** (`documantations/GRAFANA_HTTP_PHASE4.md` veya mevcut belgeye bölüm). | Hayali uç yok; en az bir health/login benzeri uç seçildi ve gerekçelendirildi. |
| A.2 | Sentinel rolü: **bağlantıyı doğrula**, panel kurma değil; teşhis önerisi Faz 1 skill’e yönlendir. | Kısa “hikaye” paragrafı yazılı. |

---

## Faz 4.B — Entegrasyon yüzeyi (kod)

| ID | Adım | Başarı kriteri |
|----|------|----------------|
| B.1 | Opsiyonel `grafana` (veya `observability.grafana`) config + env (`SENTINEL_GRAFANA_*` — `GF_*` ile çakışma yok) — `sentinel.example.yaml`, Pydantic modeller. | Secret repoda yok; `doctor` özetler. |
| B.2 | `doctor` alt komutu veya bayrak ile **bağlantı testi**: GET (veya proje kararı), timeout, 401/403/200 için anlamlı mesaj. | Mock + gerçek aynı kod yolunu kullanır. |
| B.3 | Faz 1 `agentic-troubleshoot-grafana` (ve gerekirse catalogue) **metin referansı** CLI çıktısında. | Kopyalanabilir skill yolu. |

---

## Faz 4.C — Gözlemlenebilirlik hizalaması

| ID | Adım | Başarı kriteri |
|----|------|----------------|
| C.1 | “Veri yok” / datasource sırası kısa not (Faz 2.D ile uyumlu). | |
| C.2 | LLM/Grafana önerilerinde **doğrula** uyarısı (hallüsinasyon). | |

---

## Faz 4.D — Test (mock, CI)

| ID | Adım | Başarı kriteri |
|----|------|----------------|
| D.1 | `httpx` mock veya `respx` benzeri ile 200/401/timeout senaryoları. | CI’da ağ yok. |
| D.2 | `tests/` altında yeni modül; `ruff` temiz. | |

---

## Faz 4.E — Dokümantasyon

| ID | Adım | Başarı kriteri |
|----|------|----------------|
| E.1 | README’de Faz 4: env, `doctor`, gerçek stack doğrulama checklist’ine link. | |
| E.2 | `ROADMAP_PHASE3_5.md` ile çelişki yok. | |

---

## Faz 4.F — Gerçek observability yığını ile doğrulama (lab / lokal)

**Amaç:** Mock yeterli değil; **çalışan Grafana** (senin stack’in) üzerinde bağlantının gerçekten kurulduğunu görmek.

| ID | Adım | Başarı kriteri |
|----|------|----------------|
| F.1 | Ortamda **yalnızca env veya yerel config** ile `SENTINEL_GRAFANA_BASE_URL` (+ token env) ayarla; değerleri **repoya yazma**. | |
| F.2 | `doctor …` (veya eklenen komut) ile **canlı** test çalıştır. | 200 veya bilinçli 401 (yanlış token) — ikisi de “bağlantı cevap veriyor” kanıtıdır. |
| F.3 | `documantations/PHASE4_REAL_STACK_VERIFY.md` şablonunu doldur: tarih, Grafana major sürüm (ör. UI veya `/api/health` yanıtından), **token/URL yok**, sadece “başarılı / hata kodu / atlama nedeni”. | Stack yoksa: “Observability stack şu an kapalı; F.2 tekrarlanacak” cümlesi. |

**G6:** F.3 dosyası oluşturuldu veya atlama gerekçesi yazıldı; `IMPLEMENTATION_PLAN_PHASE4.md` sonuna kapanış tarihi.

---

## Bilinçli dışarıda bırakılanlar

- SSO / çok kiracı — yok.
- Ürün telemetrisi — yok.
- Tüm dashboard’ların E2E otomasyonu — yok.

---

## Dış kaynak

- `ROADMAP_PHASE3_5.md`
- `IMPLEMENTATION_PLAN_PHASE3.md`
- `skills/agentic-troubleshoot-grafana/SKILL.md`
- `CODEX_EXECUTION_PROMPT_PHASE4.md`

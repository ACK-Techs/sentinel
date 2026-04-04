# Agentic CLI (Faz 3) — Uygulama Planı (tam)

Bu plan `ROADMAP_PHASE3_5.md` ile uyumludur: **iç kullanım**, **telemetri kodu yok**, **dış müşteri teslimi bu fazın çıktısı değildir**.

**Kök:** `sentinel-coming/cli/`

**İlgili skill’ler:** `PHASE3_SKILL_AND_DOC_INDEX.md` — yeni ve mevcut skill tablosu.

**Yürütme:** Tek oturumda otomasyona vermek için `CODEX_EXECUTION_PROMPT_PHASE3.md` kullanılır; bu dosya **kapı (kontrol noktası)** ve alt adımları tanımlar.

---

## Kapı (gate) — otomatik geçiş

Ajan veya geliştirici **kullanıcıdan onay istemez**. Her kapıda başarı kriterleri ve `ruff` + `pytest` sağlandıysa **kendi kendine onay ver** ve sonraki bölüme geç; özet log yeterli.

| Kapı | Ne zaman geçilir | Doğrulama |
|------|------------------|-----------|
| **G0** | Başlangıç testleri yeşil | `ruff` + `pytest` |
| **G1** | 3.A bitti | Wheel/sdist + smoke başarılı; `CHANGELOG` güncel |
| **G2** | 3.B bitti | Secret/çıktı gözden geçirildi; kritik bulgu yok |
| **G3** | 3.C bitti | README tek giriş akışı okunabilir |
| **G4** | 3.D bitti | Telemetri yok politikası yazılı / `ENV_FLAGS` senkron |
| **G5** | 3.E bitti | `ruff` + `pytest` yeşil; isteğe bağlı CI job |

**Kural:** Bölüm sonunda **durup insan onayı bekleme**; kriterler tutuyorsa devam et.

---

## Faz 3.A — Paketleme ve tekrarlanabilir kurulum

**Skill:** `agentic-packaging-pypi`, `agentic-wheel-build-verify`

| ID | Adım | Başarı kriteri | Not |
|----|------|----------------|-----|
| A.1 | `pyproject.toml` içine `build` paketini **`[project.optional-dependencies]` → `dev`** altına ekle (veya dokümanda `pip install build`); sürüm aralığı makul pin. | `pip install -e ".[dev]"` sonrası `python -m build` çalışır. | Hatchling zaten var. |
| A.2 | `python -m build` ile `dist/` altında `.whl` ve `.tar.gz` üret; gerekirse önce `dist/` temizle. | İki artefakt oluşur. | `.gitignore`’da `dist/` var mı kontrol et; yoksa ekle. |
| A.3 | **Smoke:** Yeni venv (örn. `.venv-smoke`), sadece wheel’den `pip install path/to.whl`, sonra `sentinel-cli --help` ve `sentinel-cli version`. | Exit code 0. | Skill: `agentic-wheel-build-verify`. |
| A.4 | README’ye **“Paket (wheel) ile kurulum”** alt bölümü: geliştirme (`-e`) vs üretilen wheel farkı. | Kopyala-yapıştır blokları çalışır. | Platform notu (Linux öncelik). |
| A.5 | `CHANGELOG.md`: `[Unreleased]` altında yapılan maddeler; Faz 3 tamamlanınca sürüm tarihi/sürüm numarası kararı (en azından Unreleased → tarih notu). | Dosya `pyproject` ile tutarlı dilde. | Keep a Changelog tarzı. |

**G1 — Otomatik geçiş:** A.3 smoke + `dist/` liste loglandı; testler yeşil → 3.B.

---

## Faz 3.B — Sertleştirme (güvenlik ve dayanıklılık)

**Skill:** `agentic-secrets-handling`, `agentic-cli-user-errors`, `agentic-approval-policy-design`

| ID | Adım | Başarı kriteri | Not |
|----|------|----------------|-----|
| B.1 | `.env.example` ve `config/sentinel.example.yaml` placeholder’ları gözden geçir; gerçek anahtar formatına benzeyen örnek yok. | Grep ile `sk-`, uzun base64 benzeri gerçekçi secret yok. | |
| B.2 | `doctor` ve `config` çıktılarında **ham API key** yazılmıyor (maske veya “set” kısa bilgi). | Kod yolu kontrolü. | Gerekirse küçük kod düzeltmesi. |
| B.3 | Yaygın hata yolları (LLM timeout, bağlantı reddi, MCP yok): kullanıcıya **kısa** mesaj; `--verbose` / log ile ayrıntı. | En az 2 senaryo dokümante veya kodda gözden geçirildi. | `agentic-cli-user-errors` ile uyum. |
| B.4 | Onay/shell/yazma politikası: `ARCHITECTURE_AGENTIC_CLI.md` ve README **çelişmiyor**; tek cümle düzeltme. | Okuyan tutarsızlık görmüyor. | |
| B.5 | `pyproject` üst sınır stratejisi: README veya `CONTRIBUTING` içinde bir paragraf (“major yükseltme ayrı karar”). | | |

**G2 — Otomatik geçiş:** B.1–B.2 kontrol listesi loglandı → 3.C.

---

## Faz 3.C — Dokümantasyon (tek giriş)

**Skill:** `agentic-docs-user-quickstart` (hizalama), `agentic-docs-developer-checklist`

| ID | Adım | Başarı kriteri | Not |
|----|------|----------------|-----|
| C.1 | README üstte: ne bu CLI, Faz 1/2 ilişkisi, **kurulum**, `doctor`, `run`/`repl`, link: `LLM_PROVIDERS.md`, `ARCHITECTURE_AGENTIC_CLI.md`, `CONTRIBUTING.md`, `CHANGELOG.md`. | Tek dosyadan yön bulunur. | |
| C.2 | README’de **Faz 3 güncel** / arşiv cümlesi; `documantations/archive/README.md` rolü. | Yinelenen uzun metin yok. | |
| C.3 | `CONTRIBUTING.md` — zaten oluşturulduysa senkron: komutlar `pyproject` ile uyumlu. | | |
| C.4 | `archive/README.md` güncel listeye `PHASE3_SKILL_AND_DOC_INDEX.md` veya Faz 3 notu ekle (isteğe bağlı tek satır). | | |

**G3 — Otomatik geçiş:** README özeti loglandı → 3.D.

---

## Faz 3.D — Feature flag’ler ve telemetri (politika)

**Skill:** `agentic-feature-flags`, `agentic-faz3-no-remote-telemetry`

| ID | Adım | Başarı kriteri | Not |
|----|------|----------------|-----|
| D.1 | Kod ve env’de geçen `SENTINEL_*` (ve deneysel) bayrakları **tablo**: ad, varsayılan, anlam, risk notu. Doğruluk kaynağı: `documantations/ENV_FLAGS_PHASE3.md` (kod değişince senkron). | `doctor` ile çelişen ifade yok. | Kullanılmayan env → kaldır veya “rezerv”. |
| D.2 | README veya kısa politika dosyası: **uzaktan ürün telemetrisi yok**; yerel log ayrımı. | `agentic-faz3-no-remote-telemetry` ile uyum. | Yeni analytics kodu **eklenmez**. |

**G4 — Otomatik geçiş:** Telemetri + bayrak tablosu doğrulandı → 3.E.

---

## Faz 3.E — Test ve CI

**Skill:** `agentic-testing-unit`, `agentic-testing-integration-mock-llm`, `agentic-ci-github-actions`

| ID | Adım | Başarı kriteri | Not |
|----|------|----------------|-----|
| E.1 | `python -m ruff check .` ve `python -m pytest -q` yeşil. | | |
| E.2 | Yeni davranış eklendiyse (çıktı maskeleme vb.) ilgili test veya smoke notu. | | |
| E.3 | **İsteğe bağlı:** `.github/workflows/` altında `cli` için lint+test job yoksa iskelet ekle; varsa Faz 3 komutlarıyla hizala. Fork güvenliği: secret yok. | | Ağır değilse yap. |
| E.4 | **İsteğe bağlı:** `scripts/smoke_wheel.sh` veya Makefile hedefi — wheel build + venv smoke (E.3’e bağlı). | | Manuel checklist da yeter. |

**G5 — Kapanış:** Test özeti + `IMPLEMENTATION_PLAN_PHASE3.md` sonuna tarih; isteğe bağlı `ROADMAP_PHASE3_5.md` tek cümle.

---

## Hızlı geri sarma

| Sorun | Önce |
|-------|------|
| Wheel import hatası | `hatch` packages, `src/` layout |
| Ruff fail | `pip install -e ".[dev]"` |
| Doctor sızdırıyor | Log/config kod yolu |

---

## Faz 3 kapanış checklist

- [ ] G1–G5 geçildi (veya isteğe bağlı maddeler bilinçle atlandı ve dokümante edildi)
- [ ] `CHANGELOG.md` güncel
- [ ] `PHASE3_SKILL_AND_DOC_INDEX.md` ile dosya listesi eşleşiyor
- [ ] `CODEX_EXECUTION_PROMPT_PHASE3.md` içindeki sıra ile uyum doğrulandı

## Dış kaynak

- `ROADMAP_PHASE3_5.md`
- `IMPLEMENTATION_PLAN_PHASE4.md` (sonraki faz)

**Faz 3 tamamlandı:** 2026-04-05

# Agentic CLI (Faz 2) — Uygulama Planı

Bu plan, **bu klasördeki** `SKILL_CATALOG_PHASE2.md` içindeki `cli/skills/agentic-*` skill’leri ile uyumludur. Üst kısımdaki **Yapay Zeka Otonomi ve Hata Yönetim Protokolü** `PROJECT_ROOT_PHASE2.md` ile aynıdır ve bağlayıcıdır.

**Kök:** Tüm yollar `sentinel-coming/` altındadır; Faz 2 belgeleri `cli/documantations/`, Faz 2 agentic skill’leri `cli/skills/`.

---

## Faz 2.A — Çerçeve, güvenlik, depo

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| A.1 | Faz 2 kapsamı ve repo yerleşimini sabitle. | `agentic-project-charter`, `agentic-repo-layout` | Kökte CLI paketi yolu ve `sentinel-coming` ile ilişki yazılı; README’de Faz 1/2 ayrımı net. | Kapsam genişlediyse charter güncelle; mimari belgeyi senkronize et. |
| A.2 | Bağımlılık ve lisans envanteri. | `agentic-dependency-licensing` | Üçüncü parti listesi + lisans sütunu; yasaklı lisans yok veya istisna onaylı. | Çakışma → alternatif kütüphane veya hukuk incelemesi. |
| A.3 | Tehdit modeli ve sırlar. | `agentic-threat-model`, `agentic-secrets-handling` | Tehdit listesi + mitigasyon; API key’ler repoda yok; örnek `.env.example` placeholder. | Sızıntı riski → secret scan + `.gitignore`. |
| A.4 | Onay politikası tasarımı. | `agentic-approval-policy-design` | Risk sınıfları (read/write/shell) ve varsayılan onay matrisi dokümante. | Çok gevşek → üretim profilinde sıkılaştır. |
| A.5 | Prompt enjeksiyonu ve araç güvenliği. | `agentic-prompt-injection-guardrails` | Skill ve sistem talimatlarında “güvenilmeyen içerik” kuralları yazılı. | İhlal senaryosu → hook veya sandbox ek önlem. |

---

## Faz 2.B — Konfigürasyon ve LLM çoklu motor

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| B.1 | Katmanlı config birleştirme. | `agentic-config-layers`, `agentic-config-env-reference` | Varsayılan < dosya < env < CLI bayrakları sırası testle doğrulandı. | Öncelik çakışması → belgede tek doğru sıra. |
| B.2 | Profiller: cloud / local. | `agentic-config-profiles` | `SENTINEL_PROFILE=local` ve `cloud` ile farklı `base_url`/model seçimi çalışır. | Profil bilinmiyor → anlamlı hata mesajı. |
| B.3 | Sağlayıcı sözleşmesi (arayüz). | `agentic-llm-provider-contract` | Tek tip stream olayları veya ortak result tipi kodda tanımlı. | API farkı → adapter alt sınıfı. |
| B.4 | Uzak OpenAI uyumlu API. | `agentic-llm-openai-compatible-remote` | En az bir uzak uç ile chat+stream doğrulandı. | TLS/proxy → `LLM_PROVIDERS.md` ve env. |
| B.5 | Lokal OpenAI uyumlu uç. | `agentic-llm-openai-compatible-local` | `localhost` base_url + model ile yanıt alınır. | Bağlantı yok → kullanıcıya servis kontrol listesi. |
| B.6 | Anthropic adapter (isteğe bağlı ama önerilir). | `agentic-llm-anthropic-messages` | Mesaj map ve tool map testi (mock veya sandbox key). | Şema farkı → sadece dokümante edilmiş alt yol. |
| B.7 | Streaming ve bağlam. | `agentic-llm-streaming-events`, `agentic-llm-context-window-strategy`, `agentic-llm-retries-timeouts` | Uzun çıktıda parça birleşimi; context dolunca politika (kes/kısalt/uyar); timeout + sınırlı retry. | Sonsuz retry yok; log’da secret yok. |

---

## Faz 2.C — CLI kabuğu, ajan döngüsü, araçlar

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| C.1 | Giriş noktası ve komutlar. | `agentic-cli-entrypoint`, `agentic-cli-repl-vs-once` | `--help`; tek komut modu ve REPL (veya planlanan mod) ayrımı çalışır. | UX karışıklığı → dokümantasyon + örnek. |
| C.2 | Yapılandırılmış log ve kullanıcı hataları. | `agentic-cli-logging`, `agentic-cli-user-errors` | Log seviyesi flag; kullanıcıya kısa exit code + mesaj. | Stack trace sızıntısı → sadece debug. |
| C.3 | Ajan tur döngüsü. | `agentic-agent-turn-loop` | `max_turns`, durdurma, iptal (varsa) tanımlı. | Sonsuz döngü → sert üst sınır. |
| C.4 | Tool şeması ve çağrı ayrıştırma. | `agentic-tools-base-contract`, `agentic-agent-tool-call-parse` | Geçersiz tool adı/args yakalanır; modele hata sonucu döner. | Model uydurma tool → kullanıcıya özet. |
| C.5 | Bash ve dosya araçları. | `agentic-tools-bash-shell`, `agentic-tools-filesystem-read`, `agentic-tools-filesystem-write` | Onay + timeout + çıktı boyutu sınırı (skill’e uygun). | İzin reddi → policy güncelle veya kullanıcı onayı. |
| C.6 | Hook’lar. | `agentic-hooks-pre-post-tool` | Pre/Post hook olayları dokümante; başarısız hook davranışı net. | Hook güvenliği → sadece yapılandırılmış komutlar. |
| C.7 | MCP istemcisi. | `agentic-mcp-client-config`, `agentic-mcp-tool-mapping` | Örnek MCP sunucusu ile en az bir araç listelenir (ortam uygunsa). | SDK yok → isteğe bağlı ekstra bağımlılık kararı. |
| C.8 | Oturum ve trajectory. | `agentic-session-persistence`, `agentic-trajectory-recording` | Oturum dosyası veya DB yolu yapılandırılabilir; PII redaksiyonu kuralları yazılı. | Disk dolması → rotasyon politikası. |
| C.9 | Geçmiş sıkıştırma (isteğe bağlı ilk sürüm). | `agentic-agent-history-compaction` | Eşik aşımında özet veya kesme davranışı tutarlı. | Özet kalitesi düşük → kullanıcı uyarısı. |
| C.10 | Çoklu sağlayıcı geçişi. | `agentic-agent-multi-provider-switch` | Aynı oturumda değilse bile CLI ile profil değişimi dokümante. | Tutarsız history → yeni oturum önerisi. |

---

## Faz 2.D — COS / gözlemlenebilirlik danışmanlığı (skill içerikleri)

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| D.1 | COS genel danışman playbook. | `agentic-cos-advisor-overview` | Faz 1 `PROJECT_ROOT.md` ve charm listesi ile hizalı özet. | Belirsizlik → Faz 1 skill’e yönlendir. |
| D.2 | MicroK8s ve Juju komut referansı. | `agentic-microk8s-ops-reference`, `agentic-juju-ops-reference` | Teşhis sırası ve komutlar; `sudo`/grup uyarıları. | Yetki hatası → oturum/grup skill’leri. |
| D.3 | Bileşen teşhisleri. | `agentic-troubleshoot-grafana`, `agentic-troubleshoot-prometheus`, `agentic-troubleshoot-loki`, `agentic-troubleshoot-alertmanager`, `agentic-troubleshoot-traefik-ingress`, `agentic-cos-catalogue-endpoints`, `agentic-cos-no-data-playbook` | Her biri checklist + tipik hata + geri dönüş içerir. | Veri yok → ilişki ve datasource skill zinciri. |

---

## Faz 2.E — Paketleme, test, dokümantasyon, skill yazım standardı

| # | Adım | İlgili skill(ler) | Başarı kriteri (checklist) | Hata / geri dönüş |
|---|------|-------------------|---------------------------|-------------------|
| E.1 | Paketleme. | `agentic-packaging-pypi` veya seçilen dağıtım | `pip install` / `uv run` veya binary pipeline dokümante. | Platform farkı → matris. |
| E.2 | Testler. | `agentic-testing-unit`, `agentic-testing-integration-mock-llm` | Mock LLM ile en az bir entegrasyon akışı yeşil. | Flaky → zaman sınırı ve izolasyon. |
| E.3 | CI. | `agentic-ci-github-actions` | PR’da lint+test (ve varsa tip kontrolü). | Gizli değişken → sadece fork güvenliği. |
| E.4 | Kullanıcı hızlı başlangıç. | `agentic-docs-user-quickstart` | API ve lokal mod için kopyala-çalıştır blokları. | Eksik adım → SKILL güncelle. |
| E.5 | Skill yazım standardı. | `agentic-skill-authoring-standard` | Yeni `agentic-*` skill’ler aynı frontmatter ve bölüm başlıklarını kullanır. | Tutarsızlık → katalog revizyonu. |
| E.6 | Feature flags (isteğe bağlı). | `agentic-feature-flags` | Deneysel araçlar bayrak arkasında. | Bayrak unutuldu → varsayılan güvenli kapalı. |
| E.7 | Telemetri (isteğe bağlı). | `agentic-telemetry-optional` | Opt-in; PII yok; devre dışı varsayılan veya açık politika kararı yazılı. | Regülasyon → veri minimizasyonu. |

---

## Hızlı geri sarma özeti

| Sorun | Önce kontrol et | Skill yönü |
|-------|-----------------|------------|
| Model yanıt yok / timeout | Profil, `base_url`, firewall | B.4–B.7 |
| Tool çalışmıyor | Onay, hook, policy | C.4–C.6 |
| Lokal model tool üretmiyor | Model yetenekleri | B.5 + `LLM_PROVIDERS.md` |
| Grafana boş | Datasource, ilişkiler | D.3, Faz 1 `cos-relation-*` |
| Ingress açılmıyor | MetalLB, Traefik | D.3, Faz 1 `cos-ingress-config` |

---

## Dış kaynak

- `cli/documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `cli/documantations/REPO_LAYOUT_RECOMMENDED.md` — önerilen `cli/` dizin ağacı
- `cli/documantations/LLM_PROVIDERS.md`
- `cli/documantations/SKILL_CATALOG_PHASE2.md`
- Workspace `agentic/`: **Pywen-dev**, **codex-main**, **claude** — Faz 2 için yardımcı tasarım/kaynak referansı (Sentinel paketine vendor edilmez; `PROJECT_ROOT_PHASE2.md` «Referans kod tabanları»)

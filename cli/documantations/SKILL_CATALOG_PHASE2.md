# Faz 2 Skill Kataloğu ve Yazım Şartnamesi

Bu dosya **tek doğruluk kaynağıdır**: her Faz 2 `agentic-*` skill dosyasının **adı, kapsamı, zorunlu bölümleri ve doldurulması gereken içerik maddeleri** burada tanımlanır. Kodlayıcı AI yalnızca bu şartnameye uygun **gövde metnini** üretir.

**Konum:** Tüm Faz 2 agentic skill’leri `sentinel-coming/cli/skills/` altındadır (Faz 1 COS skill’leri `sentinel-coming/skills/` altında kalır).

## Global kurallar (tüm `agentic-*` skill’leri)

**Dosya yolu (depo köküne göre):** `sentinel-coming/cli/skills/<skill-id>/SKILL.md`

**Frontmatter (YAML, zorunlu):**

```yaml
---
name: <skill-id>
description: <Türkçe, tek cümle; ne zaman kullanılır>
---
```

**İsteğe bağlı frontmatter** (CLI implementasyonu skill meta okuyacaksa eklenebilir; yoksa gövdede yazılır):

```yaml
allowed-tools: []   # örnek: bash, read_file — yalnızca ürün kararı varsa
paths: []           # örnek: göreli repo kökleri
```

**Gövde bölümleri (sıra ile, Türkçe başlıklar):**

1. `## Amaç` — Bu skill neyi standartlaştırır?
2. `## Kapsam` — Dahil / hariç (madde işaretli).
3. `## Kurallar` veya `## Adımlar` — Uygulanabilir kurallar veya numaralı prosedür (en az biri zorunlu).
4. `## Kontrol listesi` — Operatör veya AI için doğrulama maddeleri.
5. `## Hata ve geri dönüş` — Tipik hata → ne kontrol et → sonraki adım.
6. `## İlgili belgeler ve skill'ler` — çapraz bağlantılarda **göreli yol** kullan (skill dosyası `cli/skills/<id>/SKILL.md` konumundayken):
   - Faz 2 belgeleri (`cli/documantations/`): `../documantations/<dosya>.md`
   - Diğer Faz 2 agentic skill: `../<diğer-skill-id>/SKILL.md`
   - Faz 1 belgeleri (`sentinel-coming/documantations/`): `../../documantations/<dosya>.md`
   - Faz 1 COS/MicroK8s/Juju skill’leri (`sentinel-coming/skills/`): `../../skills/<faz1-skill-id>/SKILL.md`

**Stil:** Faz 1 skill’leri (`../../skills/juju-model-cos/SKILL.md` gibi) ile uyumlu ton; komutlar ve API adları **İngilizce** kalabilir; açıklamalar **Türkçe**.

**Okuma sırası grupları:** Aşağıdaki **Dal** sırası önerilir; her skill kendi içinde “Önce şunu oku” ile güçlendirilmelidir.

---

## Dal A — Proje, depo, güvenlik temeli

### `agentic-project-charter`

| Alan | Değer |
|------|--------|
| **Amaç** | Faz 2’nin misyonu, kapsam dışı maddeler, başarı tanımı. |
| **İçerik maddeleri** | COS danışmanlığı vs kod yazma sınırı; API+lokal LLM hedefi; `agentic/` referans depo rolü; kullanıcı persona (SRE, geliştirici). |
| **Önce oku** | `PROJECT_ROOT_PHASE2.md` |
| **Çapraz** | `agentic-repo-layout`, `agentic-cos-advisor-overview` |

### `agentic-repo-layout`

| Alan | Değer |
|------|--------|
| **Amaç** | Önerilen dizin ağacı: CLI paketi, test, config örnekleri, `sentinel-coming` ile ilişki. |
| **İçerik maddeleri** | Uygulama kökü **`sentinel-coming/cli/`** altında; kaynak (`src/` vb.), test, `.env.example`, `pyproject.toml`; üst `documantations/` + `skills/` = Faz 1 (COS); `cli/documantations/` + `cli/skills/agentic-*` = Faz 2. |
| **Önce oku** | `ARCHITECTURE_AGENTIC_CLI.md` |
| **Çapraz** | `agentic-packaging-pypi`, `agentic-config-layers` |

### `agentic-dependency-licensing`

| Alan | Değer |
|------|--------|
| **Amaç** | Bağımlılık envanteri şablonu; lisans türleri; `agentic/` kaynak kodundan türetme notları (telif farkındalığı). |
| **İçerik maddeleri** | MIT/Apache/GPL uyumluluk tablosu; SBOM veya `pip-licenses` benzeri öneri; yasaklı lisans prosedürü. |
| **Çapraz** | `agentic-project-charter` |

### `agentic-threat-model`

| Alan | Değer |
|------|--------|
| **Amaç** | STRIDE veya basit tehdit listesi: shell execution, dosya sızıntısı, API key çalınması, MCP kötü sunucu. |
| **İçerik maddeleri** | Her tehdit için mitigasyon (onay, sandbox hedefi, network policy); “kabul edilen risk” alanı. |
| **Çapraz** | `agentic-approval-policy-design`, `agentic-tools-bash-shell` |

### `agentic-secrets-handling`

| Alan | Değer |
|------|--------|
| **Amaç** | API key, kubeconfig, Juju credential saklama; loglarda maskeleme. |
| **İçerik maddeleri** | Env > secret manager > dosya izinleri sırası; `.env` git’e girmemeli; örnek placeholder isimleri (`LLM_PROVIDERS.md` ile uyumlu). |
| **Çapraz** | `agentic-cli-logging`, `agentic-config-env-reference` |

### `agentic-approval-policy-design`

| Alan | Değer |
|------|--------|
| **Amaç** | Araç risk sınıfları ve varsayılan onay matrisi (interactive vs CI). |
| **İçerik maddeleri** | read-only vs mutating; `sudo` içeren komutlar; çok adımlı onay; “yolo” modunun risk uyarısı. |
| **Çapraz** | `agentic-tools-base-contract`, `agentic-hooks-pre-post-tool` |

### `agentic-prompt-injection-guardrails`

| Alan | Değer |
|------|--------|
| **Amaç** | Güvenilmeyen içerik (issue gövdesi, web sayfası) ile sistem talimatı ayrımı. |
| **İçerik maddeleri** | Talimat önceliği; tool argümanı doğrulama; kullanıcıya “şüpheli istek” raporu. |
| **Çapraz** | `agentic-agent-turn-loop` |

---

## Dal B — Konfigürasyon ve ortam

### `agentic-config-layers`

| Alan | Değer |
|------|--------|
| **Amaç** | Birleştirme sırası ve çakışma çözümü. |
| **İçerik maddeleri** | defaults < `config.yaml` < env < CLI flags; örnek YAML blokları; liste türü alanların merge stratejisi (replace vs append). |
| **Çapraz** | `agentic-config-profiles`, `agentic-config-env-reference` |

### `agentic-config-env-reference`

| Alan | Değer |
|------|--------|
| **Amaç** | Tüm env değişkenlerinin tek tablosu: anlam, örnek, zorunluluk. |
| **İçerik maddeleri** | `LLM_PROVIDERS.md` ile birebir uyumlu tablo; profil değişkenleri; log seviyesi; config dosya yolu. |
| **Çapraz** | `LLM_PROVIDERS.md` |

### `agentic-config-profiles`

| Alan | Değer |
|------|--------|
| **Amaç** | `cloud`, `local`, `anthropic-only` gibi profillerin alan haritası. |
| **İçerik maddeleri** | Profil seçimi önceliği; örnek `.yaml` parçaları; geçişte oturum sıfırlama uyarısı. |
| **Çapraz** | `agentic-llm-openai-compatible-remote`, `agentic-llm-openai-compatible-local` |

### `agentic-feature-flags`

| Alan | Değer |
|------|--------|
| **Amaç** | Deneysel araçlar ve MCP için bayraklar; varsayılan kapalı güvenli mod. |
| **İçerik maddeleri** | `SENTINEL_EXPERIMENTAL_*` örnekleri; bayrak dokümantasyonu nerede listelenir. |
| **Çapraz** | `agentic-mcp-client-config` |

---

## Dal C — LLM sağlayıcıları

### `agentic-llm-provider-contract`

| Alan | Değer |
|------|--------|
| **Amaç** | Uygulama içi arayüz: `complete`, `stream`, hata tipleri, iptal. |
| **İçerik maddeleri** | Ortak mesaj rolü şeması; tool call iç temsili; sağlayıcıların uyması gereken minimum metotlar. |
| **Çapraz** | Tüm `agentic-llm-*` |

### `agentic-llm-openai-compatible-remote`

| Alan | Değer |
|------|--------|
| **Amaç** | Uzak OpenAI uyumlu API kullanım kuralları. |
| **İçerik maddeleri** | `base_url`, `api_key`, `model`; proxy; organization header (opsiyonel); örnek `curl`. |
| **Çapraz** | `agentic-llm-streaming-events`, `agentic-llm-retries-timeouts` |

### `agentic-llm-openai-compatible-local`

| Alan | Değer |
|------|--------|
| **Amaç** | Ollama/LM Studio/vLLM OpenAI uyumlu uç. |
| **İçerik maddeleri** | Tipik portlar; model listesi komutu; tool desteği olmayan modellerde fallback stratejisi; IPv4/IPv6 loopback. |
| **Çapraz** | `agentic-llm-context-window-strategy` |

### `agentic-llm-anthropic-messages`

| Alan | Değer |
|------|--------|
| **Amaç** | Anthropic Messages API → iç şema map; tool kullanımı. |
| **İçerik maddeleri** | `system` vs `messages`; `tool_use` / `tool_result` eşlemesi; beta header notları (varsa, “dokümanda kontrol et”). |
| **Çapraz** | `agentic-llm-provider-contract` |

### `agentic-llm-streaming-events`

| Alan | Değer |
|------|--------|
| **Amaç** | Birleşik olay türleri: metin parçası, tool çağrısı parçası, bitiş, hata. |
| **İçerik maddeleri** | Birleştirme sırası; kısmi JSON biriktirme uyarısı; UTF-8 sınır sorunları. |
| **Çapraz** | `agentic-agent-tool-call-parse` |

### `agentic-llm-context-window-strategy`

| Alan | Değer |
|------|--------|
| **Amaç** | Token/limit yaklaşımı: kesme, özet, uyarı; sistem+tools+history öncelik sırası. |
| **İçerik maddeleri** | Tahmini sayım yöntemi (heuristik vs API); kullanıcıya “bağlam dolu” mesajı. |
| **Çapraz** | `agentic-agent-history-compaction` |

### `agentic-llm-retries-timeouts`

| Alan | Değer |
|------|--------|
| **Amaç** | Retry sınıfı, exponential backoff, idempotency uyarısı. |
| **İçerik maddeleri** | Hangi HTTP kodlarında retry; maksimum deneme; timeout katmanları (connect vs read). |
| **Çapraz** | `agentic-cli-user-errors` |

---

## Dal D — CLI kabuğu ve kullanıcı deneyimi

### `agentic-cli-entrypoint`

| Alan | Değer |
|------|--------|
| **Amaç** | Ana komut ağacı: `chat`, `config`, `doctor`, `version` (örnek isimler). |
| **İçerik maddeleri** | Global flag’ler; yardım metni şablonu; çıkış kodları tablosu. |
| **Çapraz** | `agentic-cli-repl-vs-once` |

### `agentic-cli-repl-vs-once`

| Alan | Değer |
|------|--------|
| **Amaç** | Etkileşimli döngü vs tek satır/pipe modu. |
| **İçerik maddeleri** | stdin TTY kontrolü; slash komutları (varsa); non-interactive CI davranışı. |
| **Çapraz** | `agentic-agent-turn-loop` |

### `agentic-cli-logging`

| Alan | Değer |
|------|--------|
| **Amaç** | Yapılandırılmış log alanları; stderr vs dosya; secret redaction. |
| **İçerik maddeleri** | `session_id`, `provider`, `turn`, `tool_name` örnekleri; debug modunda bile key maskeleme. |
| **Çapraz** | `agentic-secrets-handling`, `agentic-telemetry-optional` |

### `agentic-cli-user-errors`

| Alan | Değer |
|------|--------|
| **Amaç** | Kullanıcıya gösterilecek hata mesajı şablonları (Türkçe). |
| **İçerik maddeleri** | Exit code ↔ anlam; “sonraki komut” önerisi; `--verbose` ile teknik detay. |
| **Çapraz** | `agentic-llm-retries-timeouts` |

---

## Dal E — Ajan çekirdeği

### `agentic-agent-turn-loop`

| Alan | Değer |
|------|--------|
| **Amaç** | Tur yaşam döngüsü, `max_turns`, durdurma koşulları, iptal sinyali (SIGINT). |
| **İçerik maddeleri** | Model “final answer” vs tool döngüsü; sonsuz döngü önleme; kullanıcı ara müdahalesi. |
| **Çapraz** | `agentic-agent-tool-call-parse`, `agentic-prompt-injection-guardrails` |

### `agentic-agent-tool-call-parse`

| Alan | Değer |
|------|--------|
| **Amaç** | Model çıktısından tool çağrılarının doğrulanması ve reddedilmesi. |
| **İçerik maddeleri** | Bilinmeyen araç; şema ihlali; çoklu çağrı sırası; hata mesajını modele geri besleme. |
| **Çapraz** | `agentic-tools-base-contract` |

### `agentic-agent-history-compaction`

| Alan | Değer |
|------|--------|
| **Amaç** | Uzun oturumda özetleme veya kesme politikası. |
| **İçerik maddeleri** | Hangi mesajlar korunur (system, ilk kullanıcı); özet kalitesi düşükse uyarı; maliyet notu. |
| **Çapraz** | `agentic-llm-context-window-strategy` |

### `agentic-agent-multi-provider-switch`

| Alan | Değer |
|------|--------|
| **Amaç** | Oturumlar arası profil değişimi; aynı thread’de karışık provider riski. |
| **İçerik maddeleri** | “Yeni oturum öner” kuralları; config reload. |
| **Çapraz** | `agentic-config-profiles` |

---

## Dal F — Araçlar, hook, MCP, oturum

### `agentic-tools-base-contract`

| Alan | Değer |
|------|--------|
| **Amaç** | Her aracın uyması gereken sözleşme: `name`, `description`, JSON şema, `execute`. |
| **İçerik maddeleri** | Zaman aşımı; maks çıktı boyutu; hata nesnesi formatı. |
| **Çapraz** | Tüm `agentic-tools-*` |

### `agentic-tools-bash-shell`

| Alan | Değer |
|------|--------|
| **Amaç** | Shell yürütme güvenliği: cwd, timeout, çıktı kırpma, `sudo` politikası. |
| **İçerik maddeleri** | İşletim sistemi farkları; arka plan iş yasağı (öneri); allowlist/denylist örnekleri. |
| **Çapraz** | `agentic-approval-policy-design`, `agentic-threat-model` |

### `agentic-tools-filesystem-read`

| Alan | Değer |
|------|--------|
| **Amaç** | Okuma: path normalizasyonu, symlink, repo kökü dışına çıkma. |
| **İçerik maddeleri** | Binary dosyalar; boyut sınırı; encoding. |
| **Çapraz** | `agentic-tools-filesystem-write` |

### `agentic-tools-filesystem-write`

| Alan | Değer |
|------|--------|
| **Amaç** | Yazma/yama: atomik yazma; yedekleme önerisi; .git içine yazma uyarısı. |
| **İçerik maddeleri** | Onay zorunluluğu; diff önizleme önerisi. |
| **Çapraz** | `agentic-approval-policy-design` |

### `agentic-tools-web-fetch-optional`

| Alan | Değer |
|------|--------|
| **Amaç** | İsteğe bağlı HTTP GET; SSRF riski ve domain allowlist. |
| **İçerik maddeleri** | Varsayılan kapalı; boyut sınırı; redirect limiti. |
| **Çapraz** | `agentic-threat-model`, `agentic-feature-flags` |

### `agentic-hooks-pre-post-tool`

| Alan | Değer |
|------|--------|
| **Amaç** | PreToolUse / PostToolUse olayları; subprocess veya plugin noktası. |
| **İçerik maddeleri** | stdin JSON şeması (örnek); nonzero exit = bloklama mı uyarı mı; timeout. |
| **Çapraz** | `agentic-approval-policy-design` |

### `agentic-mcp-client-config`

| Alan | Değer |
|------|--------|
| **Amaç** | MCP sunucu listesi config şekli; stdio vs HTTP; env injection. |
| **İçerik maddeleri** | Örnek `mcp_servers` YAML; güvenilir kaynak uyarısı. |
| **Çapraz** | `agentic-mcp-tool-mapping`, `agentic-feature-flags` |

### `agentic-mcp-tool-mapping`

| Alan | Değer |
|------|--------|
| **Amaç** | MCP tool adlarının iç registry ile çakışma önleme ve isim önekleri. |
| **İçerik maddeleri** | `mcp_<server>_<tool>` gibi kural; çakışma çözümü. |
| **Çapraz** | `agentic-tools-base-contract` |

### `agentic-session-persistence`

| Alan | Değer |
|------|--------|
| **Amaç** | Oturum dosyası yolu, format (jsonl/sqlite), resume davranışı. |
| **İçerik maddeleri** | Bozuk dosya kurtarma; çoklu oturum; gizlilik (disk şifreleme uyarısı). |
| **Çapraz** | `agentic-trajectory-recording` |

### `agentic-trajectory-recording`

| Alan | Değer |
|------|--------|
| **Amaç** | Tur bazlı kayıt: model çıktısı, tool çağrıları, sonuçlar (denetim/replay). |
| **İçerik maddeleri** | PII redaksiyonu; döndürme politikası; opt-in. |
| **Çapraz** | `agentic-cli-logging`, `agentic-telemetry-optional` |

---

## Dal G — COS danışmanlığı ve teşhis (Faz 1 ile köprü)

### `agentic-cos-advisor-overview`

| Alan | Değer |
|------|--------|
| **Amaç** | Danışman ajanının COS Lite bileşen haritası ve okuma sırası. |
| **İçerik maddeleri** | `PROJECT_ROOT.md`, `ARCHITECTURE_COS.md`, `IMPLEMENTATION_PLAN.md` köprüleri; hangi Faz 1 skill ne zaman çağrılır. |
| **Çapraz** | Tüm `agentic-troubleshoot-*`, Faz 1 `cos-*` |

### `agentic-microk8s-ops-reference`

| Alan | Değer |
|------|--------|
| **Amaç** | Teşhis için MicroK8s komut şablonları ve sıra. |
| **İçerik maddeleri** | `microk8s status`, `kubectl get pods -A`, addon kontrolü; grup üyeliği uyarısı. |
| **Çapraz** | Faz 1 `microk8s-*` skill’leri |

### `agentic-juju-ops-reference`

| Alan | Değer |
|------|--------|
| **Amaç** | `juju status`, `debug-log`, model switch, `run` örnekleri. |
| **İçerik maddeleri** | `cos` modelinde çalışma kuralı; ilişki tablosu okuma. |
| **Çapraz** | Faz 1 `juju-*`, `cos-relation-*` |

### `agentic-troubleshoot-grafana`

| Alan | Değer |
|------|--------|
| **Amaç** | Giriş, datasource, boş pano, admin parola akışı. |
| **İçerik maddeleri** | `get-admin-password`; Traefik URL; ilişki eksikliği belirtileri. |
| **Çapraz** | `agentic-cos-no-data-playbook`, Faz 1 `cos-deploy-grafana` |

### `agentic-troubleshoot-prometheus`

| Alan | Değer |
|------|--------|
| **Amaç** | Hedef yok, scrape hatası, PVC, charm blocked. |
| **İçerik maddeleri** | `juju status` mesajları; metrics endpoint ilişkileri. |
| **Çapraz** | Faz 1 `cos-deploy-prometheus`, `cos-relation-prometheus-grafana` |

### `agentic-troubleshoot-loki`

| Alan | Değer |
|------|--------|
| **Amaç** | Log akışı yok, depolama, charm hataları. |
| **İçerik maddeleri** | Loki ↔ Grafana ilişkisi; örnek sorgu yolu (LogQL’e dokunma seviyesi). |
| **Çapraz** | Faz 1 `cos-deploy-loki`, `cos-relation-loki-grafana` |

### `agentic-troubleshoot-alertmanager`

| Alan | Değer |
|------|--------|
| **Amaç** | Ready endpoint, routing, sessiz uyarılar. |
| **İçerik maddeleri** | Ingress path örnekleri; Prometheus/Loki uyarı yolları (yüksek seviye). |
| **Çapraz** | Faz 1 `cos-deploy-alertmanager` |

### `agentic-troubleshoot-traefik-ingress`

| Alan | Değer |
|------|--------|
| **Amaç** | LoadBalancer IP yok, proxied endpoints boş, TLS. |
| **İçerik maddeleri** | MetalLB ön koşulu; `show-proxied-endpoints`; Catalogue URL. |
| **Çapraz** | Faz 1 `cos-ingress-config`, `cos-deploy-traefik`, `microk8s-addons-dns-storage` |

### `agentic-cos-catalogue-endpoints`

| Alan | Değer |
|------|--------|
| **Amaç** | Catalogue ve proxied uçların keşfi; kullanıcıya URL iletme. |
| **İçerik maddeleri** | `juju show-unit catalogue/0` okuma rehberi; skill içinde komut örnekleri. |
| **Çapraz** | `agentic-troubleshoot-traefik-ingress` |

### `agentic-cos-no-data-playbook`

| Alan | Değer |
|------|--------|
| **Amaç** | Grafana’da “no data” için sistematik kontrol listesi. |
| **İçerik maddeleri** | Datasource → dashboard → scrape → ilişki → zaman aralığı sırası; resmi troubleshooting linkleri. |
| **Çapraz** | `agentic-troubleshoot-grafana`, `agentic-troubleshoot-prometheus` |

---

## Dal H — Kalite, paketleme, dokümantasyon, meta

### `agentic-packaging-pypi`

| Alan | Değer |
|------|--------|
| **Amaç** | `pyproject.toml`, entry point, sürümleme, `uv`/`pip` kurulum dokümantasyonu. |
| **İçerik maddeleri** | İsteğe bağlı `hatchling`/`setuptools`; konsol script adı. |
| **Çapraz** | `agentic-repo-layout`, `agentic-ci-github-actions` |

### `agentic-testing-unit`

| Alan | Değer |
|------|--------|
| **Amaç** | Birim test dizin yapısı, fixture, sağlayıcı mock sınırı. |
| **İçerik maddeleri** | pytest örünü; hangi modüller kritik % hedefi (yumuşak öneri). |
| **Çapraz** | `agentic-testing-integration-mock-llm` |

### `agentic-testing-integration-mock-llm`

| Alan | Değer |
|------|--------|
| **Amaç** | Sahte LLM ile uçtan uca tur + tool çağrısı testi tasarımı. |
| **İçerik maddeleri** | Deterministik yanıt fixture’ı; zaman sınırı. |
| **Çapraz** | `agentic-agent-turn-loop` |

### `agentic-ci-github-actions`

| Alan | Değer |
|------|--------|
| **Amaç** | PR pipeline: format, lint, test; cache; Python sürüm matrisi. |
| **İçerik maddeleri** | Fork PR’larda secret yok; örnek workflow iskeleti (YAML açıklamalı). |
| **Çapraz** | `agentic-packaging-pypi` |

### `agentic-docs-user-quickstart`

| Alan | Değer |
|------|--------|
| **Amaç** | Son kullanıcı için 5 dakikada çalıştır: cloud ve local. |
| **İçerik maddeleri** | Kopyala-yapıştır komutlar; Ollama örneği; hata giderme mini tablo. |
| **Çapraz** | `LLM_PROVIDERS.md`, `agentic-cli-entrypoint` |

### `agentic-skill-authoring-standard`

| Alan | Değer |
|------|--------|
| **Amaç** | Yeni `agentic-*` veya proje skill’i eklerken kurallar; frontmatter; çapraz referans. |
| **İçerik maddeleri** | Bu kataloga uyum; Faz 1 skill örneği ile diff; review checklist. |
| **Çapraz** | `cli/documantations/SKILL_CATALOG_PHASE2.md` (bu dosya) |

### `agentic-telemetry-optional`

| Alan | Değer |
|------|--------|
| **Amaç** | Opt-in telemetri / OpenTelemetry hatları; PII yok; örnek span isimleri. |
| **İçerik maddeleri** | Varsayılan kapalı veya açık ürün kararı placeholder; exporter env. |
| **Çapraz** | `agentic-cli-logging` |

---

## Dal I — Referans ve ileri opsiyoneller

### `agentic-reference-agentic-folder`

| Alan | Değer |
|------|--------|
| **Amaç** | Workspace `agentic/` altındaki Codex/Pywen/Claude kesitleri: hangi desen nerede; **uyarlama notları**. |
| **İçerik maddeleri** | Tablo: konu → örnek dosya yolu → ne öğrenilir; telif/lisans hatırlatması (genel). |
| **Çapraz** | `agentic-dependency-licensing`, `agentic-llm-provider-contract` |

### `agentic-sandbox-hardening-reference`

| Alan | Değer |
|------|--------|
| **Amaç** | Codex-tarzı sandbox hedefleri; Pywen’de olmayan boşlukların kapatılması yönünde rehber (uygulama kararı). |
| **İçerik maddeleri** | seatbelt/linux namespaces yüksek seviye; POC’te minimum önlem listesi. |
| **Çapraz** | `agentic-threat-model`, `agentic-tools-bash-shell` |

### `agentic-offline-airgap-notes`

| Alan | Değer |
|------|--------|
| **Amaç** | Air-gapped ortamda API yok; yalnız lokal model; pip mirror; MCP kısıtı. |
| **İçerik maddeleri** | Kontrol listesi; hangi skill’ler devre dışı kalır. |
| **Çapraz** | `agentic-llm-openai-compatible-local`, `agentic-mcp-client-config` |

### `agentic-devcontainer-optional`

| Alan | Değer |
|------|--------|
| **Amaç** | VS Code / devcontainer ile tutarlı geliştirme ortamı (opsiyonel). |
| **İçerik maddeleri** | Örnek `devcontainer.json` alanları; Docker socket risk uyarısı. |
| **Çapraz** | `agentic-repo-layout` |

### `agentic-adr-template`

| Alan | Değer |
|------|--------|
| **Amaç** | Mimari karar kaydı şablonu (dil, sağlayıcı seçimi, sandbox seviyesi). |
| **İçerik maddeleri** | ADR başlık seti: Bağlam, Karar, Sonuçlar, Alternatifler. |
| **Çapraz** | `agentic-project-charter` |

---

## Dal J — Faz 3 iç kullanım teslimatı (ek skill'ler)

### `agentic-wheel-build-verify`

| Alan | Değer |
|------|--------|
| **Amaç** | Hatchling ile wheel/sdist üretimi; temiz venv’de wheel’den kurulum smoke testi. |
| **İçerik maddeleri** | `python -m build`; `dist/` kontrolü; `agentic-packaging-pypi` ile uyum. |
| **Çapraz** | `agentic-packaging-pypi`, `agentic-ci-github-actions` |

### `agentic-docs-developer-checklist`

| Alan | Değer |
|------|--------|
| **Amaç** | `CONTRIBUTING.md` ile hizalı ruff/pytest komutları; PR öncesi kontrol listesi. |
| **İçerik maddeleri** | `sentinel-coming/cli/` kökünde çalıştırılacak komutlar; secret yok uyarısı. |
| **Çapraz** | `agentic-testing-unit`, `agentic-ci-github-actions` |

### `agentic-faz3-no-remote-telemetry`

| Alan | Değer |
|------|--------|
| **Amaç** | Faz 3’te uzaktan ürün telemetrisi kodu eklenmez; README tek cümle politikası. |
| **İçerik maddeleri** | Yerel log vs analytics ayrımı; `agentic-telemetry-optional` sonraya bırakılır. |
| **Çapraz** | `IMPLEMENTATION_PLAN_PHASE3.md`, `ROADMAP_PHASE3_5.md` |

---

## Özet: Skill kimlik listesi (oluşturulacak dosyalar)

Aşağıdaki **58** Faz 2 skill için `SKILL.md` üretilmelidir (dal sırasıyla):

`agentic-project-charter`, `agentic-repo-layout`, `agentic-dependency-licensing`, `agentic-threat-model`, `agentic-secrets-handling`, `agentic-approval-policy-design`, `agentic-prompt-injection-guardrails`, `agentic-config-layers`, `agentic-config-env-reference`, `agentic-config-profiles`, `agentic-feature-flags`, `agentic-llm-provider-contract`, `agentic-llm-openai-compatible-remote`, `agentic-llm-openai-compatible-local`, `agentic-llm-anthropic-messages`, `agentic-llm-streaming-events`, `agentic-llm-context-window-strategy`, `agentic-llm-retries-timeouts`, `agentic-cli-entrypoint`, `agentic-cli-repl-vs-once`, `agentic-cli-logging`, `agentic-cli-user-errors`, `agentic-agent-turn-loop`, `agentic-agent-tool-call-parse`, `agentic-agent-history-compaction`, `agentic-agent-multi-provider-switch`, `agentic-tools-base-contract`, `agentic-tools-bash-shell`, `agentic-tools-filesystem-read`, `agentic-tools-filesystem-write`, `agentic-tools-web-fetch-optional`, `agentic-hooks-pre-post-tool`, `agentic-mcp-client-config`, `agentic-mcp-tool-mapping`, `agentic-session-persistence`, `agentic-trajectory-recording`, `agentic-cos-advisor-overview`, `agentic-microk8s-ops-reference`, `agentic-juju-ops-reference`, `agentic-troubleshoot-grafana`, `agentic-troubleshoot-prometheus`, `agentic-troubleshoot-loki`, `agentic-troubleshoot-alertmanager`, `agentic-troubleshoot-traefik-ingress`, `agentic-cos-catalogue-endpoints`, `agentic-cos-no-data-playbook`, `agentic-packaging-pypi`, `agentic-testing-unit`, `agentic-testing-integration-mock-llm`, `agentic-ci-github-actions`, `agentic-docs-user-quickstart`, `agentic-skill-authoring-standard`, `agentic-telemetry-optional`, `agentic-reference-agentic-folder`, `agentic-sandbox-hardening-reference`, `agentic-offline-airgap-notes`, `agentic-devcontainer-optional`, `agentic-adr-template`.

**Faz 3 ekleri (3 skill):** `agentic-wheel-build-verify`, `agentic-docs-developer-checklist`, `agentic-faz3-no-remote-telemetry`. Ayrıntı: `PHASE3_SKILL_AND_DOC_INDEX.md`.
</think>


<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
StrReplace
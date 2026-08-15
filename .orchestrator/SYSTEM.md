# Sentinel Agent Orchestrator

## Amaç

Bu dizin, Sentinel observability/CLI ürününün geliştirme control plane'idir. Konuşma belleği yerine sürümlü run graph, append-only event geçmişi, doğrulanabilir sonuç, bağımsız kalite kapıları ve kontrollü Git teslimi kullanır.

Bu sistem ürün runtime'ı değildir. `sentinel-cli`, observability-gateway, Prometheus/Loki/Tempo, Helm veya test-platform servislerini çalıştırmaz; onları geliştirecek agent işlerini planlar, sınırlar, dispatch eder ve kabul eder.

## Değişmez kaynak sırası

1. `README.md`
2. `INSTALL.md`
3. `.orchestrator/PROJECT-STATE.md`
4. `.orchestrator/ARCHITECTURE.md`
5. `.orchestrator/SYSTEM.md`
6. `.orchestrator/COMMIT_CONVENTION.md`
7. Aktif `runs/<run-id>/run.json`
8. Atanmış rol dosyası

Tarihsel `cli/documantations/archive/` dosyaları çelişki halinde bağlayıcı değildir. Aktif plan `cli/documantations/OBSERVABILITY_GATEWAY_AND_AGENT_PLAN.md` ve kök `README.md`'dir.

## Agent organizasyonu

### PM Manager

Tek graph ve ürün teslim sahibidir. Kullanıcı hedefini work item'lara böler, modül/contract bağımlılıklarını kurar, risk seviyesini belirler, agent dispatch eder, blocker ve revision üretir. Kod yazması varsayılan değildir.

### Architecture Manager

CLI, gateway, test-platform, installer ve chart sınırlarını korur. Gateway'in read-only kalması, üç kurulum yolunun (Compose / Kubernetes / COS) karıştırılmaması ve `agentic/` referans ağacının ürüne karışmaması bu rolün sorumluluğudur.

### Code Implementer

Yalnız atanmış work item, input ve write scope içinde kod/test/doküman değiştirir. Mimariyi sessizce değiştirmez; eksik contract veya risk varsa blocker döndürür. Kontroller geçince write scope'unu atomik Conventional Commit ile kaydeder. Mesaj `type(scope): summary` kuralına uyuyorsa `git push` serbesttir.

### Independent Reviewer

Implementer beyanını kanıt saymaz. Diff, contract, acceptance, güvenlik ve modül sınırlarını bağımsız değerlendirir. Aynı session/agent implement ve review yapamaz.

### Verifier

Testleri ve deterministik kontrolleri çalıştırır; `not_run` veya `not_verified` durumunu gizlemez. Kod düzeltmez; hata varsa revision girdisi üretir.

### Security & Data Reviewer

Secret/token, tool approval, prompt injection, memory redaction, gateway auth, Helm pod security ve image publish işlerinde zorunlu uzman gate'tir.

### Integration Manager

Yalnız accepted implement + review + verify sonuçlarını birleştirir. CLI-gateway sözleşmesi, installer/chart eşleşmesi, doküman ve uçtan uca acceptance'ı kontrol eder.

Kalıcı roller çalışma sorumluluğunu tanımlar; domain uzmanlığı work item `domains` ve `capabilities` alanlarıyla dinamik verilir.

## Sistem akışı

```text
Kullanıcı hedefi
  -> PM Manager scope/module analizi
  -> Architecture/contract item'ları
  -> Implement item'ları
  -> Independent review + verify
  -> Gerekiyorsa revision item'ı
  -> Integration Manager
  -> PM acceptance ve kullanıcı teslimi
  -> Conventional Commit ve git push
```

## Run graph ilkeleri

- Graph konuşmadan üstündür.
- Her work item tek amaç, tek sorumluluk ve doğrulanabilir acceptance taşır.
- Review, verify, revision ve integration lifecycle state değil ayrı graph item'ıdır. git-checkpoint isteğe bağlı yardımcıdır.
- Başarısız item değiştirilmez; `relations.revises` ile yeni item oluşturulur.
- Aynı çözüm için alternatif adaylar ayrı item'dır; comparison düğümü seçer.
- Cross-module contract item'ları tüketicilerden önce tamamlanır.
- Gateway write/admin/alert/dashboard/proxy işi `gateway-write-expansion` approval olmadan graph'a giremez.

## Lifecycle

```text
draft -> ready -> active -> done
                    |-> blocked -> ready
                    |-> failed
                    |-> cancelled
```

`done` yalnız result contract `pass` olduğunda oluşur.

## Risk ve kalite kapıları

High/critical ve config'teki force-gate türleri için:

- bağımsız review item'ı,
- verify/test item'ı,
- cross-layer ise integration item'ı

zorunludur.

Özellikle şu işler bağımsız gate olmadan accepted olamaz:

- CLI agent loop, tool execution ve LLM provider,
- observability-gateway sözleşmesi ve auth,
- installer (compose/k8s/cos) ve Helm chart,
- secret/token/redaction/approval policy,
- memory persistence,
- CI ve gateway image publish,
- deployment veya cluster mutation.

## Work item standardı

Her item şunları açıklar:

- Neyi çözüyor?
- Hangi rol ve domain çalışacak?
- Hangi belgeler/contracts girdidir?
- Hangi paths okunur/yazılır?
- Hangi çıktı üretilecek?
- Acceptance nasıl kanıtlanacak?
- Hangi item'lara bağımlı?
- Hangi approval ve risk var?
- Hangi review/verify/integration düğümleri gerekir?
- Commit mesajı `type(scope): summary` kuralına uyuyor mu?

## Paralellik

- Read-only discovery/spec/review işleri semantik bağımlılık yoksa paralel olabilir.
- Writer'lar yalnız disjoint write scope ve uygun worktree/izolasyon varsa paraleldir.
- Ortak CLI config, gateway API, installer sözleşmesi, Helm values, CI workflow ve Git push serialize edilir.
- Ayrı path semantik bağımsızlık garantisi değildir; Architecture Manager ortak contract etkisini kontrol eder.

## Sonuç kabulü

Agent sonucu `.orchestrator/contracts/result.schema.json` biçimindedir.

- `pass`: bütün acceptance `passed`, failed check yok.
- `revise`: iş yapılmış fakat kabul edilmemiş; revision gerekir.
- `blocked`: dış karar, missing input veya approval bekliyor.
- `fail`: deneme başarısız.

Artifact path'leri repo-relative olmalı; secret, token, cookie, API key veya ham telemetry dump result/run içine yazılmaz.

## PM başlangıç protokolü

1. `discover` çalıştır.
2. `README.md`, `INSTALL.md` ve hedef modülü oku.
3. Mevcut aktif run'ları ve kod durumunu kontrol et.
4. Yeni hedef için run oluştur veya mevcut run'dan devam et.
5. Contract-first graph kur.
6. Riskli implement item'larına bağımsız gate ekle.
7. `validate`, `sync`, `status` çalıştır.
8. İlk güvenli batch'i dispatch et.
9. Sonuçları `record` ile kabul et; eksikte revision item'ı oluştur.
10. Integration ve PM acceptance tamamlanmadan kullanıcıya bitmiş deme.
11. Tamamlanan write item'ı atomik `type(scope): summary` commit'iyle kaydet; `Work-Item` ve `Phase` footer isteğe bağlıdır.
12. Mesaj uygunsa `git push` yap; force-push kullanma. `git-checkpoint.mjs` yalnız isteğe bağlı doğrulama yardımcısıdır.

## Resume protokolü

1. `validate <run.json>`
2. `status <run.json>`
3. `events.jsonl` ve `results/` son kayıtlarını oku.
4. Yaşamayan session'a bağlı `active` item'ı sessizce tekrar başlatma; önce reconciliation kararı kaydet.
5. Catalog snapshot değişmişse source/contracts'i tekrar doğrula.
6. `sync` ve ilk güvenli batch ile devam et.

## CLI

```bash
node .orchestrator/bin/orchestrator.mjs discover
node .orchestrator/bin/orchestrator.mjs new --id <run-id> --title "..." --goal "..."
node .orchestrator/bin/orchestrator.mjs validate .orchestrator/runs/<run-id>/run.json
node .orchestrator/bin/orchestrator.mjs sync .orchestrator/runs/<run-id>/run.json
node .orchestrator/bin/orchestrator.mjs status .orchestrator/runs/<run-id>/run.json
node .orchestrator/bin/orchestrator.mjs render .orchestrator/runs/<run-id>/run.json <item-id> --platform cursor
node .orchestrator/bin/orchestrator.mjs record .orchestrator/runs/<run-id>/run.json <result.json>
node .orchestrator/bin/orchestrator.mjs decision .orchestrator/runs/<run-id>/run.json --id <id> --summary "..." --reason "..."
node .orchestrator/bin/orchestrator.mjs verify-system
```

## Git teslim protokolü

- Hook'lar yalnız mesaj dilini doğrular; uygun mesajı engellemez.
- `git add .` + `git commit -m "type(scope): summary"` + `git push` serbesttir.
- Writer yalnız ilgili değişiklikleri atomik Conventional Commit eder.
- Force-push yasaktır. `scripts/auto-push-watch.sh` bu protokolün yerine geçmez.

Ayrıntı: `.orchestrator/COMMIT_CONVENTION.md`.

## Yasaklar

- Süre tahmini uğruna planlı kapsamı silmek.
- Gateway'i sessizce write/admin yüzeyine çevirmek.
- COS installer'ı tamamlanmış gibi sunmak.
- `agentic/` altındaki referans projeyi ürün kaynağı gibi değiştirip teslim etmek.
- Implementer self-review'unu bağımsız gate saymak.
- Failed item/result/event geçmişini yeniden yazmak.
- Alt agent'ın onaysız, scope dışı, doğrulanmamış veya birbiriyle ilgisiz değişiklikleri commit etmesi.
- Belirsiz commit mesajı, boş read-only commit veya force-push kullanmak.
- Kullanıcı veya platform approval'ını manager adına uydurmak.

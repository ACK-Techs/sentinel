# Sentinel Orchestrator Mimari Kararları

## Kontrol düzlemi

Sistem, AI agent framework daemon'ı değildir. Muhakemeyi manager modele; invariant, scheduling, history ve handoff üretimini dependency-free Node çekirdeğine verir.

```text
Manager reasoning
  + JSON run graph
    + JSONL append-only events
    + immutable results
    + platform adapters
    + role protocols
    + controlled Git checkpoints
```

## Neden ürün runtime'ından ayrı?

Ürün runtime'ı `sentinel-cli`, FastAPI observability-gateway, Prometheus/Loki/Tempo, Helm chart, Compose installer ve test-platform servisleridir. Orchestrator yalnız bunların geliştirilmesini yönetir. İki katman karıştırılmaz:

- `.orchestrator`: geliştirme agent control plane'i.
- `cli/`, `observability-gateway/`, `test-platform/`, `charts/`: ürün ve lab runtime'ı.

## Sabit roller ve dinamik uzmanlık

PM, architecture, implementer, reviewer, verifier, security ve integration sorumlulukları tekrar eden governance rolleri olduğu için kalıcı protokoldür. Modül/teknoloji uzmanlığı sabit agent listesi değildir; work item `domains` ve `capabilities` ile atanır.

Örnek capabilities:

```text
cli-commands
agent-loop
llm-adapters
tool-registry
observability-gateway
prometheus-query
compose-install
helm-chart
cos-discovery
test-platform
secret-handling
approval-policy
```

## JSON graph ve küçük lifecycle

Domain/kind açık uçlu; lifecycle küçüktür. Review, integration veya git-checkpoint state değildir çünkü kendi girdisi, sonucu, agent'ı ve acceptance kanıtı vardır.

## Contract-first graph

Modül sınırını geçen her özellik en az şu yapıya ayrılır:

```text
pm-scope
  -> architecture-contract
     -> implementation(s)
        -> independent-review
        -> verification
           -> integration
                 -> pm-acceptance
```

Küçük ve düşük riskli tek-modül değişikliklerinde PM scope ile contract aynı item olabilir; risk gate politikası değişmez.

## Platform bağımsızlığı

Canonical run platform tool adlarını içermez. Codex, Cursor ve Claude adapter'ları dispatch guidance verir. Native subagent/worktree varsa kullanılır; yoksa `render` paste-ready prompt üretir.

## History ve concurrency

- `run.json` güncel snapshot.
- `events.jsonl` append-only audit.
- `results/` immutable attempt sonuçları.
- `revision` optimistic concurrency.
- `.lock` kısa filesystem mutation lock'u.

## Repository hedef yapısı

```text
cli/                         # sentinel-cli Python paketi
observability-gateway/       # read-only FastAPI telemetry API
test-platform/               # hedef uygulama, load, chaos, smoke
charts/sentinel/             # Kubernetes Helm chart
for-download/                # Compose bundle ve COS lab scriptleri
scripts/                     # MicroK8s/COS yardımcı scriptler
skills/                      # operasyonel skill belgeleri
documantations/              # kök dokümantasyon
.github/workflows/           # CLI CI ve gateway image
agentic/                     # referans projeler; ürün değil
.orchestrator/               # bu control plane
```

`agentic/` `doNotTouch` altındadır. Orchestrator catalog onu ürün source root saymaz.

## Projeye özgü kalite invariant'ları

1. Observability gateway read-only'dir; alert, dashboard, backend write veya Grafana proxy eklemek ayrı approval ister.
2. CLI, Prometheus/Loki/Tempo'ya doğrudan bağlanmaz; telemetry gateway üzerinden gider.
3. Secret'lar committed YAML'a yazılmaz; env ve `.env.example` placeholder kullanılır.
4. Compose, Kubernetes ve COS kurulum yolları ayrıdır; `sentinel install --mode cos` COS kurucusu değildir.
5. `agentic/` referans koddur; Sentinel ürünü `cli/`, `observability-gateway/` ve ilgili lab/deploy ağaçlarındadır.
6. Tool execution approval, timeout, output limit ve read-only bash varsayılan güvenlik yüzeyidir; sessizce kapatılmaz.
7. Memory/session yazıları redaction'dan geçer; ham secret persist edilmez.
8. Gateway hata mesajları secret sızdırmaz.
9. Test-platform lab'dır; production tenant veya gerçek ödeme verisi taşımaz.
10. COS installer preflight/install/verify TODO'su tamamlanmış iddia edilemez.
11. Image publish ve cluster mutation kullanıcı/platform approval ister.
12. `scripts/auto-push-watch.sh` orchestrator teslim protokolünün yerine geçmez.

Bu invariant'ları etkileyen item `high` veya `critical` risk alır ve architecture/security review gerektirir.

## Git checkpoint mimarisi

Writer commit'leri Conventional Commit dilindedir. Mesaj uygunsa `git add` / `git commit` / `git push` serbesttir. `commit-msg` ve `pre-push` yalnız bu dili doğrular. Force-push yapılmaz.

## Genişletme kuralı

Yeni kalıcı role ancak farklı run'larda tekrar eden ayrı sorumluluk ve farklı permission/model/tool ihtiyacı kanıtlanırsa eklenir. Yeni relation veya lifecycle state, mevcut graph semantiğiyle kayıpsız ifade edilemiyorsa eklenir.

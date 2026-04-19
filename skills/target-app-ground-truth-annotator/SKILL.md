---
name: target-app-ground-truth-annotator
description: scripts/scenario_runner.py — chaos senaryo başlat/bitir; namespace annotation + ground-truth.jsonl ile precision/recall için etiket üretir.
---

## Purpose
Her chaos/load senaryosu için **makine-okunur ground-truth** üretmek: senaryo başlangıç/bitiş zamanı, hangi servis(ler)in etkilendiği, hangi profil uygulandı. Sentinel'in ürettiği alarmlar sonradan bu etiketlere göre **precision / recall / MTTD** metriklerine çevrilir.

## When to Use
- Elle veya CI'dan chaos senaryosu tetiklerken.
- Offline replay / analiz sırasında log'u tekrar toplarken.
- Yeni bir senaryo profili eklerken annotation şemasını genişletmek için.

## Contract / Interface
CLI:
```
python scripts/scenario_runner.py run \
    --scenario flash-crowd \
    --chaos-profile degraded \
    --target-services orders,payments \
    --duration 600
```
Yan etkiler:
1. `t0` anında namespace `sentinel-target`'a annotation ekler:
   - `sentinel.io/chaos-start: "<RFC3339>"`
   - `sentinel.io/chaos-profile: "degraded"`
   - `sentinel.io/chaos-services: "orders,payments"`
   - `sentinel.io/scenario-id: "<uuid>"`
2. Her target serviste `POST /admin/chaos/profile` ile profili uygular.
3. Load generator job'u ayrı bir Job olarak apply edilir (senaryo YAML `SCENARIO` env ile).
4. `t1` bitişinde:
   - `sentinel.io/chaos-end: "<RFC3339>"` annotation'ı (start silinmez; audit trail).
   - Her hedef serviste profil `normal`'e çekilir.
5. Her adım `ground-truth.jsonl` dosyasına (default: `./artifacts/ground-truth.jsonl`) JSON satır olarak append edilir.

`ground-truth.jsonl` kayıt şeması:
```json
{"scenario_id":"...", "ts":"2026-04-19T10:00:00Z", "event":"chaos_start",
 "profile":"degraded", "services":["orders","payments"],
 "scenario":"flash-crowd", "duration_s":600}
```
`event ∈ {chaos_start, chaos_end, load_start, load_end, aborted}`.

## Implementation Notes
- Kubernetes client: `kubernetes` Python paketi; annotation için `patch_namespace`.
- UUID `scenario_id` hem annotation hem JSONL'de tekrar eder — join anahtarı.
- Zaman kaynağı `datetime.now(tz=timezone.utc)`; saniye çözünürlüğü Sentinel eval için yeterli.
- Signal handler (SIGINT/SIGTERM) → `aborted` event'i yaz + profiles `normal`'e revert.
- `--dry-run` flag'i sadece JSONL'e yazar, cluster'ı etkilemez (replay).
- Scenario-runner pod'u NetworkPolicy ile hem `/admin/chaos` hem K8s API'a yetkili tek workload.
- RBAC: namespace scope, `patch` on `namespaces` + `create` on `jobs`.

## Anti-patterns
1. Annotation'ı pod labels'e koymak — pod'lar restart olunca kaybolur; namespace scope kalıcıdır.
2. Ground-truth zamanını scenario-runner lokal clock'undan değil de **her servisin kendi saatinden** toplamak — clock skew precision/recall'u bozar. Tek source-of-truth runner clock.
3. `chaos_end` event'ini atlamak (fire-and-forget) — açık kalan pencere tüm sonraki alarmları "anomali" olarak etiketler.
4. JSONL yerine CSV / düz text kullanmak — şema evrimi zorlaşır, nested services listesi bozulur.
5. Scenario ID'yi senaryo ismine eşitlemek (`"flash-crowd"`) — aynı profili 2 kez koşmak idempotent olur, ayrı pencere etiketlenemez.

## Example Snippet
```python
# scripts/scenario_runner.py
import json, uuid, time, argparse, datetime as dt, httpx
from kubernetes import client, config

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()

def annotate(ns: str, patch: dict):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    v1.patch_namespace(ns, {"metadata": {"annotations": patch}})

def write_gt(path, rec): 
    with open(path, "a") as f: f.write(json.dumps(rec) + "\n")

def run(args):
    sid = str(uuid.uuid4())
    ns = "sentinel-target"
    services = args.target_services.split(",")
    annotate(ns, {
        "sentinel.io/chaos-start": now(),
        "sentinel.io/chaos-profile": args.chaos_profile,
        "sentinel.io/chaos-services": args.target_services,
        "sentinel.io/scenario-id": sid,
    })
    for s in services:
        httpx.post(f"http://{s}.{ns}.svc:8000/admin/chaos/profile",
                   json={"profile": args.chaos_profile}, timeout=5)
    write_gt(args.out, {"scenario_id": sid, "ts": now(), "event": "chaos_start",
                        "profile": args.chaos_profile, "services": services,
                        "scenario": args.scenario, "duration_s": args.duration})
    try:
        time.sleep(args.duration)
    finally:
        for s in services:
            httpx.post(f"http://{s}.{ns}.svc:8000/admin/chaos/profile",
                       json={"profile": "normal"}, timeout=5)
        annotate(ns, {"sentinel.io/chaos-end": now()})
        write_gt(args.out, {"scenario_id": sid, "ts": now(), "event": "chaos_end",
                            "scenario": args.scenario})
```

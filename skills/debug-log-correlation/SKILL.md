---
name: debug-log-correlation
description: "Birden fazla Sentinel servisinden gelen log'ları trace ID veya correlation ID üzerinden ilişkilendirip kronolojik olay zinciri oluşturur"
---

## Purpose
Sentinel'in dağıtık mimarisinde bir hata genellikle birden fazla servisi geçer: gateway → orders → payments → inventory. Bu skill, tek bir trace ID veya correlation ID üzerinden tüm servis log'larını Loki'de birleştirip tam olay zincirini kronolojik sırayla sunar.

## Workflow

### 1. Başlangıç trace ID'sini belirle
```bash
# Gateway log'undan hatalı trace ID'sini bul
logcli query '{service="gateway", level="error"} | json | line_format "{{.trace_id}} {{.message}}"' \
  --limit=10 --since=30m
```

### 2. Tüm servislerden o trace ID'li log'ları topla
```bash
TRACE_ID="4bf92f3577b34da6a3ce929d0e0e4736"

logcli query "{trace_id=\"${TRACE_ID}\"}" \
  --limit=500 --since=1h \
  -o jsonl | jq -r '[.timestamp, .labels.service, .line] | @tsv' | sort
```

### 3. Loki multi-line JSON log'unu ayrıştır
```bash
# Structured log'ları normalleştir
logcli query "{trace_id=\"${TRACE_ID}\"}" -o jsonl | \
  jq -r '.line | fromjson | [.timestamp, .service, .level, .message, .span_id] | @csv' | \
  sort -t, -k1
```

### 4. Span-to-span zincirini Tempo ile çapraz doğrula
```bash
# Tempo'dan tam span ağacını al
curl -s "http://tempo.sentinel-cos.svc:3200/api/traces/${TRACE_ID}" | \
  jq '.batches[].scopeSpans[].spans[] | {
    name: .name,
    spanId: .spanId,
    parentSpanId: .parentSpanId,
    startTime: .startTimeUnixNano,
    status: .status
  }' | jq -s 'sort_by(.startTime)'
```

### 5. Timeline oluştur
```
10:05:01.234 [gateway]   → POST /orders HTTP 200 başladı
10:05:01.256 [orders]    → order.create span başladı
10:05:01.290 [payments]  → payment.charge span başladı
10:05:01.450 [payments]  → ERROR: insufficient_funds — span hata ile kapandı
10:05:01.460 [orders]    → payment failed, saga compensation başladı
10:05:01.480 [inventory] → stock.release span
10:05:01.510 [gateway]   → HTTP 402 yanıt döndü
```

### 6. Eksik log uyarısı
Bir servis log üretmemişse:
- OTEL exporter down mu? `kubectl logs -n sentinel-target deploy/<svc> | grep "otel exporter"`
- Log level çok yüksek mi? `INFO` log'lar `WARN` level'da bastırılıyor olabilir.

## Common mistakes
1. `logcli` sorgusunda `trace_id` label yerine log satırı içindeki alanı aramak — Loki label extraction pipeline'ı olmadan regex gerekir.
2. Zaman senkronizasyonunu göz ardı etmek — farklı pod'ların clock'u ±50ms sapabilir; mutlak sıra değil, span parent-child ilişkisine güven.
3. Sadece error level log'lara bakmak — `WARN` log'lar erken uyarı sinyali olabilir ve zincirde eksik halka bırakır.
4. Tempo'dan span çekerken truncated response almak — büyük trace'ler için `?limit=10000` parametresi gerekli.

## References
- `skills/obs-tempo-trace-query`
- `skills/obs-tempo-pipeline-e2e`
- `skills/debug-api-request-replay`

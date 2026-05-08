---
name: debug-api-request-replay
description: "Başarısız bir API isteğini Tempo trace'inden veya Loki log'undan çıkarıp birebir tekrar oynatır ve farkı gösterir"
---

## Purpose
Üretim veya staging ortamında gerçekleşen başarısız bir API çağrısını, aynı header/body/auth ile tekrar tetikleyerek hatayı yerel veya test ortamında yeniden üretmek. Sentinel'in Tempo + Loki altyapısından istek detayları çekilir; `httpie` veya `curl` komutu otomatik üretilir.

## Workflow

### 1. Trace ID ile isteği bul
```bash
# Loki'den hata veren trace'i çek
logcli query '{service="orders"} |= "500" | json' \
  --from="2024-01-15T10:00:00Z" --to="2024-01-15T10:05:00Z" \
  --limit=5 | jq '.traceId'
```

### 2. Tempo'dan span detayını çek
```bash
TRACE_ID="abc123def456"
curl -s "http://tempo.sentinel-cos.svc:3200/api/traces/${TRACE_ID}" | \
  jq '.batches[].scopeSpans[].spans[] | select(.name == "POST /orders") | {
    traceId: .traceId,
    attributes: .attributes
  }'
```

### 3. Orijinal isteği yeniden oluştur
Span attribute'larından şu alanları al:
- `http.url` → endpoint
- `http.method` → method
- `http.request_content_length` → body boyutu
- `user_agent.original` → User-Agent
- `http.request.header.x-request-id` → trace/correlation ID

### 4. Request body'yi Loki'den çek
```bash
logcli query '{service="orders", span_id="<span_id>"} | json | line_format "{{.request_body}}"'
```

### 5. Replay komutu oluştur
```bash
# Otomatik üretilen replay komutu
curl -X POST "http://orders.sentinel-target.svc/orders" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: replay-$(date +%s)" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -d '{"product_id": "sku-123", "quantity": 2, "user_id": "u-456"}' \
  -v 2>&1 | tee /tmp/replay-response.txt
```

### 6. Fark analizi
```bash
# Orijinal hata
ORIG_STATUS=500
ORIG_BODY='{"error": "insufficient_stock"}'

# Replay sonucu
REPLAY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" ...)
diff <(echo "$ORIG_BODY") <(cat /tmp/replay-response.txt | jq .)
```

### 7. Chaos middleware ile deterministic replay
```bash
# Önce chaos state'i orijinal hata anındaki gibi ayarla
curl -X POST http://orders.sentinel-target.svc/admin/chaos \
  -d '{"error_rate": 0.0, "db_slow": 500}'

# Sonra replay
```

## Common mistakes
1. Replay sırasında `X-Request-ID` header'ını değiştirmemek — bazı idempotency logic'leri duplicate kabul eder.
2. Auth token'ı orijinal istek anındaki token ile replay etmeye çalışmak — token süresi geçmiş olabilir, test token kullan.
3. Chaos state'i sıfırlamadan replay yapmak — rastgele hata enjeksiyonu sonucu değiştirir.
4. Span attribute'larında body'nin tam olmadığını görmezden gelmek — büyük body'ler truncate edilir, Loki log'una bak.

## References
- `skills/debug-log-correlation`
- `skills/target-app-chaos-api`
- `skills/obs-tempo-trace-query`

---
name: debug-juju-hook-failure
description: "Juju hook hatasını kaydeder, tekrar üretir ve root cause analizini yapar; Sentinel COS charm'larına özgü hata kalıplarını kapsar"
---

## Purpose
Sentinel'in COS altyapısı Juju charm'larla yönetilir. Hook hataları (`config-changed`, `relation-joined`, `install`) charm'ı `error` state'ine sokar ve servis kesintisine neden olur. Bu skill, hook hatasının tam nedenini izole eder ve charm'ı güvenli şekilde kurtarır.

## Workflow

### 1. Hatalı birimi ve hook'u tespit et
```bash
juju status --format=json | jq '.applications | to_entries[] | 
  select(.value.units != null) | 
  .value.units | to_entries[] | 
  select(.value."agent-status".current == "error") | 
  {unit: .key, message: .value."agent-status".message}'
```

### 2. Hook log'larını oku
```bash
# Birim log'larını gerçek zamanlı izle
juju debug-log --include-module unit --replay --level ERROR -n 200

# Belirli birim
juju debug-log --include-module unit:prometheus/0 --replay -n 100
```

### 3. Hook'u interaktif debug modunda çalıştır
```bash
# debug-hooks ile hook'u paused state'de yakala
juju debug-hooks prometheus/0 config-changed

# Yeni terminal: hook'u tetikle
juju config prometheus scrape_interval=30s

# debug-hooks terminalinde:
# 1. Hook script'ini gör: cat $JUJU_DISPATCH_PATH
# 2. Env değişkenlerini gör: env | grep JUJU
# 3. Manuel adım adım çalıştır: bash -x hooks/config-changed
```

### 4. Yaygın Sentinel COS hook hataları

#### Relation data format hatası
```bash
# relation-get ile ilişki datasını kontrol et
juju run --unit prometheus/0 "relation-get -r <relation-id> - grafana/0"
# Beklenen format: {"grafana_host": "...", "grafana_port": "3000"}
```

#### Charm config validation hatası
```bash
# Config değerini doğrula
juju config prometheus | grep -A3 "scrape_interval"
# Regex veya type validation hatalarını görmek için
juju config prometheus scrape_interval=invalid 2>&1
```

#### Python dependency eksikliği
```bash
# Charm venv'ini kontrol et
juju exec --unit prometheus/0 "ls /var/lib/juju/agents/unit-prometheus-0/charm/venv/"
# Eksik kütüphane varsa charm refresh ile güncelle
juju refresh prometheus --path ./charms/prometheus
```

### 5. Charm'ı error state'inden kurtar
```bash
# Hook'u başarılı olarak işaretle ve devam et
juju resolved prometheus/0

# Veya tüm hatalı birimleri toplu düzelt
juju status --format=json | jq -r '.applications[].units | 
  to_entries[] | select(.value."agent-status".current == "error") | .key' | \
  xargs -I{} juju resolved {}
```

### 6. Root cause raporla
```bash
# Hook çalışma süresi ve kaynak tüketimi
juju debug-log --include-module unit:prometheus/0 | grep "hook.*duration\|hook.*failed"
```

## Common mistakes
1. `juju resolved` yapmadan önce asıl hatayı düzeltmemek — charm tekrar aynı hataya düşer.
2. `debug-hooks` terminalini kapamadan hook timeout beklemek — default 5 dakika timeout, uzatmak için `JUJU_HOOK_TIMEOUT` env.
3. Relation data'yı doğrudan edit etmeye çalışmak — yalnızca charm kodu üzerinden `relation-set` ile değişir.
4. Multi-unit deployment'ta sadece bir birimi fix etmek — diğer birimler leader election sonrası aynı hook'u tekrar çalıştırır.

## References
- `skills/debug-config-mismatch`
- `skills/cos-bundle-overview`
- `skills/cos-custom-charm-relation`

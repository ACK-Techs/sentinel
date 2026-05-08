---
name: juju-status-parsing
description: "juju status çıktısını JSON formatında alıp otomasyon script'lerinde ayrıştırmak, bekleme döngüleri yazmak, uygulama/unit durumunu programatik olarak sorgulamak gerektiğinde kullan."
---

## Purpose
`juju status` insan okumak için tasarlanmıştır. Otomasyon için `--format=json` ve `jq` kombinasyonu kullanılır; Bash/Python script'lerinde durum kontrolü böyle yapılır.

## Temel JSON yapısı
```bash
juju status --format=json | jq .
```

Ana alanlar:
- `.applications.<ad>.status.current`: `active | blocked | waiting | maintenance`
- `.applications.<ad>.units.<unit>.agent-status.current`: `idle | executing | error`
- `.machines.<id>.instance-status.current`: bare-metal için

## Yaygın sorgular

### Tüm uygulamaların durumu
```bash
juju status --format=json | jq '.applications | to_entries[] | {app: .key, status: .value.status.current}'
```

### Bloklanan uygulamaları bul
```bash
juju status --format=json | jq '.applications | to_entries[] | select(.value.status.current == "blocked") | .key'
```

### Bekle (uygulama hazır olana kadar)
```bash
until [[ "$(juju status myapp --format=json | jq -r '.applications.myapp.status.current')" == "active" ]]; do
  echo "Bekleniyor..."
  sleep 10
done
```

### Unit IP adresi
```bash
juju status --format=json | jq -r '.applications."prometheus-k8s".units."prometheus-k8s/0"."public-address"'
```

## Python'da kullanım
```python
import subprocess, json
result = subprocess.run(["juju", "status", "--format=json"], capture_output=True)
status = json.loads(result.stdout)
app_status = status["applications"]["prometheus-k8s"]["status"]["current"]
```

## Common mistakes
- `juju status` çıktısını `grep` ile ayrıştırmak — format değişince script bozulur.
- Unit adındaki `/` karakterini `jq` içinde kaçırmayı unutmak: `."prometheus-k8s/0"`.

## References
- `skills/juju-debug-log`
- `skills/juju-troubleshoot-blocked`
- `skills/juju-bundle-deploy`

---
name: docs-version-matrix
description: "Sentinel bileşenleri için versiyon uyumluluk matrisi oluşturur ve deprecation politikasını yönetir"
---

## Purpose
Sentinel'in bileşenleri — COS charm'ları, Kubernetes, Python, target servis versiyonları — birbirinden bağımsız yayınlanır. Hangi kombinasyonların test edildiğini ve desteklendiğini netleştiren bir versiyon matrisi, upgrade planlamasını kolaylaştırır ve "neden çalışmıyor?" sorularını azaltır.

## Workflow

### 1. Versiyon matrisi yapısı
```markdown
# Versiyon Uyumluluk Matrisi

## Desteklenen Kombinasyonlar

| Sentinel | COS | MicroK8s | Python | PostgreSQL | Durum |
|----------|-----|----------|--------|------------|-------|
| 2.1.x | 0.47 | 1.28 | 3.11 | 14 | Aktif (LTS) |
| 2.0.x | 0.45 | 1.27 | 3.11 | 14 | Güvenlik desteği |
| 1.9.x | 0.43 | 1.26 | 3.10 | 13 | EOL 2024-06 |

## COS Bileşen Versiyonları (Sentinel 2.1.x)
| Bileşen | Versiyon | Charm | Kanal |
|---------|----------|-------|-------|
| Prometheus | 2.47.0 | prometheus-k8s | 1/stable |
| Grafana | 10.2.0 | grafana-k8s | 1/stable |
| Loki | 2.9.0 | loki-k8s | 1/stable |
| Tempo | 2.3.0 | tempo-k8s | 1/edge |
| OTel Collector | 0.89.0 | otel-k8s | 1/stable |
```

### 2. Otomatik matrisi güncelleme
```bash
# Kurulu charm versiyonlarını çek
juju status --format=json | jq '{
  applications: [
    .applications | to_entries[] | {
      name: .key,
      version: .value."charm-version",
      channel: .value.channel
    }
  ]
}' > documentations/versions/current-deployment.json

# Markdown matrise dönüştür
python scripts/gen_version_matrix.py \
  --input documentations/versions/current-deployment.json \
  --output documentations/versions/matrix.md
```

### 3. Deprecation politikası
```markdown
## Deprecation Politikası

### Destek döngüsü
- **Aktif (LTS)**: Tüm bug fix + güvenlik yamaları, 18 ay
- **Güvenlik desteği**: Sadece güvenlik yamaları, 6 ay
- **EOL**: Destek yok, upgrade zorunlu

### Deprecation duyurusu
1. EOL tarihinden 3 ay önce: CHANGELOG + release notes'ta duyuru
2. 1 ay önce: README'ye deprecation banner ekle
3. EOL tarihinde: versiyon matristen "EOL" olarak işaretle

### Özellik deprecation
```python
import warnings

def old_endpoint_handler():
    warnings.warn(
        "Bu endpoint v3.0'da kaldırılacak. /v2/orders kullanın.",
        DeprecationWarning,
        stacklevel=2
    )
```

### 4. Upgrade kılavuzu referansı
```markdown
## Upgrade Kılavuzları
| Kaynak | Hedef | Kılavuz |
|--------|-------|---------|
| 2.0.x | 2.1.x | [docs/upgrade/2.0-to-2.1.md](docs/upgrade/2.0-to-2.1.md) |
| 1.9.x | 2.0.x | [docs/upgrade/1.9-to-2.0.md](docs/upgrade/1.9-to-2.0.md) |
```

### 5. CI'da versiyon matrisi testi
```yaml
# .github/workflows/matrix.yml
strategy:
  matrix:
    python: ["3.11", "3.12"]
    postgres: ["14", "15"]
steps:
  - name: Test combination
    run: pytest tests/integration/ -v
    env:
      PYTHON_VERSION: ${{ matrix.python }}
      POSTGRES_VERSION: ${{ matrix.postgres }}
```

### 6. Breaking change izleme
```bash
# Mevcut API ile karşılaştır
openapi-diff documentations/api/v1/openapi.json documentations/api/v2/openapi.json \
  --fail-on-incompatible
```

## Common mistakes
1. Matrisi yalnızca major release'lerde güncellemek — minor charm versiyonları da uyumsuzluk çıkarabilir.
2. EOL versiyonu hemen matristeki tablodan silmek — geçmiş referans için "EOL" kolonu ile tut.
3. Upgrade kılavuzunu test etmeden yayınlamak — kılavuzu takip ederek gerçek upgrade yap.
4. Deprecation uyarılarını log'a yazmak ama metric'e dönüştürmemek — kaç kullanıcı eski API kullanıyor ölçülmeli.

## References
- `skills/docs-changelog-format`
- `skills/cos-upgrade-strategy`
- `skills/ci-semantic-versioning`

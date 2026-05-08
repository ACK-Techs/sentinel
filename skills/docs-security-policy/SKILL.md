---
name: docs-security-policy
description: "Sentinel projesi için SECURITY.md ve güvenlik açığı bildirme politikası; responsible disclosure süreci"
---

## Purpose
Sentinel açık kaynak bir proje olarak güvenlik açıkları için sorumlu açıklama (responsible disclosure) politikası gerektirir. Bu skill, SECURITY.md dosyasını, triaj sürecini ve CVE bildirme iş akışını tanımlar.

## Workflow

### 1. SECURITY.md yapısı
```markdown
# Güvenlik Politikası

## Desteklenen Versiyonlar
| Versiyon | Güvenlik Desteği |
|----------|-----------------|
| 2.1.x | Aktif |
| 2.0.x | Evet |
| < 2.0 | Hayır |

## Güvenlik Açığı Bildirme

**Lütfen GitHub Issues kullanmayın.**

Güvenlik açıklarını şu adrese özel olarak bildirin:
`security@sentinel-project.io`

### Bildirimde şunları belirtin:
- Açığın türü (XSS, SQLi, RCE, vb.)
- Etkilenen bileşen ve versiyon
- Yeniden üretme adımları
- Olası etki

## Yanıt SLA'sı
| Aşama | Süre |
|-------|------|
| İlk onay | 48 saat |
| Triaj ve önceliklendirme | 5 iş günü |
| Düzeltme tahmini | 30 gün (kritik: 7 gün) |
| Açıklama (disclosure) | Düzeltmeden 90 gün sonra |

## Kapsamdaki Bileşenler
- Target servis API'leri (orders, payments, gateway, inventory)
- Chaos API (/admin/chaos) — NetworkPolicy ile korunmalı
- COS entegrasyon noktaları

## Kapsam Dışı
- Third-party charm güvenlik açıkları (Canonical'a bildir)
- Demo ortam veri güvenliği (PII içermez)
```

### 2. Güvenlik tarama pipeline'ı
```yaml
# .github/workflows/security.yml
name: Security Scan
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'  # Pazartesi 02:00

jobs:
  sast:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Bandit (Python SAST)
        run: |
          pip install bandit
          bandit -r services/ -f json -o reports/bandit.json || true
          bandit -r services/ --severity-level medium

  dependency-scan:
    name: Dependency Vulnerabilities
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Safety check
        run: |
          pip install safety
          safety check --json > reports/safety.json

  container-scan:
    name: Container Scan
    runs-on: ubuntu-latest
    steps:
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
```

### 3. Secret sızıntı kontrolü
```bash
# gitleaks ile commit geçmişinde secret tarama
gitleaks detect --source . --report-format json --report-path reports/gitleaks.json

# Pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
gitleaks protect --staged --redact
EOF
chmod +x .git/hooks/pre-commit
```

### 4. Chaos API güvenlik kontrolü
```bash
# NetworkPolicy kontrolü — /admin/chaos dışarıya kapalı mı?
kubectl get networkpolicy -n sentinel-target chaos-api-policy -o yaml | \
  grep -A10 "ingress:"

# Beklenen: sadece sentinel-scenario-runner pod'undan erişim
```

### 5. Güvenlik açığı işleme süreci
```bash
# GitHub Security Advisory oluştur
gh api repos/{owner}/{repo}/security-advisories \
  -X POST \
  -f summary="RCE via unsanitized chaos config" \
  -f description="..." \
  -f severity="critical"
```

## Common mistakes
1. Güvenlik bildirimi için GitHub Issues kullanmaya izin vermek — açık issue herkes görür, exploit yayılır.
2. `/admin/chaos` endpoint'ini public ingress'e açmak — üretim benzeri sistemde kritik güvenlik riski.
3. Güvenlik taramasını CI'a ekleyip sonuçları görmezden gelmek — `exit-code: 1` ile build'i kır.
4. CVE açıklamasından önce tüm kullanıcıların upgrade etmesini beklemek — 90 gün standardını takip et.

## References
- `skills/docs-license-compliance`
- `skills/ci-pr-gate`
- `skills/target-app-chaos-api`

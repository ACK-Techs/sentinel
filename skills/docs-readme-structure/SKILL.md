---
name: docs-readme-structure
description: "Sentinel monorepo ve alt servis README.md dosyaları için etkili yapı ve içerik kılavuzu"
---

## Purpose
İyi bir README, yeni bir geliştiricinin 10 dakika içinde Sentinel'i çalıştırıp anlayabilmesini sağlar. Bu skill, monorepo kökü ve her servis için farklı README yapıları tanımlar; gereksiz tekrardan kaçınır, arama motorları için optimize eder.

## Workflow

### 1. Monorepo kök README yapısı
```markdown
# Sentinel

> Kubernetes ortamında anomali tespiti için gözlemlenebilirlik platform test aracı.

[![CI](badge)] [![Coverage](badge)] [![License](badge)]

## Nedir?
2-3 cümle: ne yapar, kimin için, hangi problemi çözer.

## Mimari
[Kısa diyagram veya link — skills/docs-diagram-as-code]

## Hızlı Başlangıç
```bash
git clone ...
cd sentinel-coming
make setup    # MicroK8s + COS + target services
make test     # smoke test
```

## Dizin Yapısı
```
sentinel-coming/
├── services/       # Target FastAPI servisleri
├── skills/         # Claude Code skill'leri
├── documentations/ # ADR, runbook, post-mortem
├── helm/           # Helm chart'ları
└── .github/        # CI workflow'ları
```

## Servisler
| Servis | Port | Açıklama |
|--------|------|----------|
| gateway | 8080 | API yönlendirici |
| orders | 8001 | Sipariş yönetimi |
| payments | 8002 | Ödeme işleme |
| inventory | 8003 | Stok yönetimi |

## Dokümantasyon
- [ADR'lar](documentations/adr/)
- [Runbook'lar](documentations/runbooks/)
- [API Referansı](documentations/api/)

## Katkıda Bulunma
Bkz. [CONTRIBUTING.md](CONTRIBUTING.md)
```

### 2. Servis README yapısı (örn. services/orders/)
```markdown
# Orders Service

Sipariş oluşturma, listeleme ve iptal API'si. Saga pattern ile payments ve inventory servisleriyle koordinasyon sağlar.

## Endpoints
| Method | Path | Açıklama |
|--------|------|----------|
| POST | /orders | Yeni sipariş |
| GET | /orders/{id} | Sipariş detayı |
| DELETE | /orders/{id} | İptal |

## Bağımlılıklar
- PostgreSQL (sipariş veritabanı)
- Redis (idempotency cache)
- payments service (HTTP)
- inventory service (HTTP)

## Yerel Geliştirme
```bash
cd services/orders
docker compose up -d db redis
uvicorn app.main:app --reload
```

## Ortam Değişkenleri
| Değişken | Varsayılan | Açıklama |
|----------|-----------|---------|
| DATABASE_URL | postgresql://... | PostgreSQL bağlantısı |
| REDIS_URL | redis://localhost | Cache |
| PAYMENTS_URL | http://payments:8002 | Downstream |

## Chaos Kontrolleri
Bkz. `skills/target-app-chaos-api`
```

### 3. README kalite kontrol
```bash
# Gerekli bölümleri kontrol et
for section in "## Nedir\|## What" "## Hızlı Başlangıç\|## Quick Start" "## Katkı\|## Contributing"; do
  grep -qE "$section" README.md || echo "MISSING: $section"
done

# Kırık link kontrolü
grep -oP '\[.*?\]\(\K[^)]+' README.md | grep -v '^http' | while read link; do
  [ ! -e "$link" ] && echo "BROKEN: $link"
done
```

### 4. Badge otomasyonu
```markdown
[![CI](https://github.com/sentinel/sentinel-coming/actions/workflows/ci.yml/badge.svg)](...)
[![codecov](https://codecov.io/gh/sentinel/sentinel-coming/branch/main/graph/badge.svg)](...)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
```

## Common mistakes
1. Her şeyi tek README'ye doldurmak — 500 satırı aşınca kimse okumaz; ayrı dok dosyalarına böl.
2. "Bu proje..." ile başlamak — proje adı zaten başlıkta, hemen değer önermesine geç.
3. Kurulum adımlarını test etmemek — yeni bir makinede baştan takip et, eksik adımları bul.
4. Badges'leri güncel tutmamak — kırık badge güvensizlik yaratır; otomatik generate et.

## References
- `skills/docs-contributing-guide`
- `skills/docs-onboarding-checklist`
- `skills/docs-diagram-as-code`

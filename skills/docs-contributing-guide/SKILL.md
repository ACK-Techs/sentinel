---
name: docs-contributing-guide
description: "Sentinel monoreposu için CONTRIBUTING.md yazımı ve yeni katkıcı onboarding süreci standardı"
---

## Purpose
Açık ve sağlıklı bir katkı kılavuzu, PR sürecini hızlandırır, kod kalitesini korur ve yeni geliştiricilerin ilk commit'ini güvenle atmalarını sağlar. Bu skill, Sentinel'e özgü katkı kurallarını ve review beklentilerini tanımlar.

## Workflow

### 1. CONTRIBUTING.md temel yapısı
```markdown
# Katkıda Bulunma Kılavuzu

Sentinel'e katkı yapmak istediğiniz için teşekkürler!

## İçindekiler
- [Geliştirme Ortamı Kurulumu](#kurulum)
- [Kod Standartları](#standartlar)
- [Commit Mesajları](#commit)
- [PR Süreci](#pr)
- [Test Yazma](#test)
- [Skill Ekleme](#skill)

## Kurulum
```bash
# Gereksinimler: MicroK8s 1.28+, Python 3.11+, Docker 24+
git clone https://github.com/sentinel/sentinel-coming
cd sentinel-coming
make dev-setup
```

## Kod Standartları
### Python (target servisler)
- Black formatlama: `black services/`
- Ruff lint: `ruff check services/`
- Type hints zorunlu: `mypy services/`
- Docstring: Google style

### YAML/Helm
- yamllint: `yamllint helm/`
- Helm lint: `helm lint helm/sentinel-target`

## Commit Mesajları
[Conventional Commits](https://conventionalcommits.org) standardı zorunlu.
Bkz. `skills/ci-conventional-commits`

## PR Süreci
1. Feature branch: `git checkout -b feat/orders-idempotency`
2. Değişiklikler + testler
3. `make lint test` yeşil
4. PR açılır → CI otomatik çalışır
5. En az 1 reviewer onayı gerekli
6. `main` squash merge

## PR Checklist
- [ ] Testler eklendi/güncellendi
- [ ] CHANGELOG.md güncellendi (fix/feat ise)
- [ ] Yeni env var varsa `.env.example` güncellendi
- [ ] Breaking change varsa ADR açıldı
- [ ] Yeni skill eklendiyse `skills/_index.md` güncellendi

## Test Yazma
### Birim testleri
```bash
pytest services/orders/tests/ -v
```

### Entegrasyon testleri
```bash
make test-integration  # Docker Compose ile DB+Redis ayağa kaldırır
```

### Chaos testleri
```bash
make test-chaos  # Chaos profile ile senaryo çalıştırır
```
```

### 2. Yeni katkıcı için ilk adımlar
```markdown
## İlk Katkınız

"good first issue" etiketli issue'lara bakın.

Önerilen ilk katkı alanları:
- `documentations/` altına eksik runbook eklemek
- Mevcut bir target servise yeni endpoint eklemek
- Skill SKILL.md içeriğini geliştirmek
```

### 3. Skill katkısı özel kuralları
```markdown
## Yeni Skill Ekleme

1. `skills/docs-skill-index-maintenance` skill'ini oku
2. Önce mevcut skill'lerde kopya olmadığını doğrula
3. `skills/<kategori>-<isim>/SKILL.md` dosyası oluştur
4. Minimum 25 satır, özgün içerik
5. `skills/_index.md` güncelle
6. PR açarken: "yeni skill: <isim>" başlığıyla
```

### 4. Review beklentileri
```markdown
## Reviewer Kılavuzu
- 24 saat içinde ilk yorum
- "LGTM" tek başına yeterli değil — ne neden iyi?
- Blocking comment: kodu merge ettirmeden çözülmesi gerekir
- Non-blocking (nit): iyileştirme önerisi, merge'i bloklamaz
- Kişisel tercih değil, kodun doğruluğuna odaklan
```

### 5. Onboarding kontrol listesi
PR açmadan önce:
- [ ] `make dev-setup` hatasız tamamlandı
- [ ] `make test` tüm testler geçiyor
- [ ] IDE'de Black + Ruff extension kuruldu
- [ ] Conventional Commits commitlint hook aktif

## Common mistakes
1. Çok uzun CONTRIBUTING.md yazmak — "quickstart" bölümü 5 adımı geçmemeli.
2. "PR'larınızı açabilirsiniz" yazmak ama review SLA'sını belirtmemek.
3. Code style kurallarını yazmak ama otomasyonu (pre-commit hook) sağlamamak — kural otomatik uygulanmalı.
4. First-time contributors için özel bir yol haritası vermemek — "good first issue" işaretsiz repolar caydırıcı.

## References
- `skills/ci-conventional-commits`
- `skills/ci-pr-gate`
- `skills/docs-onboarding-checklist`

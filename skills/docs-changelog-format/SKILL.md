---
name: docs-changelog-format
description: "Sentinel monoreposu için CHANGELOG.md formatı standardı ve Conventional Commits entegrasyonu ile otomatik üretim"
---

## Purpose
Sentinel'de her servis ve altyapı bileşeni ayrı versiyona sahipken tutarlı bir CHANGELOG formatı, release notlarını otomatik üretmeyi ve kullanıcılara hangi sürümde neyin değiştiğini netçe göstermeyi sağlar. Keep-a-Changelog standardı ve Conventional Commits ile tam entegrasyon kurulur.

## Workflow

### 1. CHANGELOG.md yapısı (Keep a Changelog)
```markdown
# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]

### Added
- ...

### Changed
- ...

### Fixed
- ...

## [1.2.0] - 2024-01-15

### Added
- Distributed tracing support via OpenTelemetry (#142)
- Redis session cache for auth service (#138)

### Fixed
- Memory leak in orders service connection pool (#145)

[Unreleased]: https://github.com/sentinel/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/sentinel/compare/v1.1.0...v1.2.0
```

### 2. Conventional Commits commit mesaj formatı
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Geçerli tipler:
- `feat`: yeni özellik (MINOR bump)
- `fix`: hata düzeltme (PATCH bump)
- `perf`: performans iyileştirmesi (PATCH bump)
- `refactor`: davranış değiştirmeyen yeniden yazım
- `docs`: sadece dokümantasyon
- `test`: test ekleme/değiştirme
- `chore`: build sistemi, bağımlılık güncellemesi
- `ci`: CI/CD konfigürasyon değişikliği
- `BREAKING CHANGE`: footer'da belirtilirse MAJOR bump

Sentinel scope örnekleri: `orders`, `payments`, `gateway`, `cos`, `ci`

### 3. git-cliff ile otomatik CHANGELOG üretimi
```toml
# cliff.toml (repo root)
[changelog]
header = "# Changelog\n\n"
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }} ([{{ commit.id | truncate(length=7, end="") }}]({{ commit.id }}))
{% endfor %}
{% endfor %}
"""

[git]
conventional_commits = true
commit_parsers = [
  { message = "^feat", group = "Added" },
  { message = "^fix", group = "Fixed" },
  { message = "^perf", group = "Performance" },
  { message = "^refactor", group = "Changed" },
  { message = "^docs", skip = true },
  { message = "^chore", skip = true },
]
```

```bash
# Belirli tag aralığı için CHANGELOG üret
git-cliff v1.1.0..v1.2.0 --output CHANGELOG.md

# Unreleased değişiklikler
git-cliff --unreleased --prepend CHANGELOG.md
```

### 4. GitHub Actions entegrasyonu
```yaml
# .github/workflows/release.yml
- name: Update CHANGELOG
  run: |
    pip install git-cliff
    git-cliff --unreleased --prepend CHANGELOG.md
    git add CHANGELOG.md
    git commit -m "chore: update CHANGELOG for ${{ github.ref_name }}"
```

### 5. Monorepo'da servis bazlı CHANGELOG
```bash
# Her servis için ayrı CHANGELOG
git-cliff --include-path "services/orders/**" --output services/orders/CHANGELOG.md
git-cliff --include-path "services/payments/**" --output services/payments/CHANGELOG.md
```

## Common mistakes
1. `[Unreleased]` bölümünü boş bırakmak — release sırasında neyin değiştiği belirsiz kalır.
2. Commit mesajlarında scope'u tutarsız kullanmak — `feat(Orders)` ve `feat(orders)` farklı scope sayılır.
3. Breaking change'i sadece commit body'sine yazmak — `BREAKING CHANGE:` footer'da olmalı, araçlar bunu okur.
4. CHANGELOG'u sadece major sürümlerde güncellemek — her patch için bile `Fixed` bölümü doldurulmalı.

## References
- `skills/ci-semantic-versioning`
- `skills/ci-conventional-commits`
- `skills/docs-adr-workflow`

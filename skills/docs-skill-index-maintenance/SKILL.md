---
name: docs-skill-index-maintenance
description: "Sentinel skill index'ini güncel tutar; yeni skill ekleme, kategori düzenleme ve kullanım rehberini yönetir"
---

## Purpose
Sentinel monoreposunda 600'ü aşkın skill birikiyor. Bu skill'leri keşfedilebilir kılmak, kopyaları önlemek ve kategorik tutarlılığı korumak için merkezi bir index ve bakım süreci gereklidir. Bu skill, yeni skill ekleme ritüelini ve mevcut index'in sağlığını koruma yolunu tanımlar.

## Workflow

### 1. Skills dizin yapısı
```
sentinel-coming/
└── skills/
    ├── _index.md              ← Tüm skill'lerin ana listesi
    ├── _categories.md         ← Kategori tanımları
    ├── debug-*/               ← Hata ayıklama skill'leri
    ├── docs-*/                ← Dokümantasyon skill'leri
    ├── platform-*/            ← Platform mühendisliği skill'leri
    ├── target-app-*/          ← Test uygulama skill'leri
    ├── ci-*/                  ← CI/CD skill'leri
    ├── cos-*/                 ← COS altyapı skill'leri
    ├── obs-*/                 ← Observability skill'leri
    └── agentic-*/             ← Otomasyon/MCP skill'leri
```

### 2. Yeni skill oluşturma kontrol listesi
```bash
# 1. Mevcut skill'leri kontrol et — kopya var mı?
ls skills/ | grep -i "feature-flag"

# 2. Kategori belirleme
# debug- : hata tespiti ve root cause analizi
# docs-  : dokümantasyon üretimi ve bakımı
# platform- : platform mühendisliği süreçleri
# target-app- : test FastAPI servisleri için
# ci-    : GitHub Actions pipeline
# cos-   : COS charm ve altyapı
# obs-   : Prometheus/Loki/Tempo/Grafana

# 3. Dizin ve dosya oluştur
mkdir -p skills/platform-feature-flags
cat > skills/platform-feature-flags/SKILL.md << 'TEMPLATE'
---
name: platform-feature-flags
description: "..."
---
TEMPLATE

# 4. Index'e ekle
echo "| platform-feature-flags | Feature flag yönetimi | platform- |" >> skills/_index.md
```

### 3. Index sağlık kontrolü
```bash
# SKILL.md eksik dizinleri bul
for d in skills/*/; do
  [ ! -f "$d/SKILL.md" ] && echo "MISSING: $d"
done

# description alanı boş olan skill'leri bul
grep -l 'description: ""' skills/*/SKILL.md

# 25 satırdan kısa skill'leri bul (kalite kontrolü)
for f in skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  [ "$lines" -lt 25 ] && echo "SHORT ($lines lines): $f"
done
```

### 4. Kategori sayım raporu
```bash
echo "Kategori Dağılımı:"
for prefix in debug docs platform target-app ci cos obs agentic; do
  count=$(ls -d skills/${prefix}-*/ 2>/dev/null | wc -l)
  echo "  ${prefix}-*: $count skill"
done
echo "  Toplam: $(ls -d skills/*/ | wc -l)"
```

### 5. Skill referans bütünlüğü kontrolü
```bash
# Var olmayan skill'lere referans veren skill'leri bul
for f in skills/*/SKILL.md; do
  while IFS= read -r line; do
    if [[ "$line" =~ skills/([a-z-]+) ]]; then
      ref="${BASH_REMATCH[1]}"
      [ ! -d "skills/$ref" ] && echo "BROKEN REF in $f: skills/$ref"
    fi
  done < "$f"
done
```

### 6. CI entegrasyonu
```yaml
# .github/workflows/skills-lint.yml
- name: Validate skill index
  run: |
    python scripts/validate_skills.py
    # Kontroller: min satır sayısı, description dolu, SKILL.md var
```

## Common mistakes
1. Yeni skill eklerken mevcut skill'leri taramadan kopya oluşturmak — `grep -ri "feature flag" skills/` ile önce kontrol et.
2. Index'i güncellemeden skill dizini açmak — keşfedilemez kalır.
3. `_index.md` yerine her kategori için ayrı index tutmak — çapraz kategori araması zorlaşır.
4. Skill adını değiştirip eski adı tutan dizini silmemek — broken reference birikmesi.

## References
- `skills/skill-creator`
- `skills/docs-contributing-guide`

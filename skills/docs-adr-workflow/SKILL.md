---
name: docs-adr-workflow
description: "Architecture Decision Record (ADR) yazma, takip etme ve Sentinel monorepo dokümantasyon yapısına entegre etme iş akışı"
---

## Purpose
Sentinel projesinde alınan mimari kararlar — COS bileşen seçimi, servis iletişim pattern'ı, veri saklama stratejisi — zaman içinde gerekçesi unutulur. ADR'lar bu kararları bağlamı, alternatifleri ve trade-off'larıyla birlikte kalıcı hale getirir ve yeni katılımcıların "neden böyle?" sorusuna hızla yanıt bulmasını sağlar.

## Workflow

### 1. ADR dizin yapısı
```
sentinel-coming/
└── documentations/
    └── adr/
        ├── README.md          ← ADR index
        ├── 0001-cos-over-custom-stack.md
        ├── 0002-fastapi-for-target-services.md
        ├── 0003-otel-w3c-propagation.md
        └── template.md
```

### 2. Yeni ADR oluştur
```bash
# Sonraki numarayı al
NEXT=$(ls documentations/adr/*.md | grep -E '[0-9]{4}-' | wc -l)
NUM=$(printf "%04d" $((NEXT + 1)))
SLUG="microk8s-storage-backend"
touch "documentations/adr/${NUM}-${SLUG}.md"
```

### 3. ADR şablonu
```markdown
# ADR-{NUM}: {Başlık}

**Durum**: Önerildi | Kabul Edildi | Reddedildi | Kullanım Dışı | Değiştirildi

**Tarih**: YYYY-MM-DD

**Karar Verici(ler)**: @kullanici1, @kullanici2

## Bağlam
[Hangi problemi çözüyor? Neden karar almak gerekti?]

## Karar
[Tam olarak ne yapılmasına karar verildi?]

## Gerekçe
[Neden bu seçenek? Kriterleri neler?]

## Değerlendirilen Alternatifler
| Seçenek | Artı | Eksi |
|---------|------|------|
| A | ... | ... |
| B | ... | ... |

## Sonuçlar
### Olumlu
- ...

### Olumsuz
- ...

## İlgili ADR'lar
- [ADR-0001](./0001-...)
```

### 4. ADR index'ini güncelle
```bash
# documentations/adr/README.md otomatik güncelle
cat > documentations/adr/README.md << 'EOF'
# Architecture Decision Records

| # | Başlık | Durum | Tarih |
|---|--------|-------|-------|
$(for f in documentations/adr/[0-9]*.md; do
  num=$(basename $f | cut -d- -f1)
  title=$(grep "^# ADR" $f | sed 's/# ADR-[0-9]*: //')
  status=$(grep "^\*\*Durum\*\*" $f | sed 's/.*: //')
  date=$(grep "^\*\*Tarih\*\*" $f | sed 's/.*: //')
  echo "| $num | $title | $status | $date |"
done)
EOF
```

### 5. ADR review süreci
1. PR açılır, ADR taslak olarak commit edilir (durum: "Önerildi")
2. İlgili mühendisler yorum yapar, alternatifler tartışılır
3. Karar verilince durum "Kabul Edildi" olarak güncellenir
4. Eski kararı değiştiren ADR: eski ADR'a "Değiştirildi → ADR-XXXX" notu düşülür

### 6. Sentinel-özgü ADR kriterleri
- COS bileşen seçimleri: mutlaka juju charm availability ve support lifecycle belirt
- MicroK8s storage backend kararları: addon maturity ve snapshot support değerlendir
- Observability pipeline kararları: cardinality impact ve Sentinel anomaly detection etkisini analiz et

## Common mistakes
1. ADR'ı karardan aylar sonra yazmak — bağlam ve alternatifler unutulmuş olur.
2. "Durum" alanını hiç güncellemememek — kullanım dışı kararlar yeni gelenleri yanıltır.
3. Teknik detaya gömülüp "neden" sorusunu atlamamak — ADR bir implementation doc değil, karar gerekçesidir.
4. ADR olmadan büyük refactor PR'ı açmak — reviewer bağlamı olmadan inceleyemez.

## References
- `skills/docs-changelog-format`
- `skills/docs-contributing-guide`

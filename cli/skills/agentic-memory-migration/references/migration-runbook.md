## Bellek Migration Runbook (Sentinel)

Bu doküman `agentic-memory-migration` skill’i için migration akışını “dry-run raporu + checkpoint + doğrulama + yeniden çalıştırılabilirlik” prensibine bağlar.

### Migration’in giriş şartları

Migration ancak şu koşullarda çalıştırılmalı:

- `memory schema_version` mevcut kodla uyumsuz.
- Migration, memory extract/dream çıktılarının saklandığı kök üzerinde yapılacak.
- `allow_non_interactive=false` ve write jail gibi güvenlik kısıtları değerlendirilmiş.

### Adım 0: kapsam belirle

- Kaynak kök: `policy: project` veya `policy: user` altında hangi klasör hedefleniyor.
- Hedef kök: aynı kök mü, farklı klasöre “staging” yapılacak mı?
- Hangi dosya tipleri etkileniyor:
  - `extract.jsonl`
  - index dosyası
  - dream index / magic docs girdileri

### Adım 1: Dry-run raporu üret

Dry-run raporu şu bilgileri içermeli:

- etkilenen dosya listesi
- kaç kayıt dönüştürülecek (yaklaşık veya kesin)
- beklenen yeni şema alanları
- migration başarısız olursa ne olur? (rollback / fallback)

Bu rapor:
- secret maskesi uygulanmış şekilde üretilmeli
- loglarda ham içerik göstermemeli

### Adım 2: Checkpoint ve idempotency

İki kritik özellik hedeflenir:

1. Yarıda kalırsa migration “nerede kaldım” bilgisinden devam edebilme.
2. Aynı migration tekrar çalıştırıldığında double-write üretmeme.

Pratik yöntem:
- Dönüşüm batch’lerini transaction benzeri “chunk id” ile işaretle.
- Index rebuild’de “overwrite veya rebuild_from_extract” stratejisini sabitle.

### Adım 3: Dönüşüm uygulama

Uygulama sırasında:
- redaksiyon filtresi pipeline’ın her yazma adımında etkin olmalı
- write jail kuralları bypass edilmemeli
- büyük veri için batch boyutu maliyeti kontrol etmeli

### Adım 4: Doğrulama

Doğrulama checklist’i:

- index kayıtlarının `schema_version` alanı doğru mu?
- zorunlu alanlar parse ediliyor mu (topic/last_seen/confidence/source_refs)?
- secret regexleri ile herhangi bir sızıntı var mı?
- “okuma simülasyonu” ile bellek arama akışı çalışıyor mu? (en az bir query)

### Adım 5: Rapor & devam planı

Migration sonunda rapor:
- dönüştürülen kayıt sayısı
- atlanan kayıt sayısı ve gerekçeleri
- disk kullanım delta (yaklaşık)
- tekrar çalıştırma süresi tahmini
vermelidir.

### Kabul kriterleri

- Dry-run tamamlanmadan yazma yapılmamalı (varsayılan).
- Migration başarısız olsa bile tekrar çalıştırılabilir olmalı.
- Secret içeriği kalıcı dosyalara yazılmamalı.


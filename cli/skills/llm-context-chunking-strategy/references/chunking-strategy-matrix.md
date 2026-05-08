## Chunking Strategy Matrisi (Sentinel)

Bu doküman `llm-context-chunking-strategy` skill’i için chunk boyutu, sınır kuralları, overlap oranı ve stabil doc/chunk id üretimini karar standardına bağlar.

### Hedefler

- Recall’ı artırmak (doğru bilgi kırpılmasın).
- Maliyeti kontrol etmek (token bütçesi aşılmasın).
- Id stabilitesi sağlamak (RAG ölçümünde doc_id/chunk_id korunur).

### Stabil kimlik şeması

Chunk kimliklerini “metin değiştiğinde” tamamen rastgele yapmak RAG ölçümlerini bozar. Bu nedenle:

- `doc_id`: doküman düzeyi, doküman içeriğinin *stabil hash’i* (örn. normalized path + content hash veya git blob hash benzeri).
- `chunk_id`: `doc_id + chunk_index` (veya chunk sınırı belirtecinden türetilmiş).

### Doküman tipine göre önerilen chunk kuralları

1. **Kod dosyaları (.py/.ts/.yaml gibi)**
   - Sınır: fonksiyon, class, önemli heading veya top-level block.
   - Chunk boyutu: daha küçük (ör. “tek ekran” mantığı).
   - Overlap: düşük-orta (sinyal korunumu için).
   - Sonuç: araç çağrısı/parametre çıkarımı daha stabil olur.

2. **Markdown / ADR / Runbook**
   - Sınır: heading hiyerarşisi (H2/H3) ve madde grupları.
   - Chunk boyutu: orta.
   - Overlap: kısa (özellikle giriş açıklamalarında).
   - Sonuç: “hangi bölüm ne diyor” ayrımı kolaylaşır.

3. **Loglar**
   - Sınır: zaman penceresi + event delimiter (örn. boş satır veya JSON log satırı).
   - Chunk boyutu: çok büyük olmamalı; çünkü embedding/LLM token şişer.
   - Overlap: minimum; aksi halde aynı hatalar tekrar tekrar çekilir.
   - Sonuç: reranking ile tekil olay seçimi daha iyi olur.

4. **Uzun düz metin (book/chapter)**
   - Sınır: paragraf blokları + konu değişim noktaları.
   - Chunk boyutu: daha büyük, fakat “tek parçada mantık kırılması” olmasın.
   - Overlap: metin akışı sürekliliği için küçük bir pay.

### Overlap oranı rehberi (pratik)

- Amaç “aynı bilgiyi tekrar görmek” değil; sadece sınırda kalan cümlelerin tamamlanmasını sağlamak.
- Bu yüzden overlap’i şu şekilde düşün:
  - “Sınır cümlelerinin tamamlanması için gerekli kadar”
  - Token bütçesi daraldığında overlap azalt, tekrarları filtrele.

### Chunk üretiminde asla yapılmaması gerekenler

- Aynı chunk içinde hem “bağlam talimatı” hem de “kullanıcı talimatı” karıştırma.
- Enjeksiyon riski yüksek metin parçalarını aynı chunk’a yayarak risk artırma; mümkünse riskli segmenti ayrı etiketle.

### Kabul kriterleri

- Aynı dokümanın tekrar chunk’lanması deterministic (aynı sınırlar + aynı id).
- Doc/chunk id seti RAGAS faithfulness gibi metriklerde kullanılabilir durumda kalır.
- Ortalama chunk recall metriği, overlap azaltmaya rağmen bozulmadan izlenir.


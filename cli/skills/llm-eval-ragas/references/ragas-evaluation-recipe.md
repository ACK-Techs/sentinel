## RAGAS Değerlendirme Reçetesi (Sentinel)

Bu doküman `llm-eval-ragas` skill’inin RAG kalite değerlendirmesinde “hangi alanların korunacağı, hangi ölçümlerin yorumlanacağı ve bootstrap gibi stabilizasyon adımları”nı standartlaştırır.

### Neden `doc_id` korunmalı?

RAGAS benzeri değerlendirmeler bağlam kalitesini ölçer. `doc_id` kaybı yaşanırsa:
- Context_precision / recall türevleri anlamsızlaşır
- Faithfulness kontrolü kaynak doğrulaması yapamaz

Bu yüzden değerlendirme veri setinde:
- retrieval aday seti
- seçilen bağlamlar
- modelin cevabı
hepsiyle birlikte `doc_id` setleri saklanmalıdır.

### Veri seti inşası (minimum)

Her task case için şunları sakla:

1. `query`
2. `conversation_state` (varsa)
3. `retrieval_candidates`:
   - en az: `doc_id`, `text` (veya snippet), `source_meta`
4. `selected_context`:
   - retrieval sonunda LLM’e giden doküman seti (doc_id + snippet)
5. `model_answer`
6. (Opsiyonel) “ground truth”:
   - doğrulanabilir doğru cevap veya doğru davranış kontratı

### Metriği yorumlama kuralları

Tek bir metriğe göre karar alma. Bunun yerine:

- Bağlam alaka (context relevance) = retrieval ne kadar hedefledi?
- Bağlam kullanımı (context usage / faithfulness) = cevap bağlamdan mı geliyor?
- Yanıt alaka = cevap kullanıcının ihtiyacını karşılıyor mu?

Tipik hata desenleri:
- Context relevance yüksek, faithfulness düşük:
  - Model bağlamı “yanlış yorumlayıp” uyduruyor.
- Context relevance düşük, yanıt kalitesi yüksek:
  - Model bazen görev için yeterli genel bilgiyle doğru dönüyor; tekrar ölç.

### Bootstrap ile stabilizasyon

Küçük veri setlerinde RAGAS skorları varyanslı olabilir.

Standart yaklaşım:

1. case listesi üzerinde bootstrap örnekleri üret (ör. 1k tekrar).
2. skorların dağılımını raporla.
3. “ortalama fark var mı?”dan önce “hangi alt kümeler kırılıyor?” incele.

### Kabul kriterleri

- Skorlar yalnızca sayı değil; hangi `doc_id` setleri problem üretiyor görülebiliyor.
- Model cevaplarını değerlendirme raporunda bağlamdan bağımsız “tek başına” ölçmeye çalışmıyorsun.
- Aynı task seti ile baseline/candidate karşılaştırması mümkün.

### Sentinel pratik notu

RAGAS değerlendirme çıktısını `llm-eval-regression-test` golden protokolüyle aynı case id altında tut:
- Case id eşleşmesi hata kümelerini birleştirmenizi sağlar.


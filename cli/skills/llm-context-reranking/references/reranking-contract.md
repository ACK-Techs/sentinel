## Reranking Sözleşmesi (Sentinel)

Bu doküman `llm-context-reranking` skill’i için reranker’ın:
1) hangi input’u alacağını,
2) hangi output formatında geri döneceğini,
3) başarısızlık modunda nasıl degrade edeceğini
sabitlemek için kullanılır.

### Input sözleşmesi

Reranker girdisi üç parçaya ayrılmalıdır:

- `query`: kullanıcının hedefi (string)
- `candidate_documents`: retrieval aşamasından gelen aday seti (toplam N)
  - her aday için en az: `doc_id`, `snippet_text`, `source_meta`, `retrieval_score`
- `task_constraints`: output kalıbı ve güvenlik kısıtları (string/structure)

### Candidate formatı (zorunlu alanlar)

- `doc_id`: stabil id (RAG ölçümü için)
- `snippet_text`: snippet (tam metin değil; token kontrolü için)
- `retrieval_score`: retrieval aşamasından gelen score (opsiyonel ama önerilir)
- `security_label`: trusted/untrusted veya flagged/unflagged gibi

### Output sözleşmesi

Reranker sonucu:

- `ranked_docs`: sıralı liste
  - eleman: `doc_id`, `final_score`, `rationale_short`
- `selected_k`: seçilen top-K sayısı
- `dropped_docs`: atılanların kısa gerekçesi (örn. “security_label risk”, “duplicate content”)

### Faithfulness hazırlığı

Reranking yalnızca “alaka” için çalışır; “cevabın kesin doğru olması” garantisi değildir.

Bu nedenle seçim sırasında:
- `rationale_short` içinde “hangi kaynak parçası hedefi destekliyor” ifadesi olmalı.
- `doc_id` kaybolmamalı.

### Latency bütçesi

Reranker giriş adayları çok geniş olursa maliyet/latency patlar. Bu doküman kural koyar:

- `candidate_documents` en fazla N (ör. 20–80 aralığı) olmalı.
- Çok turlu görevlerde reranking’i sadece ilk turda uygula (opsiyonel policy).

### Hata ve degrade akışı

Reranker başarısız olursa:

1. `security_label` kırmızıysa seçimde bu dokümanlar otomatik düşürülür.
2. Reranker hatası varsa retrieval ranking (orijinal retrieval_score) ile devam edilir.
3. `rerank_failed=true` metriği loglanır.

### Kabul kriterleri

- Reranking output’u parse edilebilir ve `doc_id` tamamen korunur.
- Aynı query+aynı aday seti için “şartlı determinism” sağlanır:
  - aday seti sabitse sıralama stabil olmalı,
  - sadece model nondeterminism çok düşük dalgalanma gösterebilir.


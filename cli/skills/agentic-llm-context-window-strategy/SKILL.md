---
name: agentic-llm-context-window-strategy
description: Token limiti yaklaştığında kesme, özet veya uyarı politikası ile system, tools ve history önceliğini belirlerken kullan.
---

## Amaç

**Öncelik sırası** (öneri): sistem talimatları ve güvenlik kuralları > tool şemaları (kısaltılmış özet mümkünse) > son kullanıcı mesajları > ara geçmiş. **Tahmini token sayımı**: heuristik (karakter/ kelime) veya sağlayıcı `usage` alanı — proje kararı. Kullanıcıya **“bağlam dolu”** anlaşılır mesajı; maliyet/latency notu (özet LLM çağrısı pahalı olabilir).

## Kapsam

### Dahil

- Context dolmadan önce uyarı eşiği (% örn. 85).
- Uzun araç çıktılarının kırpılması (`agentic-tools-base-contract` ile uyum).

### Hariç

- Fine-tuning veya embedding tabanlı RAG (bu katalogda yoksa ekleme).

## Kurallar

- İlk kullanıcı isteği ve kritik kısıtlar mümkünse korunur.
- Özet kalitesi düşükse kullanıcıyı uyar (`agentic-agent-history-compaction`).
- Lokal küçük modellerde agresif kırpma gerekebilir.

## Kontrol listesi

- [ ] `usage` bilgisi yoksa heuristik belgelenmiş mi?
- [ ] Tool çıktısı devasa olduğunda önce kırpma mı özet mi?
- [ ] Çoklu sağlayıcıda limit farkı tablosu var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| 400 context length | Son mesajlar | History compaction |
| Özet döngüsü pahalı | Eşik | Daha ucuz özet modeli (proje kararı) |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-agent-history-compaction/SKILL.md`
- `../agentic-llm-openai-compatible-local/SKILL.md`
- `../agentic-tools-base-contract/SKILL.md`

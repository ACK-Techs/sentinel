---
name: llm-context-dynamic-injection
description: Bağlam inşası, geri çağırma ve enjeksiyon kararları alınırken; token bütçesi, retrieval doğruluğu ve çok turlu oturum kalitesi dengelenmek istendiğinde kullan.
---

## Problem çerçevesi
`llm-context-dynamic-injection` başlığı, "model ne biliyor" sorusundan çok "modelin doğru anda doğru bağlamı görmesi" sorununu çözer. Yanlış bağlam yönetimi, iyi promptu bile etkisiz hale getirir.

## Karar akışı
1. **Bağlam kaynaklarını sınıflandır:** sistem talimatı, konuşma geçmişi, retrieval çıktısı, canlı tool çıktısı.
2. **Öncelik ver:** güvenlik ve görev açısından kritik içerikleri sabit önekte tut.
3. **Sıkıştırma / seçim uygula:** gerektiğinde özetleme, chunk eleme, rerank veya cache stratejisi uygula.
4. **Enjeksiyon noktasını belirle:** retrieval çıktısını kullanıcı mesajına yapıştırma; ayrı yapılandırılmış blokta ver.
5. **Gözlemlenebilir yap:** cache hit, retrieval recall ve token tüketimini oturum bazında kaydet.

## Sentinel’de uygulanacak ölçümler
- Tur başına kullanılan toplam token ve trimming oranı.
- Retrieval kaynağı başına başarı (yararlı chunk oranı).
- Uzun oturumda kullanıcı düzeltme sayısı (bağlam kaybı göstergesi).

## Uyarılar
- Sadece daha büyük context window kullanmak sorunu tek başına çözmez.
- History compaction kalitesi düşerse agent yanlış özgüvenle cevap verir.
- Hybrid search kullanırken keyword sinyalini tamamen kapatma.

## Referanslar
- `cli/skills/agentic-llm-context-window-strategy/SKILL.md`
- `cli/skills/agentic-agent-history-compaction/SKILL.md`
- `documantations/INTEGRATION_SENTINEL_CLI_FROM_CLI_CLAUDE.md`
- `cli/documantations/ARCHITECTURE_AGENTIC_CLI.md`

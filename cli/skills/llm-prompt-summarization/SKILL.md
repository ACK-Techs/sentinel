---
name: llm-prompt-summarization
description: Prompt tasarımıyla model davranışı güvenilir ve ölçülebilir hale getirilmek istendiğinde; Sentinel ajan döngüsüne uygun istemler, güvenlik sınırları ve çıktı kalitesi optimize edilirken kullan.
---

## Tasarım niyeti
`llm-prompt-summarization` için hedef; promptu "metin yazımı" olarak değil, ajan davranış sözleşmesi olarak ele almaktır. Prompt; araç çağrısı sınırlarını, cevap formatını ve başarısızlık durumunda geri dönüş stratejisini açıkça taşımalıdır.

## Uygulama deseni
- **Görev çekirdeği:** tek cümlede iş hedefi, başarı ölçütü ve yasaklı davranışlar.
- **Bağlam katmanı:** yalnızca gerekli domain bilgisi; gereksiz örneklerle context şişirmeme.
- **Yürütme katmanı:** modelden hangi sıra ile düşünmesini/eylem almasını beklediğini açık yaz.
- **Çıktı katmanı:** JSON/Markdown/serbest metin kararıyla parse edilebilir sonuç üret.
- **Emniyet katmanı:** prompt injection, role confusion ve tool overreach için koruyucu cümleler.

## Sentinel entegrasyonu
- `agentic-agent-turn-loop` akışında prompt varyantlarını A/B etiketleriyle dene.
- `agentic-agent-tool-call-parse` ile uyumlu şema dili kullan.
- `agentic-prompt-injection-guardrails` prensipleriyle güvenilmeyen içeriği ayrı kanal olarak işle.

## Kalite kontrol
- Aynı girdiye sıcaklık değişse bile format bozulmuyor mu?
- Tool açıklamaları modelin doğru aracı seçmesini artırıyor mu?
- Uzun konuşmada ilk tur hedefi kayboluyor mu?

## Skill-spesifik kararlar
- Ozetlemede audience tanimi (yonetici, operator, gelistirici) sonucu ciddi degistirir; hedef kitleyi promptta belirt. Uzun belgede map-reduce ara ozetlerini sakla.

## Referanslar
- `cli/documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `cli/documantations/archive/PROMPT_INJECTION_GUARDRAILS_PHASE2A.md`
- `cli/skills/agentic-prompt-injection-guardrails/SKILL.md`
- `cli/skills/agentic-agent-tool-call-parse/SKILL.md`

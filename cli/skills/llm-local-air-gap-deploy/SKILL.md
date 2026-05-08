---
name: llm-local-air-gap-deploy
description: Yerel model işletimi, profil seçimi ve Sentinel CLI entegrasyonu yapılırken; donanım sınırları, model davranışı ve operasyon akışı netleştirilmek istendiğinde kullan.
---

## Operasyon odağı
Bu skill, `llm-local-air-gap-deploy` başlığında yerel LLM çalıştırmayı "kurulum + çalışma zamanı + arıza kurtarma" üçlüsüyle ele alır. Amaç yalnızca modeli ayağa kaldırmak değil; Sentinel CLI profillerinde (`local`, `openai-compatible`, `anthropic`) davranış farklarını yönetilebilir hale getirmektir.

## Uygulama akışı
1. **Çalışma profilini netleştir:** tek kullanıcı masaüstü, ekip içi LAN sunucusu veya tam air-gap ortamından hangisi hedefleniyor belirle.
2. **Model-operasyon eşleşmesini yap:** beklenen latency, bağlam uzunluğu ve VRAM sınırına göre modeli ve quantization seviyesini seç.
3. **Sentinel profile bağla:** `cli/config/sentinel.yaml` ve ortam değişkenleriyle model endpoint, timeout ve retry ayarlarını ayrı profile taşı.
4. **Smoke + failure testleri çalıştır:** kısa prompt, uzun prompt ve araç çağrısı benzeri girdilerle çökme, truncation veya timeout davranışını kaydet.
5. **Runbook üret:** model güncelleme, cache temizleme, fallback profile geçiş adımlarını operasyon dokümanına yaz.

## Pratik kontroller
- `doctor` çıktısında seçili model, base URL ve timeout değerleri görünmeli.
- Bağlam limitine yaklaşırken mesajların kesilme davranışı deterministic olmalı.
- Yerel model down olduğunda profile fallback ya da kullanıcıya açık hata mesajı üretilmeli.

## Bu konuda sık hatalar
- Tek makinede iyi çalışan ayarı ekip ortamına aynen taşımak.
- Modelin "token/s" hızını ölçmeden üretim benzeri kullanıma geçmek.
- Güvenlik sınırı olmadan LAN endpoint’i açık bırakmak.

## Skill-spesifik kararlar
- Air-gap kurulumda model artefaktini checksum ile tasit, offline wheel/dependency mirror hazirla ve ilk acilista internet cagrisini fail-fast test et. Lisans dosyalarini paketlemeden dagitim yapma.

## Referanslar
- `cli/documantations/LLM_PROVIDERS.md`
- `cli/documantations/IMPLEMENTATION_PLAN_PHASE2.md`
- `cli/skills/agentic-llm-openai-compatible-local/SKILL.md`
- `cli/skills/agentic-config-profiles/SKILL.md`

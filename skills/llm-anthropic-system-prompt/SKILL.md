---
name: llm-anthropic-system-prompt
description: "Anthropic API için etkili sistem promptu tasarlamak; persona, görev çerçevesi, davranış kısıtlamaları ve çıktı formatı bölümlerini yapılandırmak gerektiğinde kullan."
---

## Purpose
Sistem promptu, modelin davranışını çerçeveler. Zayıf sistem promptu = tutarsız yanıtlar, aşırı genel çıktı, güvenlik riski. İyi tasarım kalıcı token maliyetidir; her istek gönderilir.

## Sistem promptu bölümleri

### Temel yapı
```
# Rol ve Persona
[Kim olduğu, uzman alana, tonuna]

# Görev
[Ne yapacağı, hangi sorulara yanıt vereceği]

# Kısıtlamalar
[Yapmaması gerekenler, kapsam dışı konular]

# Çıktı Formatı
[JSON/markdown/düz metin, uzunluk kısıtı]

# Örnekler (opsiyonel, few-shot)
[İstenen davranışı gösteren Q/A çiftleri]
```

### Sentinel için örnek
```
Sen Sentinel observability platformunun yardımcı asistanısın. Prometheus, Loki, Grafana ve Kubernetes konularında uzmanlaşmışsın.

Yalnızca şu konularda yardım et:
- PromQL sorgusu yazma ve açıklama
- Kubernetes pod/deployment sorunlarını teşhis etme
- Grafana dashboard tasarımı
- Alert kuralı yazma

Yanıtlarında:
- Kod örneklerini markdown code block içinde yaz
- Komutlarda kullanıcının platform ortamını (MicroK8s/COS Lite) varsay
- Konfigürasyon içeren yanıtlarda geçerli değerleri açıkla
```

## Uzunluk ve maliyet
- Sistem promptu her istekte gönderilir → prompt caching ile maliyet düşürülür.
- 1000 token altında tutmak genellikle yeterlidir; çok uzun sistem promptu model üzerinde azalan getiri yaratır.

## Common mistakes
- Hem kullanıcı hem sistem promptuna aynı kuralı yazmak — tekrar.
- Negatif kısıtlamalar yerine pozitif yönlendirme yazmak: "sadece X yap" > "Y yapma".
- Sistem promptunu her istek için değiştirmek — prompt caching kırılır.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-prompt-caching`
- `skills/llm-prompt-system-design`

---
name: obs-grafana-variables
description: Grafana dashboard’larda template variables tasarlamak (query/custom/interval/datasource), doğru multi-select/regex davranışı kurmak veya “değişken yüzünden panel boş/yavaş” sorununu çözmek gerektiğinde kullan. Değişkenlerin performans ve UX etkisine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- İhtiyaca uygun variable set’i (örn. `service`, `namespace`, `env`, `interval`)
- Multi-select + “All” seçeneği için güvenli query kalıbı (yanlış regex patlamasını önler)
- Anti-pattern listesi: cascading variable, pahalı query, aşırı kartesian çarpım

## Workflow
- Variable ihtiyacını sor:
  - Kullanıcı hangi kırılımlarla gezmek istiyor? (service/env/region)
  - Drilldown mı, yoksa sadece filtre mi?
- Tür seçimi:
  - Query variable: datasource’dan dinamik liste
  - Custom variable: küçük sabit set (prod/staging)
  - Interval variable: panel step/interval kontrolü
  - Datasource variable: aynı dashboard’u farklı backend’lere bağlamak (dikkat: karmaşıklık)
- Performans:
  - Query variable’ı pahalı yapma (yüksek kardinalite label’ları listeleme).
  - Varsayılan değeri dar tut (All = pahalı ve riskli).
- Multi-select ve “All”:
  - Regex/escape davranışını test et; yanlış regex “her şeyi seçer” veya “hiçbir şey seçmez”.
  - Panel query’lerinde variable’ı doğru quote et.
- Doğrulama:
  - Değişkeni değiştirince paneller beklenen şekilde güncelleniyor mu?
  - En kötü senaryo: All + geniş zaman aralığında dashboard kendini öldürüyor mu?

## Anti-patterns
- 5+ değişkenin birbirini filtrelemesi (cascading): seçimler boşalır ve debug zorlaşır.
- `pod` gibi churn label’ını variable yapmak: liste sürekli değişir, cache bozulur.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`

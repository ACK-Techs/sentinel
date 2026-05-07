---
name: obs-alertmanager-routing
description: Alertmanager’da route ağacını (matchers, receiver seçimi, `continue`, grouping/repeat mirası) tasarlamak veya “alert yanlış ekibe gidiyor / iki kez gidiyor / hiç gitmiyor” problemini çözmek gerektiğinde kullan. Kural yazımı değil, **routing mantığı** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Route ağacı taslağı (root → team/service/severity dalları) ve karar gerekçesi
- Matcher sözlüğü önerisi (hangi label’lar routing için “kontrat”)
- Doğrulama: bir örnek alert’in hangi route’a düştüğünü kanıtlayan kontrol adımları

## Workflow
- Routing kontratını sabitle:
  - Alert’lerde hangi label’lar garanti? (örn. `team`, `service`, `severity`, `env`)
  - Eksikse: default route + fallback receiver.
- Ağaç tasarımı:
  - Root route: default receiver + global grouping/repeat.
  - Dallar: önce `env` (prod), sonra `severity`, sonra `team/service` gibi.
- `continue` kararı:
  - Aynı alert’in birden fazla receiver’a gitmesi isteniyorsa sadece o node’da `continue: true`.
  - Aksi halde varsayılan `false` ile “ilk eşleşen kazanır”.
- Miras (inheritance) kontrolü:
  - Child route, parent’ın grouping/repeat değerlerini miras alır; fark yaratıyorsan açık yaz.
- Doğrulama:
  - Bir test alert’i üret (label’ları routing kontratına uygun).
  - Alertmanager UI/API’de alert’in eşleştiği route/receiver’ı doğrula.

## Common mistakes
- Matcher’larda label adını yanlış yazmak veya label’ın hiç set edilmemesi.
- `continue: true`’yu “default” yapmak: beklenmedik çoklu bildirim.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`

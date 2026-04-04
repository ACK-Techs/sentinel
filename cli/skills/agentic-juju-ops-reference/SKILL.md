---
name: agentic-juju-ops-reference
description: COS model işletiminde Juju teşhis sırası, yetki uyarıları ve geri dönüş komutlarını özetlerken kullan.
---

## Amaç

Bu skill, COS Lite modelinde Juju taraflı işletim kontrollerini standartlaştırır. Amaç, model erişimi, application ve unit durumu, action ve relation görünürlüğü ile izin hatalarının güvenli şekilde ele alınmasını sağlamaktır.

## Kapsam

- Dahil:
- `juju status`, `juju status --relations`, `juju show-unit`, `juju debug-log` gibi temel teşhis komutları.
- Model yanlış seçildiğinde veya yetki yetersiz olduğunda operatöre geri dönüş vermek.
- Faz 1 Juju model ve deploy skill'lerine yönlendirme.
- Hariç:
- Yeni model tasarımı veya farklı controller topolojisi kararı.
- Faz 1 belgelerinde olmayan channel veya revision sabitlemesi.

## Adımlar

1. Önce şunu doğrula: kullanıcı doğru controller ve doğru modelde mi, beklenen model adı `cos` mu.
2. Temel görünürlük kontrolünü yap:
   - `juju models`
   - `juju status --model cos`
   - `juju status --model cos --relations`
3. Sorunlu uygulama veya unit varsa ayrıntı al:
   - `juju show-unit <unit> --model cos`
   - `juju show-application <application> --model cos`
   - `juju debug-log --model cos --replay --include <application>`
4. Action veya parola gerekiyorsa Faz 1 skill ile hizalı action kullan:
   - Örnek: Grafana için ilgili deploy skill'deki action.
5. Yetki hatası veya controller erişim sorunu varsa:
   - Giriş kimliğini ve controller seçimini doğrula.
   - `sudo` önermeden önce Juju erişim modelini doğrula; Juju komutları çoğu durumda kullanıcı bağlamında çalışır.
   - Yetki hatasını “yeniden bootstrap et” diye varsayma; önce model erişimini doğrula.

## Kontrol listesi

- [ ] Kullanıcı doğru modelde ve beklenen controller'da mı?
- [ ] Sorunlu application veya unit açıkça tespit edildi mi?
- [ ] Relation görünürlüğü `juju status --relations` ile doğrulandı mı?
- [ ] Gereken action veya endpoint Faz 1 skill ile çapraz kontrol edildi mi?
- [ ] Yetki hatasında gereksiz `sudo` önerilmedi mi?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| `model not found` | Aktif model ve controller | `juju models` ve `../../skills/juju-model-cos/SKILL.md` |
| Uygulama `blocked` veya `waiting` | Relation eksik mi, config eksik mi | İlgili deploy veya relation skill'e dön |
| `permission denied` veya login sorunu | Juju kimliği ve controller erişimi | Kullanıcıdan erişim bağlamını doğrulamasını iste |
| Relation görünmüyor | `juju status --relations` çıktısı | İlgili Faz 1 relation skill'e geç |
| Action sonucu başarısız | Leader unit ve action çıktısı | İlgili bileşen troubleshoot skill'i |

## İlgili belgeler ve skill'ler

- `../../documantations/PROJECT_ROOT.md`
- `../../documantations/ARCHITECTURE_COS.md`
- `../documantations/PROJECT_ROOT_PHASE2.md`
- `../../skills/juju-model-cos/SKILL.md`
- `../../skills/juju-snap-setup/SKILL.md`
- `../../skills/cos-deploy-grafana/SKILL.md`
- `../../skills/cos-deploy-prometheus/SKILL.md`
- `../../skills/cos-deploy-loki/SKILL.md`
- `../../skills/cos-deploy-alertmanager/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`

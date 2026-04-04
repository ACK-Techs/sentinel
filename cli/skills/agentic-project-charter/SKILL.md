---
name: agentic-project-charter
description: Faz 2 agentic CLI’nin misyonu, kapsam dışı sınırları ve başarı tanımını netleştirirken bu skill’i kullan.
---

## Amaç

Sentinel Faz 2’nin **terminal tabanlı danışman ajanı** rolünü, Faz 1 COS kurulumundan ayırarak standartlaştırır: ne yapılır (API + lokal LLM, araç destekli danışmanlık), ne yapılmaz (Faz 1’in yerine geçmek değil, canonical kurulumu skill/doküman dışına itmemek). Hedef persona: **SRE / platform** ve **uygulama geliştirici**; workspace `agentic/` yalnızca **referans desen** kaynağıdır, ürünün tek doğruluk kaynağı bu charter ve `cli/documantations/` belgeleridir.

## Kapsam

### Dahil

- Faz 2 misyonu: COS/MicroK8s/Juju yığınına **danışan**, arıza ve iyileştirmede **Faz 1 skill’leriyle uyumlu** öneriler.
- Çift motor: **uzak API** ve **lokal OpenAI-uyumlu** uç (`LLM_PROVIDERS.md` ile uyumlu env sözleşmesi).
- Başarı tanımı: yapılandırılabilir CLI, güvenlik/onay hatları, dokümante edilmiş skill ağı.

### Hariç

- Faz 1’de tanımlı charm sürüm/channel seçimini bu skill’de tek başına sabitlemek (Faz 1 `PROJECT_ROOT.md` ve ilgili skill’ler önceliklidir).
- `agentic/` altındaki üçüncü parti kodu ürün gibi garanti etmek (lisans/telif ayrı skill).

## Kurallar

- Eksik gereksinimde **sıfır varsayım**: kullanıcıya danış (`PROJECT_ROOT_PHASE2.md` protokolü).
- COS “nasıl kurulur” aksiyonlarını özetlerken Faz 1 `../../documantations/PROJECT_ROOT.md` ve `../../documantations/IMPLEMENTATION_PLAN.md` ile **çelişen** iddia verme.
- Referans repo `agentic/` yalnızca mimari örnek; uygulama kararları `IMPLEMENTATION_PLAN_PHASE2.md` ve kod ile sabitlenir.

## Kontrol listesi

- [ ] Faz 1 vs Faz 2 sorumluluk tablosu ekip içi paylaşımda anlaşıldı mı?
- [ ] “Sadece kod yazan ajan” ile “COS danışmanı” ayrımı charter’da net mi?
- [ ] API + lokal LLM hedefi README/plan ile uyumlu mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Kapsam şişmesi | `IMPLEMENTATION_PLAN_PHASE2.md` sprint sınırları | Charter’da “kapsam dışı” maddeleri güncelle |
| Faz 1 ile çakışan yönerge | `../../documantations/PROJECT_ROOT.md` | Faz 2 yanıtını Faz 1 skill’e yönlendir |

## İlgili belgeler ve skill'ler

- `../documantations/PROJECT_ROOT_PHASE2.md`
- `../documantations/IMPLEMENTATION_PLAN_PHASE2.md`
- `../../documantations/PROJECT_ROOT.md`
- `../agentic-repo-layout/SKILL.md`
- `../agentic-cos-advisor-overview/SKILL.md`

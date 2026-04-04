# Sentinel — Faz 2: Agentic CLI (Proje Özeti)

Aşağıdaki **Yapay Zeka Otonomi ve Hata Yönetim Protokolü**, Faz 2 dokümantasyonu ve `cli/skills/agentic-*` skill’leri için de bağlayıcıdır; üst dizindeki `documantations/PROJECT_ROOT.md` (Faz 1 — COS kurulumu) ile birlikte okunmalıdır.

1. **Sıfır Varsayım Kuralı:** Eksik bilgi veya belirsiz seçenekte kodlayıcı AI **kendi başına karar vermez**, **durur** ve kullanıcıya danışır.

2. **Maksimum 2 Deneme (Fail-Safe):** Komut hatasında en fazla **bir veya iki** düzeltme denemesi.

3. **Derin Analiz ve Bekleme (Stop & Think):** İki denemeden sonra hata sürüyorsa **yeni komut/kod denenmez**; kök neden analizi yapılır ve **kullanıcı onayı beklenir**.

---

## Faz 1 ve Faz 2 ilişkisi

| Faz | Amaç | Ana çıktı |
|-----|------|-----------|
| **Faz 1** | Canonical COS Lite’ı MicroK8s + Juju ile kurmak | `../documantations/` + `../skills/*` (COS/MicroK8s/Juju) |
| **Faz 2** | Bu yığına **danışan**, **iyileştirme öneren** ve **arıza durumunda çözüm öneren** bir **terminal (CLI) ajanı** | `cli/` paketi; model **API** veya **lokal inference** |

Faz 2 uygulaması bu belge ve aynı klasördeki `SKILL_CATALOG_PHASE2.md` ile yönetilir.

## Referans kod tabanları (`agentic/`) — yardımcı kaynak

Workspace kökünde **`agentic/`** altında üç ayrı proje, Faz 2 CLI için **yardımcı tasarım ve kaynak referansı** olarak kullanılır. Bunlar Sentinel ürününün parçası değildir; **doğrudan vendor edilmez**, ihtiyaç halinde desen, API şekli veya davranış **uyarlanarak** `sentinel-coming/cli/` içine taşınır.

| Dizin | Rol |
|-------|-----|
| `agentic/Pywen-dev/` | Python tabanlı ajan, araçlar, LLM adapter, hook, config — **birincil teknik hizalama** (hedef dil Python ise). |
| `agentic/codex-main/` | TypeScript / SDK ve araç tarafı — stream, MCP, üretim kalıpları için **desen kaynağı**. |
| `agentic/claude/` | TypeScript — CLI komut yüzeyi, izinler, oturum/MCP UX için **desen kaynağı**. |

**Kurallar:** Telif ve lisans farkındalığı `agentic-dependency-licensing` ve `agentic-reference-agentic-folder` skill şartnameleri ile uyumlu tutulur; kopyalanan veya uyarlanan parçalar dokümante edilir. Belirsiz seçeneklerde **Sıfır Varsayım Kuralı** geçerlidir (kullanıcıya sor, tek başına genişletme).

## Vizyon (Faz 2)

- **Çift motor:** **Bulut API anahtarı** (OpenAI uyumlu, Anthropic, vb.) veya **yerel sunucu** (Ollama, LM Studio, vLLM, OpenAI-uyumlu `base_url`).
- **Araç destekli danışmanlık:** Güvenlik sınırları içinde komut önerisi, dosya/çıktı okuma; isteğe bağlı **MCP**.
- **Faz 1 köprüsü:** COS/MicroK8s/Juju sorularında `../documantations/` ve `../skills/*` (Faz 1) ile **tutarlı** kalınır.

## Kapsam (yüksek seviye)

- CLI (bu klasörün üstü `cli/`): yapılandırma birleştirme, oturum, REPL veya tek komut modu.
- LLM: sağlayıcı soyutlaması, streaming, hata ve yeniden deneme politikası.
- Güvenlik: onay politikası, sırlar, prompt enjeksiyonuna karşı dikkat.
- Gözlemlenebilirlik danışmanlığı: Faz 1 skill’leri ve resmi Ubuntu Observability dokümantasyonu ile hizalı playbook’lar.

## Okuma sırası

**Bu dosyayı `cli/documantations/` içinden okuyorsanız** göreli yollar:

1. `../../documantations/PROJECT_ROOT.md` — Faz 1 bağlamı  
2. `PROJECT_ROOT_PHASE2.md` — bu dosya  
3. `ARCHITECTURE_AGENTIC_CLI.md`  
4. `REPO_LAYOUT_RECOMMENDED.md` — **önerilen** `cli/` dizin ağacı (kodlamadan önce okunmalı)  
5. `LLM_PROVIDERS.md`  
6. `IMPLEMENTATION_PLAN_PHASE2.md`  
7. `SKILL_CATALOG_PHASE2.md` — **58** Faz 2 skill şartnamesi  
8. `../skills/agentic-*` — Faz 2 skill gövdeleri

**Depo köküne göre tam yol** (`sentinel-coming/`): `documantations/PROJECT_ROOT.md` (Faz 1); Faz 2 için `cli/documantations/*` ve `cli/skills/agentic-*`.

## Dış referanslar

- [Ubuntu Observability](https://documentation.ubuntu.com/observability/)
- Workspace `agentic/`: Pywen-dev, codex-main, claude — **yardımcı kaynak** (ayrıntı yukarıdaki bölüm)

# Mimari: Agentic CLI (Faz 2)

Bu belge, **Sentinel Faz 2** terminal ajanının mantıksal katmanlarını özetler. Uygulama dili ve çerçeve `IMPLEMENTATION_PLAN_PHASE2.md` ile sabitlenir; buradaki diyagram **davranış sözleşmesidir**.

## Referans implementasyonlar (yardımcı kaynak)

Aşağıdaki katmanların gerçek dünyada nasıl kurgulandığına dair **yardımcı kaynak**, workspace `agentic/` altındaki üç dizindedir (`Pywen-dev`, `codex-main`, `claude`). Sentinel CLI bu kodları **alt modül olarak bağlamaz**; mimari burada tanımlı kalır, uygulama ise `sentinel-coming/cli/` içinde üretilir ve gerektiğinde referanslardan **uyarlama** yapılır. Ayrıntılı kurallar ve lisans farkındalığı: `PROJECT_ROOT_PHASE2.md` («Referans kod tabanları») ve `SKILL_CATALOG_PHASE2.md` içindeki `agentic-reference-agentic-folder`.

## Katman özeti

```mermaid
flowchart TB
  subgraph User["Kullanıcı"]
    T[Terminal]
  end

  subgraph CLI["CLI"]
    EP[entrypoint / argparse veya eşdeğeri]
    CFG[config merge: defaults, file, env, flags]
    PROF[profil: cloud | local | custom]
  end

  subgraph LLM["LLM katmanı"]
    REG[Provider registry]
    REM[Remote API providers]
    LOC[Local OpenAI-compatible HTTP]
    STR[Streaming normalizasyonu]
  end

  subgraph Agent["Ajan"]
    LOOP[turn loop: max_turns, stop conditions]
    HIST[message history + optional compaction]
    PARSE[tool call parse / validate]
  end

  subgraph Tools["Araçlar"]
    TR[Tool registry]
    BASH[bash / shell]
    FS[filesystem read/write]
    MCP[MCP client]
    HOOK[hooks: PreToolUse / PostToolUse]
    APR[approval / policy gate]
  end

  subgraph Domain["Danışmanlık bağlamı (Faz 1)"]
    COS[sentinel-coming/skills + documantations]
  end

  T --> EP
  EP --> CFG --> PROF
  CFG --> REG
  REG --> REM
  REG --> LOC
  REM --> STR
  LOC --> STR
  STR --> LOOP
  LOOP --> HIST
  LOOP --> PARSE
  PARSE --> APR
  APR --> HOOK
  HOOK --> TR
  TR --> BASH
  TR --> FS
  TR --> MCP
  LOOP -.-> COS
```

## Veri akışı (özet)

1. **Başlangıç:** CLI argümanları ve ortam değişkenleri `config merge` ile birleştirilir; aktif **profil** (ör. `SENTINEL_PROFILE=local`) hangi LLM bloğunun seçileceğini belirler.

2. **Sağlayıcı seçimi:** `Provider registry` uygun modülü yükler: uzak API için taban URL + API key; lokal için `base_url` (örn. `http://127.0.0.1:11434/v1`) ve model adı. Her iki yol da mümkün olduğunca **aynı iç mesaj şemasına** (ör. OpenAI chat uyumlu) map edilir; Anthropic gibi farklı API’ler **adapter** ile bu şemaya veya ortak iç modele dönüştürülür.

3. **Ajan döngüsü:** Kullanıcı mesajı + sistem talimatları + (varsa) proje skill metinleri modele gider. Stream biter veya tool çağrıları üretilir. Tool çağrıları **policy** ve **onay**dan geçer, yürütülür, sonuçlar geçmişe eklenir; tur sayısı ve durdurma koşulları kontrol edilir.

4. **Danışmanlık:** Sistem veya skill talimatları, ajanı Faz 1 dokümantasyonu (`sentinel-coming/documantations/`) ve Faz 1 skill’leri (`sentinel-coming/skills/juju-*`, `cos-*`, `microk8s-*`) ile uyumlu komut ve teşhis sırasına yönlendirir. Faz 2 agentic skill metinleri `cli/skills/agentic-*` altındadır.

## Güvenlik ve sınırlar (mimari)

- **Sırlar:** API anahtarları tercihen ortam veya gizli depo; repoda düz metin önerilmez (ayrıntı `LLM_PROVIDERS.md` ve ilgili skill).
- **Yürütme:** Üretim benzeri ortamlarda terminal ve dosya araçları **onay** veya **kısıtlı mod** ile bağlanmalıdır (uygulama politikası).
- **MCP:** Yalnızca yapılandırılmış sunucular; yetkisiz sunucu eklenmesi kullanıcı onayına tabi tutulmalıdır.

## İzleme (isteğe bağlı)

CLI içi **yapılandırılmış log** (seviye, olay türü, session id) ve isteğe bağlı **OpenTelemetry** veya dosyaya trajectory; Faz 2 planında hangi sprint’te ekleneceği tanımlanır.

## İlgili belgeler

Bu dosya ile **aynı klasörde** (`cli/documantations/`):

- `REPO_LAYOUT_RECOMMENDED.md` — mantıksal katmanlara karşılık **önerilen** kaynak dizin yapısı  
- `LLM_PROVIDERS.md` — ortam değişkenleri ve mod matrisi  
- `IMPLEMENTATION_PLAN_PHASE2.md` — fazlı teslimat  
- `SKILL_CATALOG_PHASE2.md` — skill → katman eşlemesi  
- `PROJECT_ROOT_PHASE2.md` — Faz 2 proje özeti  
- `archive/` — Faz 2.A–E teslim notları (tarihsel; günlük okuma zorunlu değil)

Faz 1: `../../documantations/PROJECT_ROOT.md`, `../../documantations/ARCHITECTURE_COS.md`

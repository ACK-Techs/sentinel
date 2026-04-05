# Yol haritası — Faz 3–5

**Faz 2 (A–E)** `IMPLEMENTATION_PLAN_PHASE2.md` ile kapatıldı. **Faz 5** planı şimdilik yok; önce **Faz 3 ve 4**.

---

## Kapsam sınırı (önemli)

**Şu anki hedef:** Sistemi **yalnızca kendi kullanımın** için olgunlaştırmak — kendi makinede kur, dene, test et, gereksinimleri öğren.

- **Faz 3 ve 4** bu doğrultuda: iç kullanım, geliştirme ve doğrulama odaklı.  
- **Şirkete / müşteriye / dışarıya** yönelik paketleme, satış veya “kurumsal ürün” dilini **bu fazların doküman ve kodunda taşıma** niyeti yok; o aşama **sonra**, gerçek kullanımdan çıkan gereksinimlere göre çevrilecek.  
- **Telemetri (anonim istatistik vb.):** **Ürün ortaya çıktıktan sonra** eklenebilir; şimdilik **yok**, Faz 3’te de zorunlu değil.

---

## Özet fazlar

| Faz | Çalışma adı | Amaç (özet) |
|-----|-------------|-------------|
| **3** | CLI’yi kendi kullanımına “tam” sayılacak hale getirmek | Kendi makinede kurulum, paketleme, sertleştirme, tek okunabilir dokümantasyon — **hepsi bireysel/dev kullanımı için**. |
| **4** | Observability + Grafana LLM kolaylığı | Kendi stack’inde Grafana; **bağlantı testi** (mock CI + **istenen gerçek yığın** doğrulaması). Stack çalışırken canlı HTTP ile doğrula; ayrıntı: `IMPLEMENTATION_PLAN_PHASE4.md`. |
| **5** | (Sonra) | İleride planlanır. |
| **Bireysel kapanış** | REPL ↔ Grafana operasyonel özet | `doctor` sonucunun ajan bağlamına secret-safe taşınması; plan: `IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` |

---

## Onaylı kararlar

### Faz 3

1. **Dağıtım:** Öncelik **senin ortamında** tekrarlanabilir kurulum: wheel/sdist, `pip install -e`, doküman — **halka PyPI veya müşteri teslimi şart değil**; dışarıya özel kanal kararı **ürün aşamasında**.  
2. **Feature flag’ler:** Test için **hepsi açık kalabilir**; varsayılanları kilitleme işi **sonra**.  
3. **Telemetri:** **Şimdilik yok**; ürün netleştikten sonra düşünülür.

### Faz 4

4. **Entegrasyon:** Kendi observability kurulumunda Grafana; **Grafana’nın LLM bağlantıları için sunduğu kolaylık** hedeflenir.  
5. **Çok kullanıcılı giriş / yönetici hesabı:** **Şimdilik bu roadmap’in parçası değil**; observability ve ürün ihtiyacı netleşince ayrı tasarlanır. **Şu anki odak:** tek kullanıcı, kendi makine, öneri ve çözüm üreten CLI.  
6. **Test:** **Bağlantı var mı** yeterli; mümkünse observability yığını açıkken **gerçek** HTTP doğrulaması da yapılır (`PHASE4_REAL_STACK_VERIFY.md`, secret yok).

### Faz 5

7. **Ertelendi** — önce 3 ve 4.

---

## Dokümantasyon bakımı

- Faz 2 teslim notları: `archive/README.md`  
- Uygulama planları: [IMPLEMENTATION_PLAN_PHASE3.md](IMPLEMENTATION_PLAN_PHASE3.md), [IMPLEMENTATION_PLAN_PHASE4.md](IMPLEMENTATION_PLAN_PHASE4.md) (iç kullanım dilinde)  
- Faz 3’ü otomasyonla tek seferde yürütmek için: [CODEX_EXECUTION_PROMPT_PHASE3.md](CODEX_EXECUTION_PROMPT_PHASE3.md) — indeks: [PHASE3_SKILL_AND_DOC_INDEX.md](PHASE3_SKILL_AND_DOC_INDEX.md)  
- Faz 4: [CODEX_EXECUTION_PROMPT_PHASE4.md](CODEX_EXECUTION_PROMPT_PHASE4.md) — indeks: [PHASE4_SKILL_AND_DOC_INDEX.md](PHASE4_SKILL_AND_DOC_INDEX.md)  
- Bireysel kapanış: [CODEX_EXECUTION_PROMPT_INDIVIDUAL_CLOSE.md](CODEX_EXECUTION_PROMPT_INDIVIDUAL_CLOSE.md) — indeks: [INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md](INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md)

---

## Sonraki adım

1. Faz 3 görevlerini `IMPLEMENTATION_PLAN_PHASE3.md` üzerinden yürüt.  
2. Ardından Faz 4: `IMPLEMENTATION_PLAN_PHASE4.md`.  
3. Bireysel kullanım için REPL–Grafana bağlamı: `IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` — indeks: `INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md`.  
4. Dışa dönük ürün ve telemetri — **ayrı faz / ayrı karar**.

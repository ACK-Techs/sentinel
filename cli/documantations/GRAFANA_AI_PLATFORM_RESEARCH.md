# Grafana × AI / LLM — araştırma özeti (Sentinel bağlamı)

**Amaç:** Sentinel CLI ile “Grafana’yı ajanın görmesi” eksığını kapatırken, Grafana ekosisteminin **nerede** LLM sunduğunu ve **self-hosted COS** ile sınırları netleştirmek.

**Not:** Bağlantılar resmi Grafana kaynaklarına gider; ürün duyuruları zamanla değişebilir — uygulamada sürüm ve dokümandan doğrula.

---

## 1. Grafana tarafında LLM / ajan özellikleri (platform)

| Özellik | Kısa açıklama | Sentinel ile ilişki |
|--------|----------------|---------------------|
| **LLM plugin (grafana-llm-app)** | Grafana içinde merkezi LLM erişimi: anahtar saklama, istek proxy, akış. OpenAI, Anthropic, OpenAI-uyumlu uç noktalar. | Bu, **Grafana UI içindeki** özellikler; Sentinel’in dış terminal ajanı **otomatik paylaşmaz**. Kendi LLM’ini Grafana’ya bağlamak için ayrı kurulum. |
| **Grafana Assistant (Grafana Cloud)** | Sayfa/datasource bağlamıyla gömülü ajan (yan panel). Araştırma, panel/dashboard yardımı. | **Cloud** odaklı; kendi COS + Traefik Grafana’nızda birebir aynısı olmayabilir. |
| **Grafana Assistant CLI / Tunnel (duyurular)** | Cloud ekosisteminde CLI/tünel ile asistan erişimi (yol haritası/önizleme). | Sentinel’ten **farklı ürün hattı**; entegrasyon kararı ayrı. |

Kaynaklar (genel bakış):

- [LLM plugin for Grafana](https://grafana.com/grafana/plugins/grafana-llm-app)
- [Grafana Assistant blog](https://grafana.com/blog/2025/05/07/llm-grafana-assistant)
- [LLM plugin / ML app docs](https://grafana.com/docs/plugins/grafana-ml-app/latest/llm/llm-setup)

---

## 2. Programatik erişim (CLI / otomasyon için)

Sentinel’in Faz 4’te yaptığı gibi **HTTP API** temel kalır:

- Kimlik: çoğunlukla `Authorization: Bearer <service_account_token>` (ve gerekirse `X-Grafana-Org-Id`).
- Sağlık: `GET /api/health` (Traefik alt yolunda 302 → izlenen yönlendirme gibi edge case’ler).
- İleri veri: datasource sorguları, dashboard API, Prometheus uyumlu sorgu uçları — **ayrı endpoint ve yetki** ister.

API referansı: [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/)

---

## 3. Mimari ayrım (kafa karışıklığını önlemek için)

1. **Grafana’nın içindeki LLM** = kullanıcı Grafana’da çalışırken asistan / açıklama / üretim özellikleri.  
2. **Sentinel CLI REPL** = ayrı süreç; modele giren tek şey **prompt + (varsa) tool çıktıları**.  
3. **Köprü** = ya (a) modele **özet bağlam enjekte etmek** (doctor sonucu, kısa statik config özeti), ya (b) **tool/MCP** ile Grafana’dan veri çekmek, ya (c) kullanıcının metin olarak yapıştırması.

Faz 4 yalnızca (3) için altyapıyı doğrular; **bireysel kapanış** (implementation plan) (a) ve/veya (b) ile eksığı kapatır.

---

## 4. COS / self-hosted notu

Canonical COS + `grafana-k8s` kurulumunuzda:

- Traefik **proxied endpoints** her zaman tüm uygulamaları listelemeyebilir; Grafana yolu ortamınıza özel (ör. `/cos-grafana-0`).
- LLM plugin kurulu değilse Grafana içinde “AI” sekmesi yoktur; bu **eksiklik değil**, farklı ürün katmanıdır.

Teşhis: `skills/agentic-troubleshoot-grafana/SKILL.md`, `skills/agentic-troubleshoot-traefik-ingress/SKILL.md`.

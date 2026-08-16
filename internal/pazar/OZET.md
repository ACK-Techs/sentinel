# Özet

Şirket içi. Public değil. Tarama: 16 Ağustos 2026.

## Bu pazar nedir

Sentinel tek kutuya oturmuyor: OSS observability yüzeyi + AIOps/agentic SRE + CLI-first operator asistanı. 2026’da büyük satıcılar AI’yi kendi platformunun özelliği olarak satıyor. Bağımsız AI SRE (HolmesGPT/Robusta, Resolve) mevcut stack’in üzerine ajan koyuyor. Sentinel ikinci gruba yakın; farkı Datadog yerine **OSS LGTM + kendi read-only gateway**.

Tam Datadog rakibi değil. Doğal dil sorgusu tek başına özellik; gateway + yazmasız CLI ürün olabilir.

## Benzer ürün var mı

En yakın: **HolmesGPT** (CNCF Sandbox, 0.33.0 / 15 Haz 2026, Prometheus/Loki/Tempo, CLI, read-only varsayılan) + ticari katman **Robusta**. İkinci: Grafana gcx (GA 28 Tem 2026) + Grafana Assistant + mcp-grafana.

Komşu ve canlı: Datadog Bits AI (DASH 9 Haz 2026), AWS DevOps Agent (GA 31 Mar 2026), Azure SRE Agent, k8sgpt, kubectl-ai, Copilot CLI, Honeycomb Intelligence. **New Relic Grok 2026 ürün adı değil**; bugün New Relic AI / SRE Agent. OTel bir rakip ürün değil, Mayıs 2026’da CNCF graduation.

## Sentinel’in durduğu yer

Boşluk: Prom/Loki/Tempo önünde daraltılmış salt-okunur API + tek Python CLI + BYO LLM/Ollama. Grafana Assistant tam güç Cloud’a bağlı — self-managed kama.

Risk: HolmesGPT bu işi ücretsiz yapıyor. Grafana Temmuz 2026’da gcx+Assistant+MCP ile niche’i kapattı. Copilot CLI + mcp-grafana DIY satın alma gerektirmez. “AI SRE” cümlesi duyulmaz; “LGTM için güvenli CLI asistanı” dar ama anlatılabilir.

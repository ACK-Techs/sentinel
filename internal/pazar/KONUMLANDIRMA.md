# Konumlandırma

Şirket içi. Public değil. Tarama: 16 Ağustos 2026.

## Boşluk

1. Read-only HTTP gateway — Prom/Loki/Tempo’yu tek token + timeout ile toplamak. HolmesGPT doğrudan toolset; Grafana MCP Grafana API. “Ajan telemetry’ye Grafana veya kubeconfig olmadan dar API ile gider” güvenlik hikâyesi. Çekirdek bu olmalı.
2. CLI-first REPL — install, doctor, obs, lab. Hepsini tek Python CLI’da seven: platform, COS/lab, air-gap.
3. BYO LLM (Ollama) + read-only default — Datadog/AWS vermez. Grafana LLM plugin ve HolmesGPT verir; gateway + lab ile paketleyen az.

Cümle: Datadog değiliz. Grafana Cloud Assistant değiliz. Prometheus/Loki/Tempo önünde, varsayılan yazmasız, terminalden konuşulan operator asistanı — modeli siz seçersiniz.

## Risk

1. HolmesGPT ücretsiz, CNCF, aynı omurga. Fark gateway + lab + tek repo olmadan özellik kopyası gibi durur.
2. Grafana Temmuz 2026: gcx + Cloud MCP + Assistant GA. Self-managed tam Assistant hâlâ Cloud’a bağlı — en temiz kama; kip kapanırsa daralır.
3. Copilot CLI + mcp-grafana + k8sgpt DIY.
4. “AI SRE” her sitede aynı. Observability platform diye çıkmak intihar.
5. Yalnızca NL PromQL = özellik. Ürün: gateway RBAC/audit/air-gap, lab’den üretime aynı CLI, HolmesGPT’den neden başka binary.

## Kim alır / almaz

Alır (hipotez): LGTM self-host eden platform/SRE; KVKK/GDPR/air-gap; Ollama; lab/COS.  
Almaz: Datadog’dan “AI da olsun” diyen enterprise; ücretsiz kubectl-ai; Slack on-call otomasyonu (Robusta/PagerDuty).

SaaS olursa Grafana $20/kullanıcı ve Datadog kredi ile yarışır — kaybeder. Makul yol: OSS CLI+gateway + ileride air-gap/policy paket (Robusta modeli).

# Grafana HTTP — Faz 4 (taslak)

Bu dosya **Faz 4 uygulaması** sırasında, kurduğun Grafana sürümüne göre güncellenir: hangi **HTTP uçları** kullanıldığı, **Authorization** biçimi ve resmi dokümantasyon linkleri.

## Resmi kaynaklar (genel)

- [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/) — sürüm seçiciden kendi sürümünü seç.

## Planlanan ortam sözleşmesi (kod ile senkron tutulacak)

| Değişken | Anlam |
|----------|--------|
| `SENTINEL_GRAFANA_BASE_URL` | Örn. `https://grafana.example.com` (sonunda `/` olmadan) |
| `SENTINEL_GRAFANA_API_KEY` veya proje kararı | Bearer token; **repoya yazılmaz** |

## Doğrulama uçları (örnek)

Uygulama tamamlanınca burada **tek birincil health/ready** uç seçilir (ör. `GET /api/health`). Gerçek yol Grafana sürümüne göre Codex/dokümantasyon ile netleştirilir.

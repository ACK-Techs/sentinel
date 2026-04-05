# Grafana HTTP — Faz 4

Faz 4 için Sentinel CLI'nin rolü dar tutulur: Grafana'da dashboard veya datasource yaratmaz; yalnızca verilen ayarlarla HTTP erişiminin cevap verip vermediğini doğrular ve operatörü gerekirse teşhis skill'ine yönlendirir.

## Resmi kaynaklar

- [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [Grafana service account tokens](https://grafana.com/docs/grafana/latest/administration/service-accounts/)

Seçilen uç, Grafana HTTP API dokümantasyonundaki yaygın sağlık kontrolü yolu olan `GET /api/health` üstünden sabitlendi. Sentinel varsayılan olarak bu yolu kullanır; gerekirse `SENTINEL_GRAFANA_HEALTH_PATH` ile override edilebilir.

## Faz 4 ortam sözleşmesi

| Değişken | Anlam |
|----------|--------|
| `SENTINEL_GRAFANA_ENABLED` | Opsiyonel; açıkça Grafana kontrolünü işaretler |
| `SENTINEL_GRAFANA_BASE_URL` | Örn. `https://grafana.example.com` (sonunda `/` olmadan) |
| `SENTINEL_GRAFANA_TOKEN` | Bearer token veya service account token; **repoya yazılmaz** |
| `SENTINEL_GRAFANA_TOKEN_ENV` | Token'ın hangi env değişkeninden okunacağını override eder |
| `SENTINEL_GRAFANA_HEALTH_PATH` | Varsayılan `/api/health` |
| `SENTINEL_GRAFANA_TIMEOUT_SEC` | Kısa bağlantı testi timeout değeri |
| `SENTINEL_GRAFANA_VERIFY_SSL` | Varsayılan `true`; self-signed/TLS istisnası bilinçli karar olmalı |

## HTTP davranışı

- İstek türü: `GET`
- Yol: `GET /api/health`
- Header: token varsa `Authorization: Bearer <token>`
- Başarı: `200`
- Kimlik hatası: `401` veya `403`
- Ağ/TLS problemi: timeout veya HTTP istemci hatası olarak raporlanır

Sentinel `doctor` çıktısında ham token, tam secret veya parola yazdırmaz. Yalnızca token var/yok bilgisi ve HTTP sonucu özetlenir.

## Teşhis köprüsü

Bağlantı başarısız ama Grafana ayakta görünüyorsa, operatör şu skill'e yönlendirilir:

- `skills/agentic-troubleshoot-grafana/SKILL.md`

Bu köprü özellikle şu ayrımı net tutar:

- Login veya token sorunu
- URL/ingress erişim sorunu
- Datasource bağlı ama panelde "no data" görünmesi

## "No data" notu

`/api/health` 200 dönmesi tek başına dashboard verisinin doğru olduğu anlamına gelmez. Grafana erişiyor olsa bile datasource relation sırası, Prometheus/Loki bağlantısı veya zaman aralığı yüzünden panel boş kalabilir. Bu durumda önce datasource sağlığını, sonra Faz 1 teşhis akışını doğrula.

## Doğrulama uyarısı

Grafana veya LLM tabanlı öneriler teşhis yardımcısıdır; otomatik olarak doğru kabul edilmemelidir. Özellikle TLS istisnası, self-signed sertifika veya datasource değişikliklerinde öneriyi canlı ortam belirtileriyle doğrula.

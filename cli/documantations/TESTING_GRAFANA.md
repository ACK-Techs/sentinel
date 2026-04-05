# Grafana testing

Bu repo varsayilan olarak agsiz CI kosullarini hedefler. Bu nedenle Faz 4 testlerinin ana yolu `httpx.MockTransport` kullanan unit testlerdir; canli Grafana testleri ayrik marker ile tutulur.

## Kurulum

```bash
cd sentinel-coming/cli
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## CI benzeri calistirma

```bash
cd sentinel-coming/cli
.venv/bin/python -m ruff check .
.venv/bin/python -m pytest -q
```

Bu yol `live` marker'li testleri toplamaz. Varsayilan davranis `-m "not live"` ile aynidir.

## Canli Grafana testi

Canli testler yalniz istege baglidir ve gercek ağa gider. Secret degerleri repoya yazmayin.

Gerekli env:

```bash
export SENTINEL_GRAFANA_BASE_URL=https://grafana.example.com
export SENTINEL_GRAFANA_TOKEN=replace-me
# Opsiyonel:
# export SENTINEL_GRAFANA_HEALTH_PATH=/api/health
# export SENTINEL_GRAFANA_TIMEOUT_SEC=5
# export SENTINEL_GRAFANA_VERIFY_SSL=true
```

Canli marker ile calistirma:

```bash
cd sentinel-coming/cli
.venv/bin/python -m pytest -q -m live tests/integration/test_grafana_live.py
```

Basari kriteri:

- `200`: baglanti ve yetki dogrulandi
- `401` veya `403`: Grafana cevap veriyor; token veya yetki ayrica duzeltilmeli

Test ve rapor ciktisinda URL veya token yazmayin. Ozet olarak yalniz HTTP kodu ve durum kullanin.

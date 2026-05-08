---
name: python-docstring-standard
description: "Google/NumPy docstring standartları ve sphinx entegrasyonu — Sentinel SDK API dokümantasyonu için"
---

## Purpose
Tutarlı docstring formatı hem IDE autocomplete kalitesini artırır hem de Sphinx ile otomatik API docs üretimini mümkün kılar. Sentinel'de Google style docstring tercih edilir; NumPy style yalnızca bilimsel/sayısal API'lerde kullanılır.

## Workflow

### 1. Google style — fonksiyon

```python
def query_prometheus(
    url: str,
    promql: str,
    start: str = "now-1h",
    end: str = "now",
    step: str = "60s",
) -> list[dict]:
    """Prometheus'tan anlık veya aralıklı metrik verisi çeker.

    HTTP GET /api/v1/query_range endpoint'ine istek atar ve sonucu
    normalize edilmiş dict listesi olarak döndürür.

    Args:
        url: Prometheus base URL (ör. http://prometheus:9090).
        promql: Geçerli bir PromQL sorgu ifadesi.
        start: Başlangıç zamanı, RFC3339 veya relative (now-1h).
        end: Bitiş zamanı, RFC3339 veya relative (now).
        step: Örnekleme adımı (ör. 60s, 5m, 1h).

    Returns:
        Her element `{"metric": {...}, "values": [[timestamp, value], ...]}``
        formatında dict olan liste. Sonuç yoksa boş liste döner.

    Raises:
        MetricQueryError: Prometheus 4xx/5xx yanıt döndürdüğünde.
        httpx.TimeoutException: Bağlantı zaman aşımında.

    Example:
        >>> data = query_prometheus(
        ...     "http://prometheus:9090",
        ...     'rate(http_requests_total[5m])',
        ...     start="now-30m",
        ... )
        >>> print(data[0]["metric"]["job"])
        'gateway'
    """
```

### 2. Google style — sınıf

```python
class TempoClient:
    """Grafana Tempo HTTP API istemcisi.

    Sentinel'in trace sorgulama katmanı için Tempo'ya HTTP/2 bağlantısı
    yönetir. Connection pool ve retry mantığı dahilidir.

    Attributes:
        base_url: Tempo API base URL.
        timeout: İstek zaman aşımı saniyesi.
        max_retries: Başarısız isteklerde maksimum yeniden deneme sayısı.

    Example:
        >>> client = TempoClient("http://tempo:3200", timeout=5.0)
        >>> trace = await client.get_trace("abc123ef")
    """

    def __init__(self, base_url: str, timeout: float = 10.0, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: httpx.AsyncClient | None = None
```

### 3. NumPy style (sayısal API)

```python
def compute_error_rate(
    total_requests: np.ndarray,
    error_requests: np.ndarray,
) -> np.ndarray:
    """Hata oranı vektörünü hesaplar.

    Parameters
    ----------
    total_requests : np.ndarray, shape (N,)
        Toplam istek sayısı zaman serisi.
    error_requests : np.ndarray, shape (N,)
        Hatalı istek sayısı zaman serisi.

    Returns
    -------
    np.ndarray, shape (N,)
        [0.0, 1.0] aralığında hata oranı. total_requests sıfırsa NaN.

    Notes
    -----
    Division by zero koruması np.errstate ile sağlanır.
    """
    with np.errstate(invalid="ignore"):
        return np.where(total_requests > 0, error_requests / total_requests, np.nan)
```

### 4. Sphinx conf.py entegrasyonu

```python
# docs/conf.py
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",    # Google/NumPy style
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
autodoc_typehints = "description"
```

## Common mistakes

- `Args:` bloğunda tip tekrar yazmak — type hint'ler zaten var, docstring'de yalnızca açıklama yaz
- `Returns:` bloğunu atlamak — IDE'ler ve Sphinx döndürülen değeri belgeleyemez
- Raises bloğunu eksik bırakmak — çağıran kod hangi exception'ı yakalaması gerektiğini bilmez
- Tek satırlık docstring'e Args/Returns koymak — tek satır yalnızca özet içermelidir

## References
- `skills/python-ruff-lint`
- `skills/python-mypy-strict`
- `skills/fastapi-openapi-customization`

# Faz 2.A Sirlar ve Hassas Veri Yonetimi

Bu belge, `agentic-secrets-handling` skill'inin Faz 2.A teslimidir. Gercek anahtar depolamaz; placeholder ve operasyon kurali tanimlar.

## Saklama sirasi

1. Secret manager veya vault benzeri cozum
2. Ortam degiskeni
3. Yerel dosya, ancak kisitli izinle (`chmod 600`) ve repo disinda tercih edilir

## Placeholder env sozlesmesi

`.env.example` dosyasi yalniz su isimleri placeholder olarak kullanir:

- `SENTINEL_PROFILE`
- `SENTINEL_MODEL`
- `SENTINEL_OPENAI_BASE_URL`
- `SENTINEL_API_KEY`
- `SENTINEL_LOCAL_BASE_URL`
- `SENTINEL_LOCAL_MODEL`
- `SENTINEL_LOCAL_TIMEOUT_SEC`
- `ANTHROPIC_API_KEY`
- `SENTINEL_ANTHROPIC_MODEL`

Bu isimler [LLM_PROVIDERS.md](/home/caglarkc/Desktop/sentinel/sentinel-coming/cli/documantations/LLM_PROVIDERS.md) ile uyumlu tutulmustur.

## Git ve dosya hijyeni

- `cli/.gitignore` icinde `.env`, `.env.*`, `*.pem`, `*.key`, `*.token`, `secrets/`, `sessions/`, `trajectories/` ve benzeri hassas ciktilar ignore edilir.
- Gercek anahtar, kubeconfig veya Juju credential repoya eklenmez.
- Bir sizinti fark edilirse yeni degisim yapmadan once rotate edilir ve gereken history temizligi proseduru baslatilir.

## Log ve trajectory ilkeleri

- Debug dahil hicbir log seviyesinde tam key, token, JWT veya kubeconfig icerigi yazilmaz.
- Trajectory/session kaydi eklendiginde secret redaction zorunlu olacaktir.
- Hata mesajlari kullaniciya kisaca donmeli, secret deger yansitmamalidir.

## Operasyon notu

- Fork tabanli CI akislarinda secret olmayacagi varsayilir.
- Lokal LLM modunda dahi servisler mumkunse `127.0.0.1` ile sinirli tutulur.

## Ilgili belgeler

- `LLM_PROVIDERS.md`
- `DEPENDENCY_LICENSES.md`
- `THREAT_MODEL_PHASE2A.md`

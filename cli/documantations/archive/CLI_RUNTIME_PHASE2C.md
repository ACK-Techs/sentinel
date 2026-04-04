# Faz 2.C CLI Runtime Ozeti

## Alt komutlar

- `run`: tek seferlik prompt
- `repl`: etkilesimli mod
- `config`: efektif config ve aktif profil
- `doctor`: profil, model, base_url, API key varligi ve MCP durumu
- `version`: paket surumu

Arguman verilmeden:

- stdin TTY degilse once modu calisir
- stdin TTY ise REPL baslar

## Cikis kodlari

- `0`: basari
- `2`: config veya kullanim hatasi
- `3`: LLM/provider hatasi
- `4`: tool/validation hatasi
- `130`: kullanici iptali

## Logging

- Varsayilan stderr JSON log
- `--verbose` debug detaylarini acar
- Stack trace normal modda yazdirilmaz

## MCP

- Faz 2.C'de MCP runtime best-effort ve opsiyoneldir
- `sentinel-cli[mcp]` kurulmadan yalnizca disabled/diagnostic yolu calisir
- Tool adlandirma kuralı: `mcp_<server>_<tool>`

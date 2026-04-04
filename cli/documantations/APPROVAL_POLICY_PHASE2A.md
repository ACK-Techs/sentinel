# Faz 2.A Onay Politikasi Tasarimi

Bu belge, `agentic-approval-policy-design` skill'ine uygun olarak Faz 2.A icin varsayilan risk siniflarini ve onay matrisini sabitler. Bu turda enforcement kodu zorunlu degildir; net metin sozlesmesi yeterlidir.

## Risk siniflari

| Sinif | Tanim | Ornek |
|------|-------|-------|
| `read-safe` | Salt okuma, hassas pattern disi dusuk risk | Repo icindeki genel dokuman veya kod dosyasi okumak |
| `read-sensitive` | Salt okuma ama sir veya operasyon verisi icerebilir | `.env`, kubeconfig, credential dosyasi, CI secret dosyalari |
| `write-controlled` | Geri alinabilir ama mutating islem | Kaynak dosyaya patch, config dosyasi guncelleme |
| `shell-low` | Dusuk riskli tek adimli shell | `pwd`, `ls`, `python -m` gibi denetimli komut |
| `shell-high` | Ayricalik, network etkisi veya yikici potansiyel | `sudo`, `rm`, servis durdurma, paket kurma, uzun betik calistirma |

## Varsayilan onay matrisi

| Islem turu | Interactive varsayilan | Automation/CI varsayilan |
|------------|------------------------|--------------------------|
| `read-safe` | Otomatik izin | Otomatik izin |
| `read-sensitive` | Kullanici onayi zorunlu | Varsayilan red veya mock |
| `write-controlled` | Diff/ozet goster, sonra onay | Varsayilan kapali; yalniz acik profile ile |
| `shell-low` | Ozet + tekil onay tercih edilir | Dar allowlist ile |
| `shell-high` | Varsayilan red | Yasak |

## Ek kurallar

- `sudo` veya yetki yukselten komutlar Faz 2 icin varsayilan olarak reddedilir.
- Birden fazla mutating adim iceren akislarda onay tek komut bazli degil, islem ozeti bazli dusunulmelidir.
- "YOLO" veya tam otomatik kip ileride eklenirse varsayilan kapali olur ve uretim profiline acilmaz.
- Policy degisiklikleri oturum kaydina yazilmalidir.

## Not

Bu matris Faz 2.A icin belge seviyesinde sabittir. Faz 2.C arac katmaninda ayni adlarla kodlastirilmasi beklenir.

## Ilgili belgeler

- `THREAT_MODEL_PHASE2A.md`
- `PROMPT_INJECTION_GUARDRAILS_PHASE2A.md`
- `ARCHITECTURE_AGENTIC_CLI.md`

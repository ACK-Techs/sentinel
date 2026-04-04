# Faz 2.A Tehdit Modeli Ozeti

Bu belge, `agentic-threat-model` ve ilgili skill'lerle uyumlu ilk tehdit ozetidir. Faz 2.A amaci, tum kontrolleri kodlamak degil; risk siniflarini, mitigasyon yonunu ve kabul edilen riskleri acik yazmaktir.

## Varliklar

- LLM API key ve benzeri kimlik bilgileri
- Kullanici calisma dizini, config ve oturum dosyalari
- Shell ve dosya araci uzerinden tetiklenebilecek degisiklikler
- Faz 1 ile ilgili kubeconfig, Juju credential ve operasyon verileri
- Ileride eklenecek MCP sunucu baglantilari

## Tehdit ozeti

| Tehdit | Ornek senaryo | Etki | Baslangic mitigasyonu | Kabul edilen risk |
|--------|---------------|------|------------------------|-------------------|
| Shell komutlarinin kotuye kullanimi | Model tehlikeli veya yikici komut onerir | Yuksek | Varsayilan onay matrisi, risk siniflamasi, `sudo`/yikici kaliplarda engel | Faz 2.A'da kod gate yok; politika metinle sabit |
| Hassas dosya sizintisi | `.env`, kubeconfig veya secret dosyalari okunur | Yuksek | Secret pattern ignore, untrusted istekte durdurma, read/write ayrimi | Salt belge seviyesi, runtime enforcement Faz 2.C'de |
| API key log sizintisi | Hata logu veya trajectory tam anahtar yazar | Yuksek | Redaction zorunlulugu, `.env.example` placeholder, gercek secret repoya alinmaz | Logger henuz uygulanmadi |
| Prompt injection | Web/issue icerigi sistem talimatini ezmeye calisir | Orta-Yuksek | Untrusted icerik ayri ele alinir, ozetlenmeden tool argumani olmaz, supheli durumda dur/sor | Hook ve parser Faz 2.C'ye kaldi |
| Kotu niyetli MCP sunucusu | Sahte sunucu veri ceker veya komut yonlendirir | Yuksek | Yalniz allowlist/yapilandirilmis sunucu, yeni sunucu icin acik kullanici onayi | MCP kodu henuz yok |
| Lokal LLM servisinin dis aga acilmasi | `0.0.0.0` dinleyen local endpoint | Orta | `127.0.0.1` ornegi, dokumantasyon uyarisı, profil bazli kontrol | Runtime dogrulama Faz 2.B'ye kaldi |

## Mitigasyon ilkeleri

1. Okuma, yazma ve shell aksiyonlari farkli risk siniflarina ayrilir.
2. Sırlar icin once vault/secret manager, sonra env, en son izinli dosya kullanilir.
3. Untrusted icerik hicbir zaman sistem talimati gibi muamele gormez.
4. Referans depolardan kod kopyalamadan once lisans ve uyarlama kaydi kontrol edilir.

## Kabul edilen riskler

- Faz 2.A sonunda onay ve guardrail'ler belge seviyesinde netlesmis olur; enforcement kodu Faz 2.C'ye tasinir.
- CLI henuz shell veya filesystem araci calistirmadigi icin riskler gercek yuzeyden cok tasarim seviyesindedir.

## Ilgili belgeler

- `APPROVAL_POLICY_PHASE2A.md`
- `SECRETS_HANDLING_PHASE2A.md`
- `PROMPT_INJECTION_GUARDRAILS_PHASE2A.md`
- `ARCHITECTURE_AGENTIC_CLI.md`

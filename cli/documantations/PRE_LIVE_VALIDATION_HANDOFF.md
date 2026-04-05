# Canlı bağlantı öncesi doğrulama — yönetici el sıkışması

**Amaç:** Gerçek Grafana/COS ortamına `doctor` veya CLI ile bağlanmadan önce kod ajanından iki teslim almak: (1) mimari sağlamlık raporu, (2) özellik bazlı test kapsamı + makinede çalıştırma talimatı.

**Bağlam:** Faz 4 teslimi tamamlandı (ör. `ruff` + `pytest` yeşil, mock tabanlı Grafana kontrolleri). `PHASE4_REAL_STACK_VERIFY.md` şu an *stack kapalı* atlama satırı içeriyor; COS/Juju ayağa kalktıktan sonra canlı doğrulama ayrı turda yapılacak ve bu dosya **secret olmadan** güncellenecek.

**Kök:** `sentinel-coming/cli/`

---

## Görev A — Mimari ve yapı incelemesi (rapor, kod değişikliği zorunlu değil)

Aşağıdaki bloğu **kod yazan ajana** tek görev olarak ver.

```text
Kök: sentinel-coming/cli/

Görev: Kod tabanının mimari sağlamlık ve eksiklik incelemesi — rapor üret, isteğe bağlı küçük düzeltmeler.

Kapsam (hepsini tara ve özetle):
- Paket yapısı: src layout, pyproject, bağımlılık sınırları, public API
- Config: Pydantic modelleri, loader (dosya + env önceliği), örnek YAML ile gerçek davranış uyumu
- CLI: run/repl/config/doctor akışları, hata mesajları, secret sızıntısı riski
- Faz 4: observability/grafana.py, doctor içindeki Grafana özeti, env sözleşmesi (SENTINEL_GRAFANA_*), GRAFANA_HTTP_PHASE4.md ile kod uyumu
- Test stratejisi: unit vs integration, mock kullanımı, boşluklar
- Güvenlik ve operasyon: timeout, SSL verify, loglarda hassas veri

Çıktı formatı (markdown rapor):
1. Executive summary (5–10 cümle)
2. Güçlü yönler
3. Riskler / teknik borç (öncelik: yüksek-orta-düşük)
4. Önerilen geliştirmeler (madde madde, dosya yolu ile)
5. Faz 4 canlı test öncesi özellikle kontrol edilmesi gerekenler

Kısıt: Uzun refaktör veya geniş kapsamlı özellik ekleme yapma; rapor odaklı. Net bug veya tek satırlık güvenlik düzeltmesi varsa ayrı bölümde listele, uygulamayı ayrı onayla yap.
```

---

## Görev B — Özellik bazlı testler + çalıştırma rehberi

Aşağıdaki bloğu **ayrı bir oturumda** veya A’dan sonra ver.

```text
Kök: sentinel-coming/cli/

Görev: Faz 4 ve ilgili yüzeyler için test kapsamını genişlet; “bağlanıyor / bağlanmıyor / atlandı” durumlarını pytest ile mümkün olduğunca kodla ifade et; canlı ağ gerektirenleri işaretle.

Zorunlu ilkeler:
- CI’da varsayılan: ağ yok — mevcut mock transport / httpx.MockTransport kalıbını kullan.
- Secret repoya girmesin; fixture’larda sahte URL/token.
- Gerçek Grafana’ya istek atan testler varsa: pytest marker (ör. @pytest.mark.live veya requires_network) ve varsayılan koleksiyonda SKIP veya -m "not live" ile hariç tut; dokümanda açıkça yaz.

Kapsam örnekleri (eksikleri sen tamamla):
- GrafanaSettings: env override, token_env adı, health_path, verify_ssl, enabled bayrakları
- check_grafana_connection: skipped (base_url yok), 200, 401/403, timeout, TLS/verify edge (mock ile)
- load_config + grafana bloğu: sentinel.example.yaml ile uyum
- doctor JSON çıktısı: grafana anahtarı var mı, troubleshoot_skill yolu, ham token yok
- Regresyon: mevcut test_cli_modes / test_config_loader ile çakışma yok

Teslimler:
1. Yeni veya güncellenmiş test dosyaları (tests/unit ve gerekirse tests/integration)
2. Kısa “Test çalıştırma” bölümü: ya documantations/ altında küçük bir TESTING_GRAFANA.md ya da README’ye alt başlık — şu komutlar net olsun:
   - venv: python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
   - CI benzeri: .venv/bin/python -m ruff check . && .venv/bin/python -m pytest -q
   - Canlı (opsiyonel): hangi env değişkenleri, hangi pytest -m komutu, başarı kriteri (HTTP kodu özeti, URL/token yazma yasağı)

Çalıştırma: Mümkünse aynı oturumda ruff + pytest çalıştır; kullanıcı makinesinde komutları kopyala-yapıştır ile tekrarlanabilir olsun.
```

---

## Senin (insan) sıran — canlı doğrulama

Stack hazırsa (ör. Juju `grafana` active, Traefik ingress URL’si):

1. Repoya token yazma; `export` veya `.env` (gitignore).
2. `SENTINEL_GRAFANA_BASE_URL` = Traefik üzerinden Grafana’ya giden **taban URL** (yol ve TLS senin kurulumuna göre).
3. `sentinel-cli doctor` (veya projedeki eşdeğer) çalıştır.
4. `documantations/PHASE4_REAL_STACK_VERIFY.md` tablosunu doldur; önceki “stack kapalı” cümlesini güncelle veya değiştir.

---

## İndeks güncellemesi

Bu dosya, Faz 4 sonrası **canlı test öncesi** koordinasyon içindir. İlgili: [PHASE4_MANAGER_HANDOFF.md](PHASE4_MANAGER_HANDOFF.md), [PHASE4_SKILL_AND_DOC_INDEX.md](PHASE4_SKILL_AND_DOC_INDEX.md).

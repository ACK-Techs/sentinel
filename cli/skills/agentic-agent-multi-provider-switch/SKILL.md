---
name: agentic-agent-multi-provider-switch
description: Oturumlar arası profil ve sağlayıcı değişiminde riskleri ve yeni oturum önerisini tanımlarken kullan.
---

## Amaç

Aynı **thread** içinde OpenAI uyumlu ile Anthropic arasında geçiş, mesaj **tool şema farkı** nedeniyle risklidir. Kural: **profil değişiminde yeni oturum öner**; zorunluluğu proje kararı. **Config reload**: çalışan süreçte dosya değişimi destekleniyorsa dokümante et; değilse yeniden başlat.

## Kapsam

### Dahil

- CLI ile `--profile` değişimi davranışı.
- Geçmiş temizliği / uyarı mesajı şablonu.

### Hariç

- Çoklu model voting / ensemble.

## Kurallar

- Eski provider’a özel tool sonuçları yeni provider’da reddedilebilir; temiz başlangıç tercih.
- `agentic-config-profiles` ile alan haritası tutarlı.
- Session dosyası provider alanı yazılırsa migration notu.

## Kontrol listesi

- [ ] Profil değişince model adı ve base_url doğrulandı mı?
- [ ] Kullanıcıya “geçmiş sıfırlansın mı?” soruluyor mu (interactive)?
- [ ] CI’da tek profil sabit mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Karışık tool id | History | Yeni oturum |
| Eski API key kullanıldı | Env cache | Process restart |

## İlgili belgeler ve skill'ler

- `../agentic-config-profiles/SKILL.md`
- `../agentic-llm-provider-contract/SKILL.md`
- `../agentic-session-persistence/SKILL.md`
- `../documantations/LLM_PROVIDERS.md`

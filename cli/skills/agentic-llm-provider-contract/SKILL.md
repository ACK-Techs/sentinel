---
name: agentic-llm-provider-contract
description: Uygulama içi LLM soyutlaması için complete/stream, hata tipleri ve iptal sözleşmesini tanımlarken kullan.
---

## Amaç

Tüm sağlayıcılar için **ortak arayüz**: örn. `complete` / `stream` (veya eşdeğeri), **iptal** (task cancel / timeout), **hata tipleri** (ağ, auth, oran, sunucu, şema). İç temsil: **mesaj rolleri** (`system`, `user`, `assistant`, `tool`), **tool call** iç yapısı (ad, argüman JSON, call id). Sağlayıcı adapter’ı bu sözleşmeye map eder (`ARCHITECTURE_AGENTIC_CLI.md`).

## Kapsam

### Dahil

- Minimum metot seti ve dönüş tipleri (proje dili ne olursa olsun).
- Streaming olaylarının üst kümesi (`agentic-llm-streaming-events` ile uyum).

### Hariç

- Her bulut sağlayıcısının özel beta API’leri (dokümanda “resmi dokümanda doğrula”).

## Kurallar

- OpenAI uyumlu ve Anthropic yolları aynı **iç modele** veya aynı olay enum’ına birleştirilir.
- Tool çağrısı kısmi parçalar stream’de birikir; tamamlanınca tek doğrulanmış yapı üretilir.
- İptal: kullanıcı Ctrl+C veya API abort; kaynak sızıntısı olmaması için context manager önerisi.

## Kontrol listesi

- [ ] Birim testte mock provider sözleşmeyi ihlal edince test kırılıyor mu?
- [ ] Hata tipi → kullanıcı mesajı eşlemesi `agentic-cli-user-errors` ile uyumlu mu?
- [ ] Tüm `agentic-llm-*` skill’ler bu sözleşmeye atıfta mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Adapter eksik metot | Protocol / trait | Derleme hatası veya runtime guard |
| Tool şema uyuşmazlığı | Provider ham çıktı | Parse katmanında açıklayıcı hata |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../documantations/LLM_PROVIDERS.md`
- `../agentic-llm-streaming-events/SKILL.md`
- `../agentic-llm-anthropic-messages/SKILL.md`
- `../agentic-agent-tool-call-parse/SKILL.md`

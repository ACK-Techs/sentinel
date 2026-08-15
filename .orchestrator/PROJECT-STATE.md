# Current Project State

## Durum

- Sentinel Pre-Alpha bir observability ve altyapı otomasyon projesidir.
- Asıl ürün `sentinel-cli` (`cli/`), read-only `observability-gateway/` ve lab `test-platform/` ağaçlarındadır.
- Compose ve Kubernetes (Helm) kurulum yolları çalışır; COS installer preflight/install/verify adımları kodda TODO'dur.
- Gateway Prometheus, Loki ve Tempo için tek read-only HTTP girişidir; CLI backend URL'lerini doğrudan bilmez.
- `agentic/` bağımsız referans projeler içerir; teslim edilen ürün değildir.
- `.orchestrator` geliştirme control plane'i kuruldu; henüz ürün run graph'ı yok.

## Ürün sınırları

| Yol | Ne yapar | Ne yapmaz |
|---|---|---|
| Compose | Yerel observability stack + gateway | Kubernetes, Juju, COS, test-platform servisleri |
| Kubernetes Helm | Mevcut kümede chart + gateway | Küme oluşturmaz |
| COS / Juju | Script'lerle lab hazırlığı; CLI discovery yarım | `sentinel install --mode cos` COS indirmez |

## Bir sonraki çalışma

Kullanıcı geliştirmeyi başlattığında PM Manager ilk run'ı hedefe göre oluşturmalıdır. Tipik sıra:

1. İlgili modül contract'ı (CLI komut yüzeyi, gateway API, installer davranışı).
2. Implement + test.
3. Bağımsız review ve verify (`cli`: Ruff/Pytest; `observability-gateway`: Pytest; lab: smoke script).
4. Docs/INSTALL senkronu.
5. Conventional Commit ve `git push`.

Bu maddeler doğrudan kodlanmadan önce aktif run içinde architecture/contract, implement, review, verify ve integration item'larına bölünmelidir.

## Açık kullanıcı sınırları

- Gateway write/admin/alert/dashboard/proxy genişlemesi kullanıcı onayı ister.
- Paid provider/credential, production write, destructive operation, cluster mutation ve image publish kullanıcı/platform boundary'sidir.
- Commit mesajı `type(scope): summary` kuralına uymalıdır; `Work-Item` ve `Phase` isteğe bağlıdır.
- Mesaj uygunsa `git add` / `git commit` / `git push` serbesttir; force-push yasaktır.

## Resume

Yeni oturum bu dosyadan sonra `.orchestrator/runs/` altındaki aktif run'ları kontrol eder. Bu state dosyası run graph'ın yerine geçmez; run oluştuğunda gerçek execution state run/event/result dosyalarındadır.

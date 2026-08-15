# Sentinel Commit ve Push Standardı

Hook'lar yalnız commit dilini doğrular. Mesaj uygunsa normal Git akışı serbesttir:

```bash
git add .
git commit -m "feat(cli): add doctor token check"
git push
```

Yerel hook'ları bir kez etkinleştirin:

```bash
git config core.hooksPath .githooks
```

## 1. Tek commit biçimi

```text
type(scope): imperative English summary
```

İsteğe bağlı:

```text
type(scope): imperative English summary

Optional body explaining why.

Work-Item: <run-work-item-id>
Phase: <phase-id>
```

Kurallar:

- `type` ve `scope` İngilizce, küçük harf ve ASCII olmalıdır.
- Özet İngilizce, emir kipinde, küçük harfle başlamalı ve nokta ile bitmemelidir.
- Subject en fazla 72 karakter olmalıdır.
- `Work-Item` ve `Phase` zorunlu değildir; orchestrator run'ına bağlamak istenirse eklenir.
- Commit tek bir mantıksal amacı kapsamalıdır.

## 2. İzin verilen type değerleri

| Type | Kullanım |
|---|---|
| `feat` | Kullanıcıya veya tüketiciye yeni davranış |
| `fix` | Hatalı davranışın düzeltilmesi |
| `docs` | Yalnız dokümantasyon |
| `test` | Yalnız test/fixture kapsamı |
| `refactor` | Davranışı değiştirmeyen kod yapısı değişikliği |
| `perf` | Ölçülmüş performans iyileştirmesi |
| `build` | Build/dependency/toolchain |
| `ci` | CI/CD ve otomasyon |
| `chore` | Ürün davranışı olmayan bakım/repo işlemi |
| `revert` | Önceki commit'in kontrollü geri alınması |

## 3. Scope seçimi

Scope, değişen ürün alanını anlatır: `cli`, `agent`, `llm`, `tools`, `gateway`, `obs`, `install`, `compose`, `k8s`, `cos`, `charts`, `test-platform`, `scripts`, `skills`, `docs`, `security`, `memory`, `session`, `ci`, `orchestrator`, `repo`.

## 4. Faz değerleri

`Phase` footer kullanılırsa yalnız şunlardan biri geçerlidir:

- `phase-cli-runtime`
- `phase-observability-gateway`
- `phase-test-platform`
- `phase-installers`
- `phase-charts`
- `phase-ops-lab`
- `phase-skills-docs`
- `phase-security`
- `phase-ci`
- `phase-orchestrator`

## 5. Doğru örnekler

```text
feat(gateway): keep tempo search behind the read-only api
```

```text
fix(cli): fail doctor when the gateway token is missing
```

```text
chore(orchestrator): add project control plane
```

## 6. Yasak örnekler

```text
updates
fix stuff
wip
feat: changes
feat(gateway): Added some things.
```

Force-push, `fixup!` / `squash!` remote'a taşımak ve `--no-verify` ile hook'u atlamak yasaktır. `scripts/auto-push-watch.sh` bu protokolün yerine geçmez.

## 7. Push

Mesaj kuralına uyan commit'ler `git push` ile gönderilir. `git-checkpoint.mjs push` zorunlu değildir; isteğe bağlı toplu doğrulama yardımcısıdır.

- `commit-msg` hook'u commit anında dilini doğrular
- `pre-push` hook'u gönderilen commit dilini doğrular; uygun mesajı engellemez
- Push fast-forward olmalıdır
- Force-push yasaktır

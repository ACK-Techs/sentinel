---
name: agentic-devcontainer-optional
description: VS Code devcontainer ile tutarlı geliştirme ortamı için örnek alanlar ve Docker socket risk uyarısı verirken kullan.
---

## Amaç

**`.devcontainer/devcontainer.json`**: `image` veya `Dockerfile`, `features` (Python, git), `postCreateCommand` (`uv sync` veya `pip install -e .`), `remoteUser`. **Docker socket mount**: geliştirme kolaylığı sağlar ancak **konteyner kaçışı** riski — yalnız güvenilir repolarda ve bilinçli tercih. **Alternatif**: socket olmadan, sadece dil runtime.

## Kapsam

### Dahil

- CLI geliştirme için minimal uzantı önerisi (Python, Ruff).
- Workspace mount ve `forwardPorts` (lokal LLM portu için).

### Hariç

- Kurumsal devcontainer registry politikası.

## Kurallar

- Root kullanıcıdan kaçın (mümkünse).
- Secret’ları devcontainer env dosyasına koyma; `secrets` veya host env mount dokümante.
- `agentic-repo-layout` ile dizin uyumu.

## Kontrol listesi

- [ ] Konteyner içinde `pytest` yeşil mi?
- [ ] `git` safe directory ayarı gerekli mi?
- [ ] Docker socket gerçekten gerekli mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Mount izin | uid/gid | devcontainer özellikleri |
| Yavaş volume | osxfs | clone strategy |

## İlgili belgeler ve skill'ler

- `../agentic-repo-layout/SKILL.md`
- `../agentic-packaging-pypi/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`
- `../agentic-threat-model/SKILL.md`

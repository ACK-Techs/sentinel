---
name: juju-bundle-deploy
description: "Juju bundle YAML dosyasıyla birden fazla uygulamayı ve aralarındaki relation'ları tek komutla dağıtmak, bundle'ı override dosyasıyla özelleştirmek ya da mevcut deployment'ı bundle ile eşitlemek gerektiğinde kullan."
---

## Purpose
Bundle, karmaşık çok-uygulama deployment'larını tekrarlanabilir hale getirir. COS Lite ve diğer Juju çözümleri bundle formatında dağıtılır.

## Temel bundle yapısı
```yaml
bundle: kubernetes
applications:
  prometheus-k8s:
    charm: prometheus-k8s
    channel: latest/stable
    scale: 1
  grafana-k8s:
    charm: grafana-k8s
    channel: latest/stable
    scale: 1
    options:
      admin-password: changeme
integrations:
  - - prometheus-k8s:grafana-source
    - grafana-k8s:grafana-source
```

## Bundle deploy
```bash
juju deploy ./cos-lite.yaml
# veya Charmhub'dan:
juju deploy cos-lite
```

## Override dosyası ile özelleştirme
Yerel `overlay.yaml` bundle'ı değiştirmeden genişletir:
```yaml
applications:
  grafana-k8s:
    options:
      admin-password: prod-sifre-123
```
```bash
juju deploy cos-lite --overlay overlay.yaml
```

## Mevcut deployment ile senkronizasyon
```bash
juju diff-bundle cos-lite.yaml  # planlanmış değişiklikleri gösterir
juju deploy cos-lite.yaml       # idempotent; yalnızca delta uygulanır
```

## Tüm application/relation çekme (export)
```bash
juju export-bundle > current-state.yaml
```

## Common mistakes
- `options` ve `config` anahtar kelimelerini karıştırmak — bundle'da `options` kullanılır.
- Overlay'de yanlış intent: override `applications` düzeyinde çalışır, `integrations` ayrı ele alınır.
- `diff-bundle` çalıştırmadan doğrudan deploy yapmak — beklenmedik kaynaklar silinebilir.

## References
- `skills/juju-charm-deploy`
- `skills/juju-relation-add-remove`
- `skills/cos-bundle-overview`

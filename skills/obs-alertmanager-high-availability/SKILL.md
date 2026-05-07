---
name: obs-alertmanager-high-availability
description: Alertmanager’ı HA modunda çalıştırmak (cluster/peers, gossip mesh, dedup) veya “HA var ama duplicate bildirim gidiyor” sorununu çözmek gerektiğinde kullan. Amaç doğru cluster üyeliği ve tekil bildirim davranışıdır.
---

## Purpose
Bu skill’in çıktısı:
- HA topolojisi kararı (kaç replica, peer keşfi, servis/ingress)
- Duplicate suppression’ın çalışması için gerekli koşullar checklist’i
- Doğrulama: aynı alert iki Prometheus’tan gelse bile tek bildirim kanıtı

## Workflow
- HA hedefini yaz:
  - Neyi koruyoruz? (Alertmanager pod ölümü, node ölümü, zone)
  - RPO: silences/notification state kaybı kabul edilebilir mi?
- Peer keşfi:
  - Replica’lar birbirini nasıl bulacak? (stable DNS, headless service, static peer list)
- Ağ gereksinimi:
  - Cluster portları/mesh erişimi açık mı? (network policy, firewall)
- Dedup koşulları:
  - Prometheus’lar aynı alert’i aynı label set’iyle mi gönderiyor?
  - Alertmanager’lar aynı cluster’ın üyesi mi? (split brain var mı?)
- Operasyonel kontroller:
  - Rolling restart sırasında cluster küçülürken duplicate olmamalı.
  - Time drift (NTP) kontrolü.
- Doğrulama:
  - İki farklı kaynaktan aynı alert’i gönder; notification sayısı tek mi ölç.

## Common mistakes
- Peers yanlış/eksik: cluster oluşmaz → her replica ayrı bildirim yollar.
- Split brain (iki ayrı cluster): dedup bozulur.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`

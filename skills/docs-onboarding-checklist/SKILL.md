---
name: docs-onboarding-checklist
description: "Sentinel projesine yeni katılan geliştirici için adım adım onboarding kontrol listesi ve ilk hafta planı"
---

## Purpose
Sentinel'in karmaşık altyapısı — Juju, MicroK8s, COS, multiple FastAPI services, 600+ skills — yeni bir geliştiriciye bunaltıcı gelebilir. Bu skill, ilk günden itibaren bağımsız katkı yapabilecek düzeye gelinmesi için yapılandırılmış bir ilerleme planı sunar.

## Workflow

### 1. Onboarding checklist (documentations/onboarding.md)
```markdown
# Sentinel Onboarding Checklist

## Gün 1: Ortam Kurulumu
- [ ] Repoyu fork et ve clone'la
- [ ] `make dev-setup` çalıştır — MicroK8s + COS + target services
- [ ] `kubectl get pods -n sentinel-target` → tüm pod'lar Running
- [ ] `kubectl get pods -n sentinel-cos` → COS pod'ları Running
- [ ] Grafana'yı aç: `http://localhost:3000` (admin/admin)
  - [ ] "Sentinel Overview" dashboard'unu bul
  - [ ] Bir servis metriği görüntüle

## Gün 2: Mimariyi Anla
- [ ] `documentations/adr/` altındaki ilk 5 ADR'ı oku
- [ ] `skills/cos-bundle-overview` SKILL.md oku
- [ ] `skills/target-app-repo-layout` SKILL.md oku
- [ ] Trace oluştur ve Tempo'da izle:
  ```bash
  curl http://localhost:8080/orders -X POST -d '{"product_id":"sku-1","quantity":1,"user_id":"u-1"}'
  # Grafana → Explore → Tempo → Trace ID ile ara
  ```

## Gün 3: Chaos ve Anomali
- [ ] `skills/target-app-chaos-api` oku
- [ ] `degraded` profili aktifleştir ve Grafana'da etkisini gözlemle:
  ```bash
  curl -X POST http://localhost:8001/admin/chaos -d '{"profile":"degraded"}'
  ```
- [ ] Alert'i tetikle ve runbook'u takip et

## Gün 4: İlk Katkı
- [ ] `skills/docs-contributing-guide` oku
- [ ] "good first issue" etiketli bir issue seç
- [ ] PR açma sürecini takip et

## Hafta 2: Derinleşme
- [ ] COS charm'larından birini Juju üzerinden config'ini değiştir
- [ ] Yeni bir Prometheus alert rule yaz
- [ ] Target servise yeni endpoint ekle (test dahil)
- [ ] Bir skill SKILL.md dosyasını geliştir ve PR aç

## Yardım Kaynakları
| Konu | Kaynak |
|------|--------|
| Juju | `skills/debug-juju-hook-failure` |
| OTel | `skills/target-app-fastapi-otel-bootstrap` |
| Chaos | `skills/target-app-chaos-api` |
| CI | `skills/ci-pr-gate` |
| Alerting | `skills/obs-prometheus-alerting-rules` |
```

### 2. Ortam kurulum otomasyonu
```bash
# Makefile
.PHONY: dev-setup
dev-setup:
	@echo "1/5 MicroK8s addon'ları aktifleştiriliyor..."
	microk8s enable dns storage ingress
	@echo "2/5 COS deploy ediliyor..."
	juju deploy cos-lite --trust
	@echo "3/5 Target servisler deploy ediliyor..."
	helm upgrade --install sentinel-target helm/sentinel-target -n sentinel-target --create-namespace
	@echo "4/5 Port-forward başlatılıyor..."
	kubectl port-forward -n sentinel-cos svc/grafana 3000:3000 &
	kubectl port-forward -n sentinel-target svc/gateway 8080:8080 &
	@echo "5/5 Smoke test çalıştırılıyor..."
	sleep 10 && make smoke-test
```

### 3. Bilgi doğrulama soruları (Gün 5)
```markdown
## Bilgi Kontrolü
Aşağıdaki soruları yanıtlayabilmeli:
1. Bir orders isteği hangi servislerden geçer?
2. Chaos profili `outage` etkinken Grafana'da ne görürsün?
3. Tempo'da bir trace'i trace ID ile nasıl bulursun?
4. Juju ile COS bileşenlerini nasıl yönetirsin?
5. Sentinel'de yeni bir skill nasıl oluşturulur?
```

### 4. Buddy system
```markdown
## Mentor Atama
- İlk hafta: her geliştirici bir deneyimli ekip üyeyle eşleştirilir
- Günlük 15 dakika check-in: blocker var mı?
- PR review: ilk 3 PR buddy tarafından incelenir
```

## Common mistakes
1. Onboarding'i README'de "setup" bölümüne sıkıştırmak — ayrı, kapsamlı, kademeli bir dosya gerek.
2. Ortam kurulumunu test etmeden güncellemek — her değişiklik temiz VM'de test edilmeli.
3. Katkı yapmadan 1 hafta geçmesine izin vermek — ilk gün küçük de olsa bir katkı güven oluşturur.
4. Sadece teknik konuları kapsamak — iletişim kanalları, toplantı takvimi, karar alma süreci de dahil edilmeli.

## References
- `skills/docs-contributing-guide`
- `skills/docs-readme-structure`
- `skills/target-app-repo-layout`

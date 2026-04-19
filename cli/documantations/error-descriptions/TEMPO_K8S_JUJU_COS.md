# Juju COS / MicroK8s — `tempo-k8s` “Tempo API not ready” ve ilgili hatalar

Bu not, `cos` modelinde `tempo-k8s` charm’ı ile yaşanan **waiting**, **hook failed** ve cluster kesintilerinde görülen durumlar için teşhis ve kurtarma özetidir.

## Belirtiler

- `juju status`: uygulama **waiting**, mesaj: **“Tempo API not ready just yet…”**
- Bazen birim **error**, mesaj: **hook failed: "start"** veya Pebble ile ilgili hook hataları
- `microk8s stop` / API kesintisi sonrası birimlerde **agent lost**

## Kök nedenler (birlikte veya ayrı görülebilir)

### 1. Charm / Pebble (sık görülen teknik sebep)

`tempo-k8s` charm’ı, Pebble’dan “workload ready” bildirimi gelince `tempo-ready` adlı Pebble servisini durdurmaya çalışır. Servis henüz tanımlı değilse:

```text
ops.pebble.APIError: cannot stop services: service "tempo-ready" does not exist
```

İlgili kod yolu: `_on_tempo_pebble_custom_notice` → `self.tempo.container.stop("tempo-ready")`. Hook (`tempo-pebble-custom-notice`) başarısız olunca birim uzun süre **waiting** kalabilir.

**PC aç/kapa veya pod yeniden başlayınca neden tekrarlıyor?**  
Yeniden başlatmada Pebble bazen **workload-ready** bildirimini, `tempo-ready` servisi henüz yokken veya plandan düşmüşken iletebilir. Eski charm revizyonlarında `stop("tempo-ready")` **try/except olmadan** çağrıldığı için hook her seferinde düşer; `juju status` yine **“Tempo API not ready…”** gösterebilir. Upstream `tempo-k8s-operator` içinde bu durum için `APIError`/`RuntimeError` yakalanıp log’a debug yazılıyor; bu düzeltme **daha yeni charm revlerinde** (ör. `latest/edge`) bulunur.

**Kalıcı düzeltme (stable rev 71’de takılı kaldıysan):**

```bash
juju switch cos
juju refresh tempo --channel=latest/edge --force-units
```

Edge riskli sayılabilir; ileride aynı düzeltme `latest/stable`’a gelince tekrar `juju refresh tempo --channel=latest/stable` ile sabitleyebilirsin. Sadece `scale-application 0` / `1` **aynı revde** hook’u tekrar tetiklediği için tek başına bu hatayı çözmeyebilir.

**Doğrulama:**

```bash
juju debug-log --include unit-tempo-0 --replay --no-tail | grep -E 'tempo-ready|APIError|tempo-pebble-custom-notice'
```

### 2. MicroK8s / cluster kapalı veya DNS yok

`microk8s stop` veya API erişilemezken:

```text
cannot resolve "controller-service.controller-microk8s-controller.svc.cluster.local"
```

Birimlerde **agent lost** görülmesi beklenir; cluster ayağa kalkınca genelde toparlanır.

### 3. Charm refresh + kesinti (edge/candidate)

Yükseltme sırasında cluster veya birim yeniden başlarsa bazen:

```text
exec: ./src/charm.py: not found
hook "start" ... failed: exit status 127
```

gibi **yarım/bozuk charm dizini** belirtileri çıkabilir.

**Not:** `juju restart` komutu her Juju sürümünde yoktur; CAAS için yeniden denemek için `refresh`, `scale-application` veya pod yenileme kullanılır.

## MicroK8s’i her seferinde güvenli başlatma (Juju / Tempo yarışı)

Doğrudan `sudo microk8s start` sonrası API veya `cos` pod’ları henüz hazır değilken Juju uniter tetiklenirse sorunlar görülebilir. Depoda sıralı bekleme yapan betik:

```bash
cd sentinel-coming
sudo ./scripts/cos-microk8s-start.sh
```

Takılı Tempo’yu otomatik **edge refresh** ile kurtarmak için (isteğe bağlı):

```bash
COS_HEAL_TEMPO=1 sudo ./scripts/cos-microk8s-start.sh
```

Bu script artik IP drift kurtarmasini da yapar:

- Juju client kubeconfig'lerinde eski `https://<ip>:16443` endpoint'lerini yeni host IP ile hizalar
- `/var/snap/juju/*/microk8s/credentials/client.config` kopyalarini gunceller
- `kubelet.crt` icindeki eski IP SAN'ini tespit ederse cert'i yeniden uretir ve MicroK8s'i yeniden baslatir

Sadece bu fix'i ayri calistirmak icin:

```bash
sudo ./scripts/cos-microk8s-heal.sh
```

**Kalıcı önlem:** `tempo-k8s` için `latest/edge` (veya bu düzeltmeyi içeren stable rev) kullanmaya devam et; aksi halde `latest/stable` rev 71 ile her yeniden başlatmada `tempo-ready` hatası tekrarlanabilir.

## Kurtarma adımları (önerilen sıra)

1. **Gerçek hatayı oku**

   ```bash
   juju debug-log --include unit-tempo-0 --replay --no-tail | tail -80
   ```

2. **Workload pod logu (namespace ve pod adını kendi çıktına göre düzelt)**

   ```bash
   sudo microk8s kubectl get pods -n cos | grep -i tempo
   sudo microk8s kubectl logs -n cos tempo-0 -c tempo --tail=200
   ```

   Container adı farklıysa:

   ```bash
   sudo microk8s kubectl get pod -n cos tempo-0 -o jsonpath='{.spec.containers[*].name}{"\n"}'
   ```

3. **Takılı kalıyorsa birimi yeniden oluştur**

   ```bash
   juju scale-application tempo 0
   # birkaç saniye bekle
   juju scale-application tempo 1
   ```

4. **Charm kanalı** (`tempo-ready` + `APIError` doğrulandıysa öncelik burada)

   - **`tempo-ready does not exist` ise:** `juju refresh tempo --channel=latest/edge --force-units` (yukarıdaki “Kalıcı düzeltme”).
   - Stabil tutmak için (düzeltme stable’a gelince): `juju refresh tempo --channel=latest/stable`
   - Ara risk: `latest/candidate`
   - Hata durumundaki birimlere zorlamak için her kanalda: `--force-units`

5. **Birim Juju’da “error” ve hook bekliyorsa**

   ```bash
   juju resolved tempo/0
   ```

   yalnızca birim gerçekten hata durumunda ve neyi onayladığını bildiğinizde kullanın.

## Tek satırlık hatırlatma

Tempo uzun süre **waiting** → önce `juju debug-log --include unit-tempo-0`; **`tempo-ready` + Pebble `APIError`** görülüyorsa sorun büyük ölçüde charm/Pebble tarafı; cluster kapalıysa önce DNS/API’yi düzelt.

## Uzun vadeli not

Canonical ekosisteminde `tempo-k8s` tek başına sınırlı/legacy kalabilir; üretim için **Charmed Tempo HA** (ör. `tempo-coordinator-k8s` / `tempo-worker-k8s`) geçiş rehberlerine bakmak mantıklıdır.

---

*Son güncelleme: COS / Juju 3.6.x, `tempo-k8s` (stable rev 71’de `tempo-ready` hatası; edge rev 83’te try/except düzeltmesi doğrulandı) ve MicroK8s.*

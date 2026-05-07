Önce mevcut skill'lere bakayım.

Mevcut format ve içerikleri anladım. Şimdi kapsamlı analiz yapıp listeyi hazırlıyorum.

Mevcut 65 skill'in format ve içeriğini analiz ettim. Şimdi 500+ skill listesi hazırlıyorum — mevcut boşlukları ve eksik alanları kapsayacak şekilde kategorize edilmiş:

---

## 500+ Skill Listesi

### Kategori 1: obs-prometheus

---

### Kategori 1: obs-prometheus (20 skill)
1. `obs-prometheus-scrape-config` — Prometheus scrape job ve hedef keşif kurallarını yapılandırırken kullan.
2. `obs-prometheus-recording-rules` — Sık sorgulanan metrikleri önceden hesaplayan recording rule yazarken kullan.
3. `obs-prometheus-alerting-rules` — Prometheus alerting rule sözdizimi ve threshold belirleme kurallarını yazarken kullan.
4. `obs-prometheus-remote-write` — Prometheus remote_write ve uzak depolama entegrasyonunu kurarken kullan.
5. `obs-prometheus-federation` — Çok-küme senaryolarında Prometheus federation ile merkezi metrik toplarken kullan.
6. `obs-prometheus-storage-tsdb` — TSDB retention politikası ve disk büyüme tahmini yaparken kullan.
7. `obs-prometheus-query-range` — PromQL query_range API parametrelerini ve sonuç yapısını kullanırken kullan.
8. `obs-prometheus-instant-query` — PromQL anlık sorgu endpoint'ini ve dönen veri modelini anlamak için kullan.
9. `obs-prometheus-labels-strategy` — Metrik label tasarımı, kardinalite riski ve normalleştirme kurallarını belirlerken kullan.
10. `obs-prometheus-histogram-summary` — Histogram ve Summary farkını, bucket tasarımını ve quantile hesabını anlatırken kullan.
11. `obs-prometheus-service-discovery` — Kubernetes SD, file SD ve static_config ile hedef keşfi yapılandırırken kullan.
12. `obs-prometheus-operator-crds` — ServiceMonitor/PodMonitor/PrometheusRule CRD'leri ile k8s-native izleme kurarken kullan.
13. `obs-prometheus-anomaly-detection` — PromQL ile z-score ve ratio trend tabanlı anomali tespiti yazarken kullan.
14. `obs-prometheus-api-auth` — Prometheus HTTP API'ye basic auth, TLS veya reverse proxy erişim güvenliği sağlarken kullan.
15. `obs-prometheus-capacity-planning` — Metrik sayısı ve scrape interval'e göre kaynak kapasitesi planlarken kullan.
16. `obs-prometheus-exemplars` — Trace-metric köprüsü için exemplar yapılandırması ve Grafana görselleştirmesini kurarken kullan.
17. `obs-prometheus-multi-tenancy` — Label tabanlı izolasyon ve tenant-aware sorgulama kurallarını uygularken kullan.
18. `obs-prometheus-backup-restore` — TSDB snapshot alma ve geri yükleme prosedürünü uygularken kullan.
19. `obs-prometheus-unit-testing` — promtool ile alerting/recording kural birim testini yazarken kullan.
20. `obs-prometheus-juju-charm-metrics` — Juju charm'larının sunduğu metrikleri ve scrape relation yapılandırmasını anlamak için kullan.

### Kategori 2: obs-loki (20 skill)
21. `obs-loki-query-logql` — LogQL filtre, parser ve metric query sözdizimini yazarken kullan.
22. `obs-loki-label-strategy` — Loki label tasarımı, high-cardinality önleme ve index boyutu optimizasyonu yaparken kullan.
23. `obs-loki-push-api` — Loki push API'sine log gönderme payload ve label formatını kurarken kullan.
24. `obs-loki-storage-backend` — Loki depolama backend seçimi (filesystem, S3, BoltDB) ve yapılandırmasını kurarken kullan.
25. `obs-loki-compactor` — Loki compactor retention politikası ve indeks temizleme prosedürünü yapılandırırken kullan.
26. `obs-loki-ruler-alerts` — Loki ruler ile log tabanlı alerting kuralı yazarken kullan.
27. `obs-loki-multi-tenancy` — X-Scope-OrgID header ile çok kiracılı log izolasyonu yaparken kullan.
28. `obs-loki-chunk-cache` — Loki chunk cache (memcached/redis) entegrasyonu ile sorgu performansını artırırken kullan.
29. `obs-loki-structured-metadata` — OTel log attribute ile zenginleştirilmiş Loki sorguları yaparken kullan.
30. `obs-loki-pattern-detection` — Loki pattern sorguları ile log anomalisi ve hata kümeleme analizi yaparken kullan.
31. `obs-loki-ingester-config` — Loki ingester flush interval, chunk encoding ve WAL ayarlarını yapılandırırken kullan.
32. `obs-loki-query-frontend` — Loki query frontend sharding ve caching stratejisini ayarlarken kullan.
33. `obs-loki-promtail-config` — Promtail scrape config, pipeline stages ve multi-line log birleştirmeyi kurarken kullan.
34. `obs-loki-otel-collector-export` — OTEL Collector'dan Loki'ye log export pipeline'ını yapılandırırken kullan.
35. `obs-loki-grafana-datasource` — Grafana'da Loki datasource, derived field ve trace-log korelasyonunu kurarken kullan.
36. `obs-loki-troubleshoot-ingest` — Loki'ye log gelmiyor durumunda ingestion pipeline sorunlarını teşhis ederken kullan.
37. `obs-loki-troubleshoot-query` — Loki sorgu hatası, timeout ve boş sonuç durumlarında teşhis adımlarını uygularken kullan.
38. `obs-loki-chunk-encoding` — Loki sıkıştırma formatları (gzip, snappy, lz4, zstd) ve performans trade-off'larını seçerken kullan.
39. `obs-loki-index-gateway` — Loki index gateway bileşenini ayrı node olarak konuşlandırırken kullan.
40. `obs-loki-recording-rules` — Loki recording rules ile log metriği türeterek Prometheus'a bridge yaparken kullan.

### Kategori 3: obs-tempo (18 skill)
41. `obs-tempo-trace-query` — Tempo trace arama API'si ve TraceQL sorgu sözdizimini kullanırken kullan.
42. `obs-tempo-traceql-advanced` — TraceQL span attribute filtresi ve structural operator kullanımını yazarken kullan.
43. `obs-tempo-storage-backend` — Tempo depolama backend seçimi (local, S3, GCS) ve parça yönetimini yapılandırırken kullan.
44. `obs-tempo-sampling-strategy` — Head-based ve tail-based sampling stratejisi ve OTEL Collector sampling yapılandırmasını yaparken kullan.
45. `obs-tempo-exemplars-grafana` — Tempo-Prometheus exemplar köprüsünü Grafana explore'da kurarken kullan.
46. `obs-tempo-distributor-config` — Tempo distributor ve receiver protokolleri (OTLP, Jaeger, Zipkin) yapılandırırken kullan.
47. `obs-tempo-compactor-retention` — Tempo compactor ve trace retention politikasını uygularken kullan.
48. `obs-tempo-multi-tenancy` — Tempo tenant header ile çok kiracılı trace izolasyonu yaparken kullan.
49. `obs-tempo-grafana-datasource` — Grafana'da Tempo datasource, trace-log korelasyonu ve service graph kurarken kullan.
50. `obs-tempo-service-graph` — Tempo service graph metriklerini Prometheus'a aktararak topoloji görselleştirmesi yaparken kullan.
51. `obs-tempo-span-metrics` — Tempo span metrics pipeline ile RED metriklerini türetirken kullan.
52. `obs-tempo-troubleshoot-ingest` — Tempo'ya trace gelmiyor durumunda ingestion sorunlarını teşhis ederken kullan.
53. `obs-tempo-troubleshoot-query` — Tempo sorgu hatası, boş trace ve timeout durumlarında teşhis adımlarını uygularken kullan.
54. `obs-tempo-otel-sdk-integration` — Uygulama tarafında OTEL SDK ile trace üretimi ve Tempo export yapılandırmasını yaparken kullan.
55. `obs-tempo-jaeger-compat` — Jaeger UI uyumluluğu gereken ortamlarda Tempo jaeger receiver kullanımını yaparken kullan.
56. `obs-tempo-pipeline-e2e` — OTEL SDK → Collector → Tempo → Grafana zincirini uçtan uca doğrularken kullan.
57. `obs-tempo-resource-sizing` — Tempo bileşen hafıza/CPU boyutlandırması ve disk büyüme tahmini yaparken kullan.
58. `obs-tempo-hot-cold-storage` — Tempo hot/cold storage katmanlaması ve object storage migration yaparken kullan.

### Kategori 4: obs-grafana (22 skill)
59. `obs-grafana-dashboard-design` — Grafana dashboard panel seçimi, layout ve değişken tasarımı kurallarını uygularken kullan.
60. `obs-grafana-variables` — Template değişkenleri (query, custom, interval, datasource) oluşturup kullanırken kullan.
61. `obs-grafana-alerting-unified` — Grafana unified alerting, contact point ve notification policy kurarken kullan.
62. `obs-grafana-annotations` — Grafana annotation oluşturma ve event-driven annotation yaparken kullan.
63. `obs-grafana-datasource-proxy` — Grafana datasource proxy güvenliği ve auth forward kurallarını uygularken kullan.
64. `obs-grafana-provisioning` — YAML dosyaları ile dashboard/datasource/alert otomatik yüklemeyi kurarken kullan.
65. `obs-grafana-loki-explore` — Grafana Explore'da Loki log sorgusu, log context ve live tail kullanımını yaparken kullan.
66. `obs-grafana-tempo-explore` — Grafana Explore'da Tempo trace sorgusu ve service graph kullanımını yaparken kullan.
67. `obs-grafana-prometheus-explore` — Grafana Explore ile PromQL sorgusu ve metric browser kullanımını yaparken kullan.
68. `obs-grafana-slo-panel` — Grafana'da SLO/SLI paneli ve error budget görselleştirmesini tasarlarken kullan.
69. `obs-grafana-heatmap-panel` — Grafana heatmap panel ile histogram dağılımı ve latency band görselleştirmesini yaparken kullan.
70. `obs-grafana-stat-panel` — Grafana stat ve gauge panel konfigürasyonu ve threshold renk kurallarını uygularken kullan.
71. `obs-grafana-table-panel` — Grafana table panel ile transform, field override ve link yapılandırmasını yaparken kullan.
72. `obs-grafana-logs-panel` — Grafana logs panel konfigürasyonu ve label filtresi ayarlarını yaparken kullan.
73. `obs-grafana-trace-panel` — Grafana trace panel ile trace görselleştirmesi ve span detayı yapılandırmasını yaparken kullan.
74. `obs-grafana-api-http` — Grafana HTTP API ile dashboard CRUD, alert ve datasource yönetimini yaparken kullan.
75. `obs-grafana-rbac` — Grafana RBAC ile rol, team ve folder izin yönetimini yaparken kullan.
76. `obs-grafana-plugin-install` — Grafana plugin kurulumu, offline install ve version kilitlemeyi yaparken kullan.
77. `obs-grafana-ai-plugin` — Grafana LLM plugin ile doğal dil sorgulama entegrasyonunu yaparken kullan.
78. `obs-grafana-backup-restore` — Grafana dashboard/datasource backup ve geri yükleme prosedürünü uygularken kullan.
79. `obs-grafana-image-renderer` — Grafana image renderer kurulumu ve dashboard ekran görüntüsü alma özelliğini kurarken kullan.
80. `obs-grafana-juju-relation` — Juju grafana-source relation ile datasource otomatik kaydını kurarken kullan.

### Kategori 5: obs-alertmanager (16 skill)
81. `obs-alertmanager-routing` — Alertmanager route ağacı, matchers ve continue flag yapılandırmasını kurarken kullan.
82. `obs-alertmanager-receivers` — Alertmanager receiver (email, Slack, PagerDuty, webhook) yapılandırmasını kurarken kullan.
83. `obs-alertmanager-inhibit` — Alertmanager inhibit_rules ile gereksiz alert bastırma mantığını kurarken kullan.
84. `obs-alertmanager-silence` — Alertmanager silence oluşturma ve API ile programatik bastırma yaparken kullan.
85. `obs-alertmanager-grouping` — Alert gruplama stratejisi (group_by, wait, interval, repeat) ayarlarken kullan.
86. `obs-alertmanager-high-availability` — Alertmanager HA cluster kurulumu ve duplicate supression yaparken kullan.
87. `obs-alertmanager-api` — Alertmanager v2 API ile alert listeleme ve silence CRUD yaparken kullan.
88. `obs-alertmanager-webhook-integration` — Alertmanager webhook receiver ile özel alert handler entegrasyonunu yaparken kullan.
89. `obs-alertmanager-slack-template` — Alertmanager Slack mesaj template özelleştirmesi ve rich formatting yaparken kullan.
90. `obs-alertmanager-pagerduty` — Alertmanager PagerDuty entegrasyonu ve severity mapping yapılandırmasını kurarken kullan.
91. `obs-alertmanager-opsgenie` — Alertmanager OpsGenie entegrasyonu ve responder mapping yaparken kullan.
92. `obs-alertmanager-alert-lifecycle` — Alert firing→resolved yaşam döngüsü ve flapping önleme kurallarını uygularken kullan.
93. `obs-alertmanager-troubleshoot` — Alertmanager'da bildirim gitmiyor ve route eşleşmiyor sorunlarını teşhis ederken kullan.
94. `obs-alertmanager-juju-relation` — Juju alertmanager relation ile Prometheus→Alertmanager bağlantısını kurarken kullan.
95. `obs-alertmanager-msteams` — Alertmanager Microsoft Teams entegrasyonu ve adaptive card template yaparken kullan.
96. `obs-alertmanager-runbook-url` — Alert runbook URL alanı kullanımı ve otomatik runbook oluşturma akışını kurarken kullan.

### Kategori 6: obs-otel (20 skill)
97. `obs-otel-collector-pipeline` — OTEL Collector receiver/processor/exporter pipeline mimarisini kurarken kullan.
98. `obs-otel-collector-receivers` — OTEL Collector receiver'ları (OTLP, Prometheus, Filelog, Jaeger) yapılandırırken kullan.
99. `obs-otel-collector-processors` — OTEL Collector processor'ları (batch, memory_limiter, attribute, filter) kurarken kullan.
100. `obs-otel-collector-exporters` — OTEL Collector exporter'ları (OTLP, Prometheus, Loki, debug) yapılandırırken kullan.
101. `obs-otel-collector-extensions` — OTEL Collector extension'ları (health_check, pprof, zpages) eklerken kullan.
102. `obs-otel-sdk-python` — Python OTEL SDK ile trace, metric ve log enstrümentasyonunu kurarken kullan.
103. `obs-otel-sdk-auto-instrument` — Python otomatik enstrümantasyon ile sıfır kod değişiklikli izlemeyi kurarken kullan.
104. `obs-otel-semantic-conventions` — OTEL semantic conventions (http, db, rpc, messaging) standartlarını uygularken kullan.
105. `obs-otel-baggage` — OTEL baggage API ile trace bağlamında context propagation yaparken kullan.
106. `obs-otel-context-propagation` — W3C TraceContext ve Baggage header ile servisler arası context propagation kurarken kullan.
107. `obs-otel-exemplars-bridge` — OTEL exemplar ile metrics-traces köprüsünü SDK ve Collector düzeyinde kurarken kullan.
108. `obs-otel-resource-detection` — OTEL resource detector (env, container, k8s, process) ile attribute otomatik tespiti yaparken kullan.
109. `obs-otel-sampling-config` — OTEL Collector tail sampling processor ile kural tabanlı trace örneklemeyi kurarken kullan.
110. `obs-otel-k8s-operator` — OTEL Kubernetes Operator ile CR tabanlı enstrümantasyon ve collector yönetimini yaparken kullan.
111. `obs-otel-filelog-receiver` — OTEL Collector filelog receiver ile log dosyasından Loki'ye pipeline kurarken kullan.
112. `obs-otel-hostmetrics-receiver` — OTEL Collector hostmetrics receiver ile sistem metriklerini toplarken kullan.
113. `obs-otel-k8s-cluster-receiver` — OTEL Collector k8scluster receiver ile Kubernetes cluster metriklerini toplarken kullan.
114. `obs-otel-prometheus-receiver` — OTEL Collector prometheus receiver ile mevcut scrape'leri bridge ederken kullan.
115. `obs-otel-troubleshoot-pipeline` — OTEL Collector pipeline'da telemetri akmıyor sorunlarını teşhis ederken kullan.
116. `obs-otel-collector-scaling` — OTEL Collector yatay ölçekleme ve shard stratejisini yaparken kullan.

### Kategori 7: obs-gateway (12 skill)
117. `obs-gateway-auth-token` — Observability gateway token kimlik doğrulaması ve header doğrulama mantığını kurarken kullan.
118. `obs-gateway-prometheus-adapter` — Gateway Prometheus adapter'ı ve yanıt normalleştirmesini yazarken kullan.
119. `obs-gateway-loki-adapter` — Gateway Loki adapter'ı ve log yanıt formatlamasını yazarken kullan.
120. `obs-gateway-tempo-adapter` — Gateway Tempo adapter'ı ve span detay dönüşümünü yazarken kullan.
121. `obs-gateway-error-model` — Gateway hata modeli ve secret-safe yanıt üretimini kurarken kullan.
122. `obs-gateway-health-status` — Gateway /health ve /api/v1/status endpoint'i ile backend durum özetini dönerken kullan.
123. `obs-gateway-rate-limiting` — Gateway rate limiting ile backend korumasını yaparken kullan.
124. `obs-gateway-retry-timeout` — Gateway backend retry, timeout politikası ve circuit breaker eklerken kullan.
125. `obs-gateway-caching` — Gateway sorgu cache ile tekrarlayan Prometheus/Loki sorgularını önbelleğe alırken kullan.
126. `obs-gateway-multi-backend` — Gateway'e birden fazla backend ekleme ve routing kurallarını yazarken kullan.
127. `obs-gateway-openapi-spec` — Gateway OpenAPI şeması tanımlama ve client üretimini yaparken kullan.
128. `obs-gateway-deployment-k8s` — Observability gateway'i Kubernetes Deployment olarak konuşlandırırken kullan.

### Kategori 8: k8s-core (20 skill)
129. `k8s-core-pod-lifecycle` — Pod yaşam döngüsü ve probe (liveness, readiness, startup) yapılandırmasını yaparken kullan.
130. `k8s-core-deployment-strategy` — Deployment rolling update ve canary stratejisi ile surge/unavailable ayarlarını yaparken kullan.
131. `k8s-core-statefulset` — StatefulSet, sıralı pod yönetimi ve headless service yapılandırmasını kurarken kullan.
132. `k8s-core-daemonset` — DaemonSet ile her node'a servis deploy etme ve tolerasyon kurallarını uygularken kullan.
133. `k8s-core-job-cronjob` — Kubernetes Job ve CronJob ile toplu iş ve zamanlı görev yönetimini kurarken kullan.
134. `k8s-core-configmap-secret` — ConfigMap ve Secret oluşturma, volume mount ve env inject stratejisini uygularken kullan.
135. `k8s-core-namespace` — Namespace oluşturma, ResourceQuota ve LimitRange izolasyon kurallarını uygularken kullan.
136. `k8s-core-rbac` — ClusterRole/Role ve binding ile RBAC politikası tanımlama ve doğrularken kullan.
137. `k8s-core-service-account` — ServiceAccount, token projection ve Pod identity yönetimini kurarken kullan.
138. `k8s-core-labels-annotations` — Label ve annotation stratejisi, selector tutarlılığı ve metadata standartlarını uygularken kullan.
139. `k8s-core-resource-requests-limits` — Pod resource request/limit, QoS class ve OOM riski yönetimini yaparken kullan.
140. `k8s-core-affinity-antiaffinity` — Node/pod affinity ve topologySpreadConstraint ile yerleşim kurallarını kurarken kullan.
141. `k8s-core-taints-tolerations` — Node taint ekleme ve Pod toleration ile özel iş yükü yerleşimini ayarlarken kullan.
142. `k8s-core-init-containers` — Init container kullanımı, bağımlılık beklemesi ve volume hazırlama kalıplarını uygularken kullan.
143. `k8s-core-sidecar-pattern` — Sidecar container deseni, log forwarder ve proxy sidecar ekleme kurallarını uygularken kullan.
144. `k8s-core-pod-disruption-budget` — PodDisruptionBudget ile güncelleme sırasında minimum hazır pod garantisini kurarken kullan.
145. `k8s-core-kustomize` — Kustomize overlay, patch ve base-layer ile ortam bazlı yapılandırma yönetirken kullan.
146. `k8s-core-helm-chart` — Helm chart yazımı, values override ve chart dependency yönetimini uygularken kullan.
147. `k8s-core-events-audit` — Kubernetes event izleme, audit log ve olay tabanlı alarm kurarken kullan.
148. `k8s-core-kubectl-tips` — kubectl plugin, krew, alias ve verimli komut kalıplarıyla operasyonu yaparken kullan.

### Kategori 9: k8s-net (16 skill)
149. `k8s-net-service-types` — ClusterIP, NodePort, LoadBalancer servis tipi seçimi ve yapılandırmasını yaparken kullan.
150. `k8s-net-ingress-controller` — Kubernetes Ingress resource ve controller (Traefik, nginx) kurulumunu yaparken kullan.
151. `k8s-net-gateway-api` — Kubernetes Gateway API (GatewayClass, HTTPRoute) ile gelişmiş trafik yönetimini kurarken kullan.
152. `k8s-net-networkpolicy` — NetworkPolicy ile pod-to-pod ağ izolasyonu ve egress/ingress kısıtlama kurallarını yazarken kullan.
153. `k8s-net-metallb` — MetalLB LoadBalancer IP havuzu yapılandırması ve L2/BGP modu seçimini kurarken kullan.
154. `k8s-net-coredns` — CoreDNS plugin zinciri, custom DNS ve stub zone ayarlarını yapılandırırken kullan.
155. `k8s-net-service-mesh-intro` — Service mesh (Istio, Linkerd) kavramları ve mTLS ile trafik şifrelemesine giriş yaparken kullan.
156. `k8s-net-endpoint-slice` — EndpointSlice yapısı ve büyük servis topluluğunda ölçeklenme kurallarını uygularken kullan.
157. `k8s-net-dns-troubleshoot` — Kubernetes DNS çözümleme sorunlarını (nxdomain, timeout, ndots) teşhis ederken kullan.
158. `k8s-net-egress-control` — Pod egress trafiğini kısıtlama ve egress gateway kullanımını yaparken kullan.
159. `k8s-net-ipv6-dual-stack` — Kubernetes IPv6/dual-stack yapılandırması ve MicroK8s'te etkinleştirme adımlarını uygularken kullan.
160. `k8s-net-traefik-middleware` — Traefik middleware (strip prefix, headers, rate limit) zinciri ve IngressRoute yaparken kullan.
161. `k8s-net-traefik-tls` — Traefik TLS termination, cert-manager entegrasyonu ve wildcard sertifika yönetimini kurarken kullan.
162. `k8s-net-traefik-dashboard` — Traefik dashboard erişimi, güvenlik yapılandırması ve router/service görüntülemeyi yaparken kullan.
163. `k8s-net-pod-cidr` — Pod CIDR ve Service CIDR planlama, overlap önleme ve MicroK8s ağ aralığı ayarlarken kullan.
164. `k8s-net-calico-flannel` — Calico ve Flannel CNI karşılaştırması ve MicroK8s'te CNI değişikliği yaparken kullan.

### Kategori 10: k8s-storage (14 skill)
165. `k8s-storage-pvc-pv` — PersistentVolumeClaim/PV yaşam döngüsü, reclaim policy ve access mode seçimini yaparken kullan.
166. `k8s-storage-storageclass` — StorageClass tanımlama, dynamic provisioner ve volume binding mode seçimini yaparken kullan.
167. `k8s-storage-hostpath` — HostPath volume kullanımı, güvenlik riskleri ve test ortamı kısıtlamalarını uygularken kullan.
168. `k8s-storage-local-pv` — Local PersistentVolume ile yüksek performanslı depolama ve node affinity zorunluluğunu kurarken kullan.
169. `k8s-storage-nfs` — NFS volume mount, NFS provisioner ve performans parametre ayarlarını kurarken kullan.
170. `k8s-storage-volume-snapshot` — VolumeSnapshot ve VolumeSnapshotClass ile anlık görüntü alma ve geri yüklemeyi yaparken kullan.
171. `k8s-storage-resize` — PVC online resize işlemi ve AllowVolumeExpansion StorageClass bayrağını uygularken kullan.
172. `k8s-storage-emptydir` — EmptyDir volume kullanım senaryoları, medium seçimi ve boyut limiti ayarlarken kullan.
173. `k8s-storage-projected-volume` — Projected volume ile ConfigMap/Secret/ServiceAccountToken birleştirmesini kurarken kullan.
174. `k8s-storage-csi-driver` — CSI driver kurulumu, provisioner-attacher bileşenleri ve troubleshoot yaparken kullan.
175. `k8s-storage-rook-ceph-intro` — Rook-Ceph ile k8s-native distributed storage kurulumuna giriş adımlarını yaparken kullan.
176. `k8s-storage-microk8s-hostpath` — MicroK8s hostpath-storage addon'u ve default StorageClass davranışını anlamak için kullan.
177. `k8s-storage-backup-velero` — Velero ile k8s kaynak ve PV yedekleme, schedule ve restore yaparken kullan.
178. `k8s-storage-data-migration` — Bir PVC'den diğerine veri taşıma (rsync, pod mount, snapshot clone) prosedürünü uygularken kullan.

### Kategori 11: k8s-sec (16 skill)
179. `k8s-sec-pod-security-standards` — Kubernetes Pod Security Standards ve namespace admission etiketlerini uygularken kullan.
180. `k8s-sec-admission-webhooks` — ValidatingAdmissionWebhook ve MutatingAdmissionWebhook ile politika uygularken kullan.
181. `k8s-sec-opa-gatekeeper` — OPA Gatekeeper constraint template ile küme güvenlik politikası kurarken kullan.
182. `k8s-sec-network-policies-defense` — Default-deny NetworkPolicy katmanını tasarlarken kullan.
183. `k8s-sec-secrets-management` — Kubernetes Secret şifreleme, External Secrets Operator ve vault entegrasyonunu kurarken kullan.
184. `k8s-sec-image-scanning` — Container image güvenlik taraması (Trivy) CI entegrasyonu ve politika kapısını kurarken kullan.
185. `k8s-sec-supply-chain` — Container image imzalama (cosign), SBOM üretimi ve doğrulama zincirini kurarken kullan.
186. `k8s-sec-audit-logging` — Kubernetes API audit log yapılandırması, policy düzeyleri ve SIEM entegrasyonunu kurarken kullan.
187. `k8s-sec-runtime-security` — Falco ile runtime tehdit tespiti, kural yazımı ve alert entegrasyonunu kurarken kullan.
188. `k8s-sec-tls-cert-manager` — cert-manager ile otomatik TLS sertifika yönetimi, Let's Encrypt ve self-signed CA kurarken kullan.
189. `k8s-sec-workload-identity` — Workload identity ile cloud kimlik doğrulamasını kurarken kullan.
190. `k8s-sec-seccomp-apparmor` — Seccomp profili ve AppArmor annotation ile pod sistem çağrısı kısıtlamasını uygularken kullan.
191. `k8s-sec-read-only-filesystem` — Container readOnlyRootFilesystem ve security context kurallarını uygularken kullan.
192. `k8s-sec-rbac-least-privilege` — RBAC en az ayrıcalık ilkesine göre rol tasarımı ve permission audit yaparken kullan.
193. `k8s-sec-network-encryption-mtls` — Pod-to-pod mTLS ve Linkerd/Istio ile şifreli servis iletişimi kurarken kullan.
194. `k8s-sec-cve-patching` — CVE izleme, node image güncelleme ve draining ile sıfır kesinti yama prosedürünü uygularken kullan.

### Kategori 12: k8s-scale (12 skill)
195. `k8s-scale-hpa` — Horizontal Pod Autoscaler, CPU/memory ve custom metric tabanlı ölçekleme kurarken kullan.
196. `k8s-scale-vpa` — Vertical Pod Autoscaler ile otomatik resource request öneri yapılandırmasını kurarken kullan.
197. `k8s-scale-keda` — KEDA ile event-driven autoscaling (Kafka, Redis, Prometheus metric) kurarken kullan.
198. `k8s-scale-cluster-autoscaler` — Cluster Autoscaler ile node havuzu büyütme/küçültme ve maliyet optimizasyonunu kurarken kullan.
199. `k8s-scale-resource-quotas` — ResourceQuota ve LimitRange ile namespace bazlı kaynak tavan politikasını uygularken kullan.
200. `k8s-scale-node-affinity-spread` — TopologySpreadConstraint ile pod'ları node/zone'lara eşit dağıtma kurallarını kurarken kullan.
201. `k8s-scale-load-testing` — k8s üzerinde yük testi (Locust, k6) çalıştırma ve HPA tetikleme doğrulamasını yaparken kullan.
202. `k8s-scale-custom-metrics-api` — custom.metrics.k8s.io ile Prometheus adapter ve HPA custom metric entegrasyonunu kurarken kullan.
203. `k8s-scale-pod-preemption` — Kubernetes pod preemption, priority class tanımı ve kaynak geri kazanımını uygularken kullan.
204. `k8s-scale-warm-pool` — Node warm pool ve pre-scaling stratejisi ile soğuk başlatma gecikmesini azaltırken kullan.
205. `k8s-scale-microk8s-node-add` — MicroK8s çok-node cluster kurulumu ve node ekleme prosedürünü uygularken kullan.
206. `k8s-scale-capacity-forecast` — Tarihsel metrik tabanlı kapasite tahmini ve büyüme projeksiyonu yaparken kullan.

### Kategori 13: microk8s (16 skill)
207. `microk8s-install-snap` — MicroK8s snap kurulumu, kanal seçimi ve kullanıcı grup yapılandırmasını yaparken kullan.
208. `microk8s-addons-overview` — MicroK8s addon sistemi, mevcut katalog ve etkinleştirme sırasını anlamak için kullan.
209. `microk8s-addon-registry` — MicroK8s yerel container registry addon'u kurulumu ve push/pull kullanımını yaparken kullan.
210. `microk8s-addon-ingress` — MicroK8s ingress addon'u, nginx controller ve IngressClass yapılandırmasını kurarken kullan.
211. `microk8s-addon-metallb` — MicroK8s MetalLB addon'u, IP aralığı tanımlama ve yeniden yapılandırmayı yaparken kullan.
212. `microk8s-addon-gpu` — MicroK8s GPU addon'u, nvidia device plugin ve GPU pod talebi yapılandırmasını kurarken kullan.
213. `microk8s-addon-observability` — MicroK8s observability addon'u ile dahili Grafana/Prometheus/Loki stack kurarken kullan.
214. `microk8s-kubeconfig-export` — MicroK8s kubeconfig dışa aktarma, merge ve kubectl context yönetimini yaparken kullan.
215. `microk8s-upgrade` — MicroK8s sürüm yükseltme, kanal değiştirme ve geri alma prosedürünü uygularken kullan.
216. `microk8s-ha-cluster` — MicroK8s HA cluster, dqlite ve 3-node quorum yapılandırmasını kurarken kullan.
217. `microk8s-offline-install` — İnternet bağlantısı olmayan ortamda MicroK8s ve image pre-load kurulumunu yaparken kullan.
218. `microk8s-snap-refresh-hold` — MicroK8s snap otomatik güncelleme kilitleme ve kontrollü güncelleme planlamasını yaparken kullan.
219. `microk8s-ip-change-recovery` — Host IP değişince kubeconfig, API server SAN ve Juju drift onarım prosedürünü uygularken kullan.
220. `microk8s-inspect` — microk8s inspect komutuyla hata raporu ve destek paketi oluşturma adımlarını yaparken kullan.
221. `microk8s-container-runtime` — MicroK8s containerd yapılandırması, mirror kayıt ve runtime snapshot ayarlarını yaparken kullan.
222. `microk8s-troubleshoot-api` — MicroK8s API server erişim sorunları, sertifika hatası ve port çakışması teşhisini yaparken kullan.

### Kategori 14: juju (20 skill)
223. `juju-bootstrap-cloud` — Juju bootstrap farklı cloud (aws, gce, localhost) için yapılandırma ve credential yönetimini yaparken kullan.
224. `juju-model-lifecycle` — Juju model oluşturma, silme ve model bazlı kaynak izolasyonunu yönetirken kullan.
225. `juju-charm-deploy` — Juju charm deploy, channel seçimi, revision sabitleme ve config enjeksiyonunu yaparken kullan.
226. `juju-relation-add-remove` — Juju relation ekleme/kaldırma ve relation data inceleme adımlarını uygularken kullan.
227. `juju-config-management` — Juju application config güncelleme ve YAML dosyasıyla toplu yapılandırma yaparken kullan.
228. `juju-actions` — Juju action çalıştırma, parametre geçirme ve sonuç izleme adımlarını uygularken kullan.
229. `juju-secrets-management` — Juju secrets ile charm'lara güvenli credential dağıtımını yaparken kullan.
230. `juju-resources` — Juju resource ekleme, güncelleme ve charm container image override yapılandırmasını kurarken kullan.
231. `juju-debug-log` — juju debug-log ile log filtreleme ve sorun giderme adımlarını uygularken kullan.
232. `juju-ssh-debug` — juju ssh ve juju debug-hooks ile charm birim içinde hata ayıklama yaparken kullan.
233. `juju-status-parsing` — juju status JSON çıktısı ayrıştırma ve otomasyon scriptlerinde kullanım kalıplarını uygularken kullan.
234. `juju-bundle-deploy` — Juju bundle YAML ile çok-uygulama deployment ve relation tanımlamasını yaparken kullan.
235. `juju-machine-management` — Juju machine ekleme, kaldırma ve constraint ile donanım gereksinim belirlemeyi yaparken kullan.
236. `juju-upgrade-charm` — Juju charm yükseltme, revision geçiş stratejisi ve geri alma prosedürünü uygularken kullan.
237. `juju-spaces-bindings` — Juju network space ve endpoint binding ile ağ izolasyonu yapılandırmasını kurarken kullan.
238. `juju-storage-charm` — Juju storage directive ile charm depolama talebi ve StorageClass entegrasyonunu kurarken kullan.
239. `juju-cross-model-relations` — Juju cross-model relation ile farklı model arası entegrasyonu kurarken kullan.
240. `juju-controller-backup` — Juju controller yedekleme, geri yükleme prosedürü ve DR senaryosunu uygularken kullan.
241. `juju-troubleshoot-blocked` — Juju "blocked" application durumu teşhisi ve hook hatası gidermeyi yaparken kullan.
242. `juju-terraform-provider` — Juju Terraform provider ile infrastructure-as-code charm yönetimini kurarken kullan.

### Kategori 15: cos (16 skill)
243. `cos-bundle-overview` — COS Lite Juju bundle içeriği, bileşen rolleri ve relation ağını anlayarak deploy yaparken kullan.
244. `cos-deploy-tempo` — Juju ile Tempo charm deploy, OTEL Collector relation ve ingress yapılandırmasını kurarken kullan.
245. `cos-deploy-otel-collector` — Juju ile OTEL Collector charm deploy ve telemetry routing yapılandırmasını kurarken kullan.
246. `cos-deploy-catalogue` — Juju catalogue charm ile servis keşif URL'lerini ve Grafana menü entegrasyonunu kurarken kullan.
247. `cos-relation-loki-alertmanager` — Loki→Alertmanager ruler alerting relation kurulumunu ve doğrulama adımlarını uygularken kullan.
248. `cos-relation-tempo-grafana` — Tempo→Grafana datasource relation ve trace görselleştirmesini etkinleştirirken kullan.
249. `cos-relation-otel-prometheus` — OTEL Collector→Prometheus scrape relation ve metric akışını doğrularken kullan.
250. `cos-ingress-troubleshoot` — COS Traefik ingress URL erişim sorunlarını teşhis ederken kullan.
251. `cos-upgrade-strategy` — COS Lite bileşenlerini sıralı güncelleme stratejisi ile kesintisiz yükseltmeyi uygularken kullan.
252. `cos-backup-strategy` — COS bileşenleri veri yedekleme stratejisini kurarken kullan.
253. `cos-multi-model` — COS'u ayrı Juju modeline deploy edip cross-model relation ile uygulama modellerine bağlarken kullan.
254. `cos-ha-topology` — COS bileşenlerinin yüksek erişilebilirlik topolojisi ve replica sayısı yapılandırmasını kurarken kullan.
255. `cos-resource-sizing` — COS bileşenleri için CPU/memory/disk boyutlandırma kılavuzunu uygularken kullan.
256. `cos-security-hardening` — COS stack'e TLS, auth ve NetworkPolicy katmanı ekleyerek güvenlik sertleştirmesi yaparken kullan.
257. `cos-observability-self-monitoring` — COS bileşenlerinin kendi kendini izlemesi (self-monitoring dashboard, alert) kurarken kullan.
258. `cos-custom-charm-relation` — Özel FastAPI uygulamasını COS'a bağlamak için observability relation eklerken kullan.

### Kategori 16: llm-anthropic (18 skill)
259. `llm-anthropic-messages-api` — Anthropic Messages API istek/yanıt yapısı ve content block formatını kullanırken kullan.
260. `llm-anthropic-tool-use` — Anthropic tool_use block, tool_result döngüsü ve paralel tool çağrısı mekanizmasını kurarken kullan.
261. `llm-anthropic-streaming` — Anthropic streaming SSE events ayrıştırma ve işlemeyi yazarken kullan.
262. `llm-anthropic-extended-thinking` — Anthropic extended thinking etkinleştirme, bütçe ayarı ve çıktı işlemeyi yaparken kullan.
263. `llm-anthropic-prompt-caching` — Anthropic prompt caching ile token maliyet optimizasyonunu kurarken kullan.
264. `llm-anthropic-computer-use` — Anthropic computer use (screenshot, mouse, keyboard tool) entegrasyonunu uygularken kullan.
265. `llm-anthropic-batch-api` — Anthropic Message Batches API ile toplu istek gönderme ve sonuç almayı yaparken kullan.
266. `llm-anthropic-file-api` — Anthropic Files API ile dosya yükleme, referans ve PDF işlemeyi entegre ederken kullan.
267. `llm-anthropic-vision` — Anthropic vision (image content block) ile görüntü analizi entegrasyonunu kurarken kullan.
268. `llm-anthropic-model-selection` — Claude model ailesi (Opus, Sonnet, Haiku) ve doğru model seçim kriterlerini uygularken kullan.
269. `llm-anthropic-rate-limits` — Anthropic rate limit (RPM, TPM) yönetimi ve exponential backoff kodlamasını yaparken kullan.
270. `llm-anthropic-error-handling` — Anthropic API hata kodları ve retry/fallback akışını yazarken kullan.
271. `llm-anthropic-system-prompt` — Anthropic system prompt tasarımı, persona tanımlama ve kısıtlama kurallarını yazarken kullan.
272. `llm-anthropic-token-counting` — Anthropic token sayma API ile maliyet tahmini ve context window yönetimini yaparken kullan.
273. `llm-anthropic-sdk-python` — Anthropic Python SDK kurulumu, async kullanımı ve best practice kalıplarını uygularken kullan.
274. `llm-anthropic-sdk-typescript` — Anthropic TypeScript SDK kurulumu ve streaming kullanımını uygularken kullan.
275. `llm-anthropic-admin-api` — Anthropic Admin API ile API key ve organization yönetimini yaparken kullan.
276. `llm-anthropic-migrating-versions` — Eski Claude model sürümünden yenisine migration ve davranış farkı geçişini yaparken kullan.

### Kategori 17: llm-openai (14 skill)
277. `llm-openai-chat-completion` — OpenAI Chat Completions API istek/yanıt yapısı ve temel kullanımını kodlarken kullan.
278. `llm-openai-function-calling` — OpenAI function calling (tools array) ve tool_choice parametresi kullanımını kodlarken kullan.
279. `llm-openai-streaming-sse` — OpenAI streaming SSE delta ayrıştırma ve chunk birleştirme mantığını yazarken kullan.
280. `llm-openai-embeddings` — OpenAI embeddings API ile vektör üretimi ve RAG pipeline kurarken kullan.
281. `llm-openai-responses-api` — OpenAI Responses API ile built-in tool ve session yönetimini kurarken kullan.
282. `llm-openai-compatible-server` — vLLM, LiteLLM, Ollama gibi OpenAI-compatible server kurulumu ve Sentinel entegrasyonunu yaparken kullan.
283. `llm-openai-rate-limit-retry` — OpenAI 429 rate limit ve retry-after header yönetimini yazarken kullan.
284. `llm-openai-structured-output` — OpenAI structured output ile garantili JSON yanıt alma kurallarını yazarken kullan.
285. `llm-openai-vision` — OpenAI vision (image_url content) ile görüntü analizi entegrasyonunu yazarken kullan.
286. `llm-openai-audio` — OpenAI Whisper (transcription) ve TTS API ile ses-metin dönüşümünü kurarken kullan.
287. `llm-openai-realtime-api` — OpenAI Realtime API (WebSocket) ile düşük gecikmeli ses asistanı kurarken kullan.
288. `llm-openai-fine-tuning` — OpenAI fine-tuning job oluşturma, dataset formatı ve model değerlendirme adımlarını uygularken kullan.
289. `llm-openai-assistants-api` — OpenAI Assistants API, Thread, Run ve code interpreter entegrasyonunu kurarken kullan.
290. `llm-openai-moderation` — OpenAI moderation API ile içerik güvenlik filtresi ve politika uygulamasını kurarken kullan.

### Kategori 18: llm-local (14 skill)
291. `llm-local-ollama-setup` — Ollama kurulumu, model pull, GPU/CPU çalıştırma ve API endpoint yapılandırmasını yaparken kullan.
292. `llm-local-ollama-modelfile` — Ollama Modelfile ile özel sistem promptu ve model türetmesini yazarken kullan.
293. `llm-local-ollama-openai-compat` — Ollama OpenAI-compatible endpoint ile Sentinel entegrasyonunu yaparken kullan.
294. `llm-local-vllm-setup` — vLLM sunucu kurulumu, GPU bellek ayarı ve OpenAI-compat API açma adımlarını yaparken kullan.
295. `llm-local-llama-cpp` — llama.cpp ile CPU/GPU çıkarım, GGUF model yükleme ve parametre ayarını yaparken kullan.
296. `llm-local-quantization` — GGUF/AWQ/GPTQ model niceleme formatları ve bit derinliği seçimini anlarken kullan.
297. `llm-local-gpu-memory` — GPU VRAM tahmini, model boyutu hesaplama ve çoklu GPU sharding stratejisini uygularken kullan.
298. `llm-local-context-length` — Yerel model context uzunluğu sınırı ve uzun bağlam stratejisini seçerken kullan.
299. `llm-local-benchmark` — Yerel model çıkarım hızı (tokens/s) ve doğruluk değerlendirmesini yaparken kullan.
300. `llm-local-model-registry` — Yerel model deposu yönetimi, model versioning ve ekip paylaşım stratejisini uygularken kullan.
301. `llm-local-lm-studio` — LM Studio ile GUI tabanlı yerel model çalıştırma ve OpenAI-compat server kullanımını yaparken kullan.
302. `llm-local-air-gap-deploy` — İnternetsiz ortamda yerel LLM deploy ve model transfer kurarken kullan.
303. `llm-local-multi-modal` — Yerel multimodal model (LLaVA, Gemma3) ile görüntü+metin çıkarım entegrasyonunu kurarken kullan.
304. `llm-local-gemma` — Google Gemma model ailesi, Ollama ile çalıştırma ve Sentinel profil geçişini yaparken kullan.

### Kategori 19: llm-prompt (18 skill)
305. `llm-prompt-system-design` — Sistem promptu yapısı, persona, kısıtlama ve çıktı formatı bölümlerini tasarlarken kullan.
306. `llm-prompt-chain-of-thought` — Adım adım düşünme prompting tekniği ve karmaşık görev çözüm kalıbını yazarken kullan.
307. `llm-prompt-few-shot` — Az-örnek prompting, örnek seçimi ve formatı ile LLM davranışı yönlendirirken kullan.
308. `llm-prompt-zero-shot` — Sıfır-örnek prompting ile doğrudan görev tanımı yazımını yaparken kullan.
309. `llm-prompt-react-pattern` — ReAct (Reason+Act) deseni ile araç çağrısı ve gözlem döngüsünü kurarken kullan.
310. `llm-prompt-tool-descriptions` — Agent araç açıklama ve parametre schema yazımı ile LLM araç seçim kalitesini artırırken kullan.
311. `llm-prompt-output-format` — JSON, XML, Markdown çıktı formatı zorlama ve güvenli ayrıştırmayı sağlarken kullan.
312. `llm-prompt-injection-defense` — Kullanıcı girdisindeki prompt injection girişimlerini tespit ve savunma kalıplarını uygularken kullan.
313. `llm-prompt-temperature-params` — Temperature, top-p, top-k parametrelerinin çıktı çeşitliliğine etkisini ayarlarken kullan.
314. `llm-prompt-context-stuffing` — Context window'a belge ve veri doldurma stratejisi ve önceliklendirme kurallarını uygularken kullan.
315. `llm-prompt-persona-roleplay` — LLM'e uzman persona ve rol tanımı vererek domain-specific yanıt kalitesini artırırken kullan.
316. `llm-prompt-critique-revision` — LLM çıktısını aynı veya başka LLM'e eleştirtip revizyona tabi tutma pipeline'ını kurarken kullan.
317. `llm-prompt-classification` — Metin sınıflandırma görevi için prompt tasarımı ve label listesi yazımını yaparken kullan.
318. `llm-prompt-extraction` — Yapılandırılmamış metinden alan çıkarımı için prompt ve şema tasarımını yaparken kullan.
319. `llm-prompt-summarization` — Uzun belge özetleme (map-reduce, recursive) prompt stratejisini uygularken kullan.
320. `llm-prompt-code-generation` — Kod üretimi prompt tasarımı ve güvenlik kısıtlama kurallarını yazarken kullan.
321. `llm-prompt-agentic-planning` — LLM'den plan ve alt görev listesi üretme prompt kalıbını yazarken kullan.
322. `llm-prompt-multilingual` — Çok dilli prompt tasarımı, dil tespiti ve yanıt dili yönlendirme stratejisini yazarken kullan.

### Kategori 20: llm-context (12 skill)
323. `llm-context-window-management` — Context window dolduğunda öncelik sırası ve rolling buffer stratejisini uygularken kullan.
324. `llm-context-rag-pipeline` — RAG pipeline adımları (embed, index, retrieve, augment, generate) ve entegrasyon noktalarını kurarken kullan.
325. `llm-context-vector-store` — Vector store seçimi (ChromaDB, pgvector, Qdrant) ve koleksiyon yönetimini yaparken kullan.
326. `llm-context-chunking-strategy` — Belge parçalama stratejisi, boyut seçimi ve overlap kurallarını uygularken kullan.
327. `llm-context-reranking` — RAG'de cross-encoder reranking ile alaka doğruluğunu artırırken kullan.
328. `llm-context-hybrid-search` — Vektör arama ve BM25 keyword arama hibrit kombinasyonunu kurarken kullan.
329. `llm-context-semantic-compaction` — Sentinel semantic compaction ve session bellek kalıcılığını yönetirken kullan.
330. `llm-context-conversation-history` — Konuşma geçmişi yönetimi, mesaj kısaltma ve bellek önceden yükleme stratejisini kurarken kullan.
331. `llm-context-long-doc-processing` — 100K+ token belge işleme ve bilgi agregasyon kalıplarını uygularken kullan.
332. `llm-context-knowledge-graph` — Bilgi grafiği ile LLM hafızasını zenginleştirme ve yapılandırılmış bağlam sorgulamayı yaparken kullan.
333. `llm-context-cache-hit-strategy` — Prompt cache hit oranını artırmak için sabit prefix tasarımı ve payload sıralama kurallarını uygularken kullan.
334. `llm-context-dynamic-injection` — Çalışma zamanında bağlam enjeksiyonu (live data, user profile, tool result) stratejisini kurarken kullan.

### Kategori 21: llm-eval (12 skill)
335. `llm-eval-benchmark-design` — LLM değerlendirme benchmark tasarımı, test seti oluşturma ve metrik seçimini yaparken kullan.
336. `llm-eval-llm-as-judge` — LLM-as-judge değerlendirme deseni, puanlama rubrik yazımı ve yanlılık azaltmayı kurarken kullan.
337. `llm-eval-ragas` — RAGAS framework ile RAG pipeline değerlendirmesi yapılandırmasını yaparken kullan.
338. `llm-eval-human-annotation` — İnsan değerlendirmesi için annotation kılavuzu ve kalite kontrol adımlarını yaparken kullan.
339. `llm-eval-regression-test` — LLM çıktısı regresyon testi, golden dataset ve CI pipeline entegrasyonunu kurarken kullan.
340. `llm-eval-latency-cost` — LLM yanıt gecikmesi, token maliyeti ve throughput ölçümü ile optimizasyon kararını desteklerken kullan.
341. `llm-eval-hallucination-detect` — Hallüsinasyon tespiti, kaynak doğrulama ve çelişki kontrolü kalıplarını uygularken kullan.
342. `llm-eval-safety-red-team` — LLM güvenlik red-teaming, jailbreak test senaryoları ve güvenlik politikası doğrulamasını yaparken kullan.
343. `llm-eval-tool-call-accuracy` — Agent araç çağrısı doğruluğu, parametre hata analizi ve başarı metriği tanımını yaparken kullan.
344. `llm-eval-multi-turn` — Çok turlu konuşma değerlendirmesi, tutarlılık ölçümü ve konu kayması tespitini yaparken kullan.
345. `llm-eval-a-b-testing` — İki LLM veya prompt versiyonunu A/B test ile karşılaştırma ve istatistiksel anlamlılığı değerlendirirken kullan.
346. `llm-eval-domain-specific` — Domain-spesifik (observability, k8s) LLM değerlendirme seti oluşturma ve metrik tanımını kurarken kullan.

### Kategori 22: agentic-memory (16 skill)
347. `agentic-memory-extract-pipeline` — Sentinel tur sonu bellek çıkarma pipeline'ının tetikleme koşulları ve çıktı formatını uygularken kullan.
348. `agentic-memory-dreaming` — Sentinel dreaming: LLM ile index.md otomatik güncelleme, eşik koşulları ve dosya kilidi yönetimini kurarken kullan.
349. `agentic-memory-magic-docs` — Sentinel magic docs: MAGIC DOC başlıklı Markdown dosyaları güncelleme mekanizmasını kurarken kullan.
350. `agentic-memory-away-summary` — Sentinel away özeti: oturum aralarında son tur özetini saklama ve yükleme akışını kurarken kullan.
351. `agentic-memory-redaction` — Sentinel secrets redaksiyon: API key, JWT, PEM, kubeconfig kimlik bilgilerini temizleme kurallarını uygularken kullan.
352. `agentic-memory-policy-project` — Sentinel proje belleği (policy:project) dizin yapısı ve yazma kurallarını kurarken kullan.
353. `agentic-memory-policy-user` — Sentinel kullanıcı belleği (policy:user) cwd hash ile kullanıcı dizini yönetimini kurarken kullan.
354. `agentic-memory-write-jail` — enforce_write_jail ile write_file aracını yalnızca bellek köküne kısıtlama kurallarını uygularken kullan.
355. `agentic-memory-index-schema` — Sentinel bellek index.md şeması ve LLM ile güncelleme formatını tasarlarken kullan.
356. `agentic-memory-search` — Bellek deposunda anahtar kelime ve anlam tabanlı arama araçları ile geçmiş oturum bilgisine erişirken kullan.
357. `agentic-memory-ttl-cleanup` — Bellek extract girdileri için TTL politikası, eski kayıt temizleme ve disk kullanım sınırını uygularken kullan.
358. `agentic-memory-cross-session` — Farklı oturumlar arası bellek transferi ve proje hafıza sürekliliği stratejisini kurarken kullan.
359. `agentic-memory-encryption` — Bellek dosyalarını şifreleme, anahtar yönetimi ve decrypt açma akışını kurarken kullan.
360. `agentic-memory-migration` — Bellek formatı değişikliğinde eski extract.jsonl kayıtlarını yeni şemaya geçirme prosedürünü uygularken kullan.
361. `agentic-memory-non-interactive` — allow_non_interactive=false: pipe/bare modunda bellek yazma devre dışı kuralını uygularken kullan.
362. `agentic-memory-background-thread` — turn_pipeline run_in_background ile tur sonu pipeline'ını arka plan thread'inde çalıştırma kurallarını uygularken kullan.

### Kategori 23: agentic-sec (14 skill)
363. `agentic-sec-bash-readonly` — bash_read_only modu: güvenli komut allowlist ve pipe/redirect engelleme kurallarını uygularken kullan.
364. `agentic-sec-tool-isolation` — Agent aracı izolasyonu, sandbox ortam değişkenleri ve işlem ağacı kısıtlama stratejisini kurarken kullan.
365. `agentic-sec-output-sanitization` — Agent çıktı sanitizasyonu, terminal escape filtresi ve JSON injection temizleme kurallarını uygularken kullan.
366. `agentic-sec-credential-rotation` — Agent tarafından kullanılan API key/token rotasyon stratejisi ve sıfır-kesinti yenileme akışını kurarken kullan.
367. `agentic-sec-audit-trail` — Agent eylem audit trail kaydı, imzalama ve değiştirilemez log saklama kurallarını uygularken kullan.
368. `agentic-sec-jailbreak-resistance` — Kullanıcı mesajındaki jailbreak ve role injection denemelerine karşı sistem prompt korumasını kurarken kullan.
369. `agentic-sec-data-exfiltration` — Agent'ın hassas veriyi dışarı çıkarmasını önleyen çıktı kontrol ve ağ kısıtlama kurallarını uygularken kullan.
370. `agentic-sec-dependency-audit` — CLI bağımlılıklarında güvenlik açığı taraması (pip-audit) ve CI kapısı eklemeyi yaparken kullan.
371. `agentic-sec-rate-limit-self` — Agent kendi kendine rate limit: LLM ve API çağrısı hız sınırı ve backoff kurallarını uygularken kullan.
372. `agentic-sec-env-var-handling` — Agent ortam değişkeni güvenli okuma, .env maskeleme ve log'a sızdırmama kurallarını uygularken kullan.
373. `agentic-sec-webhook-signature` — Agent webhook alıcısında HMAC imza doğrulaması ve replay saldırı önleme kurallarını uygularken kullan.
374. `agentic-sec-container-sandbox` — Agent'ı container sandbox (gVisor) içinde çalıştırma ve kısıtlama yapılandırmasını kurarken kullan.
375. `agentic-sec-input-validation` — Kullanıcı CLI girdisi doğrulama, uzunluk sınırı ve özel karakter engelleme kurallarını uygularken kullan.
376. `agentic-sec-llm-output-trust` — LLM çıktısına körü körüne güvenmeme, araç argümanı doğrulama ve hasar sınırlama kurallarını uygularken kullan.

### Kategori 24: agentic-cli (16 skill)
377. `agentic-cli-autocomplete` — CLI komut ve flag tamamlama (bash/zsh/fish completion script) üretme ve kurulum adımlarını yaparken kullan.
378. `agentic-cli-output-formats` — CLI çıktı formatı seçenekleri (JSON, table, plain) ve --format flag implementasyonunu kurarken kullan.
379. `agentic-cli-progress-display` — CLI uzun işlemlerde rich progress bar, spinner ve ETA gösterimi ekleme kurallarını uygularken kullan.
380. `agentic-cli-pager-integration` — CLI uzun çıktı için less/more pager entegrasyonu ve TTY algılama kurallarını uygularken kullan.
381. `agentic-cli-stdin-pipe` — CLI stdin okuma, pipe zincirinde kullanım ve TTY olmayan ortam tespitini uygularken kullan.
382. `agentic-cli-interactive-prompts` — CLI interaktif soru sorma ve fallback --yes flag stratejisini kurarken kullan.
383. `agentic-cli-plugin-system` — CLI plugin/extension sistemi, entry point keşfi ve plugin izolasyonu kurallarını uygularken kullan.
384. `agentic-cli-update-mechanism` — CLI sürüm güncelleme kontrolü, self-update akışı ve güvenli indirme doğrulamasını kurarken kullan.
385. `agentic-cli-crash-report` — CLI beklenmedik hata raporlama, stack trace gizleme ve destek bilgisi kurallarını uygularken kullan.
386. `agentic-cli-multi-workspace` — CLI çok çalışma alanı (workspace) desteği, profil bazlı config ve context switching kurallarını kurarken kullan.
387. `agentic-cli-alias-command` — CLI komut alias tanımlama ve config'den okuma kurallarını uygularken kullan.
388. `agentic-cli-dry-run` — CLI --dry-run flag ile değişiklik önizleme ve gerçek uygulama farkını gösterme kurallarını uygularken kullan.
389. `agentic-cli-i18n` — CLI çok dil desteği (i18n), mesaj kataloğu ve locale algılama kurallarını uygularken kullan.
390. `agentic-cli-accessibility` — CLI erişilebilirlik: renk körlüğü dostu çıktı, --no-color flag ve screen reader uyumu kurallarını uygularken kullan.
391. `agentic-cli-shell-integration` — CLI shell entegrasyon hook'ları ve ortam yükleme kolaylıkları kurarken kullan.
392. `agentic-cli-config-validation` — Başlangıçta sentinel.yaml doğrulama, hata mesajı ve migration ipucu verme kurallarını uygularken kullan.

### Kategori 25: agentic-mcp (14 skill)
393. `agentic-mcp-server-authoring` — MCP server yazımı, tool/resource/prompt tanımlama ve stdio/SSE transport kurallarını uygularken kullan.
394. `agentic-mcp-tool-schema` — MCP tool inputSchema JSON Schema tasarımı ve description kalite kurallarını yazarken kullan.
395. `agentic-mcp-resource-endpoints` — MCP resource URI şeması, MIME type ve içerik üretme kurallarını uygularken kullan.
396. `agentic-mcp-prompt-templates` — MCP prompt template tanımlama, argüman schema ve LLM-ready mesaj üretimi kurallarını yazarken kullan.
397. `agentic-mcp-sampling` — MCP sampling request ile server'dan LLM tamamlama talep etme ve onay akışını kurarken kullan.
398. `agentic-mcp-roots` — MCP roots ile server'a izin verilen dizin kümesini bildirme ve güvenli dosya erişimi kurallarını uygularken kullan.
399. `agentic-mcp-sse-transport` — MCP HTTP+SSE transport kurulumu ve endpoint yapılandırmasını kurarken kullan.
400. `agentic-mcp-auth` — MCP server kimlik doğrulaması (OAuth 2.1, bearer token) ve credential yönetimini kurarken kullan.
401. `agentic-mcp-versioning` — MCP protocol versiyon müzakeresi ve geriye dönük uyumluluk kurallarını uygularken kullan.
402. `agentic-mcp-error-codes` — MCP JSON-RPC hata kodu standartları ve istemci hata işleme kurallarını yazarken kullan.
403. `agentic-mcp-testing` — MCP server birim ve entegrasyon testi, mock transport ve golden case kurallarını uygularken kullan.
404. `agentic-mcp-observability-server` — Sentinel observability araçlarını MCP server olarak sunma ve CLI entegrasyonunu kurarken kullan.
405. `agentic-mcp-github-integration` — GitHub MCP server araçları ile issue/PR/code entegrasyonunu Sentinel agent'a bağlarken kullan.
406. `agentic-mcp-local-filesystem` — MCP filesystem server ile güvenli dosya okuma/yazma araç seti ve jail kurallarını uygularken kullan.

### Kategori 26: test (20 skill)
407. `test-unit-fastapi` — FastAPI endpoint birim testi (httpx.AsyncClient, pytest-asyncio) ve dependency override kurallarını yazarken kullan.
408. `test-unit-pydantic` — Pydantic model doğrulama birim testi ve field validator test kalıplarını yazarken kullan.
409. `test-integration-docker-compose` — Docker Compose ile servis bağımlılıkları içeren entegrasyon testi kurarken kullan.
410. `test-integration-real-backend` — Gerçek Prometheus/Loki/Tempo backend'e karşı entegrasyon testi yazma ve CI'da atlama koşulunu kurarken kullan.
411. `test-e2e-cli` — Sentinel CLI'yı subprocess olarak çağırarak uçtan uca senaryo testi yazma kurallarını uygularken kullan.
412. `test-load-locust` — Locust ile HTTP servis yük testi, task ağırlığı ve stage tanımı kurallarını yazarken kullan.
413. `test-load-k6` — k6 ile JavaScript tabanlı yük testi, threshold ve check kurallarını yazarken kullan.
414. `test-chaos-basic` — Chaos Engineering temel kavramları, deney tasarımı ve steady-state hipotez tanımını uygularken kullan.
415. `test-contract-pact` — Pact ile consumer-driven contract testi, pact file üretimi ve provider doğrulamasını kurarken kullan.
416. `test-snapshot` — Pytest snapshot testi (syrupy) ile CLI/API çıktı regresyon tespitini kurarken kullan.
417. `test-mutation` — Muttest/mutmut ile mutasyon testi ve test suite kalite ölçümünü kurarken kullan.
418. `test-property-based` — Hypothesis ile property-based testing, strategy seçimi ve shrinking davranışını yazarken kullan.
419. `test-benchmark-pytest` — pytest-benchmark ile Python fonksiyon performans testi ve regresyon eşiği kurarken kullan.
420. `test-mock-llm` — LLM API'yi mock'layan test fixture'ı ve deterministik yanıt üretimini kurarken kullan.
421. `test-mock-http` — respx/responses ile HTTP çağrı mock'lama ve request assertion kurallarını yazarken kullan.
422. `test-golden-dataset` — LLM agent için golden dataset oluşturma, güncelleme politikası ve CI değerlendirme entegrasyonunu kurarken kullan.
423. `test-coverage-reporting` — pytest-cov ile coverage raporu, minimum eşik ve CI kapısı kurallarını uygularken kullan.
424. `test-matrix-tox` — tox ile çoklu Python sürümü test matrisi ve CI entegrasyonunu kurarken kullan.
425. `test-fixtures-factory` — pytest fixture factory (factory_boy) ile test verisi üretim kalıplarını yazarken kullan.
426. `test-api-fuzzing` — HTTP API fuzzing (schemathesis) ile otomatik kenar durum testi ve CI entegrasyonunu kurarken kullan.

### Kategori 27: sec (18 skill)
427. `sec-tls-mtls-design` — TLS ve mTLS tasarımı, CA hiyerarşisi ve otomatik yenileme kurallarını uygularken kullan.
428. `sec-secrets-vault` — HashiCorp Vault kurulumu, secret engine, policy ve dynamic credential yönetimini kurarken kullan.
429. `sec-secrets-env-injection` — Kubernetes Pod'a secret env enjeksiyonu ve External Secrets Operator kullanımını kurarken kullan.
430. `sec-owasp-top10-api` — OWASP API Security Top 10 güvenlik açıklarını FastAPI servislerinde kontrol etme ve giderme kurallarını uygularken kullan.
431. `sec-dependency-sbom` — SBOM üretimi (syft), imzalama ve güvenlik açığı eşleştirmesini kurarken kullan.
432. `sec-static-analysis` — Bandit/Semgrep ile Python güvenlik statik analizi ve CI entegrasyonunu uygularken kullan.
433. `sec-dast-zap` — OWASP ZAP ile dinamik uygulama güvenlik testi ve CI pipeline entegrasyonunu kurarken kullan.
434. `sec-container-hardening` — Container image güvenlik sertleştirme: minimal base, non-root user ve read-only fs kurallarını uygularken kullan.
435. `sec-network-segmentation` — Mikro segmentasyon tasarımı, zero-trust ağ modeli ve east-west trafik kontrol kurallarını uygularken kullan.
436. `sec-threat-modeling-stride` — STRIDE tehdit modelleme metodolojisi ve kontrol eşleştirmesini uygularken kullan.
437. `sec-pen-test-checklist` — İç ağ ve API penetrasyon testi kontrol listesi ve kapsam tanımını uygularken kullan.
438. `sec-incident-response` — Güvenlik olayı müdahale planı, iletişim akışı ve forensic log toplama prosedürünü uygularken kullan.
439. `sec-compliance-cis` — CIS Benchmark kontrolleri, Kubernetes CIS hardening ve otomatik kontrol tarama kurallarını uygularken kullan.
440. `sec-api-key-lifecycle` — API anahtarı oluşturma, dağıtım, rotasyon ve iptal yaşam döngüsü yönetimini kurarken kullan.
441. `sec-jwt-validation` — JWT imza doğrulama, claim kontrolü, expiry ve algorithm pinning güvenlik kurallarını uygularken kullan.
442. `sec-oauth2-pkce` — OAuth 2.0 PKCE akışı, token endpoint ve callback işleme güvenlik kurallarını uygularken kullan.
443. `sec-supply-chain-integrity` — Yazılım tedarik zinciri güvenliği, SLSA seviye gereksinimleri ve imzalama araç zincirini kurarken kullan.
444. `sec-log-integrity` — Log değiştirilemezliği, audit log ve tamper detection kurallarını uygularken kullan.

### Kategori 28: perf (16 skill)
445. `perf-python-profiling` — py-spy ve cProfile ile Python uygulama profilleme ve hotspot tespiti kurallarını uygularken kullan.
446. `perf-async-patterns` — asyncio task grubu, semaphore ve event loop tıkanmasını önleme kurallarını uygularken kullan.
447. `perf-connection-pooling` — httpx/aiohttp/asyncpg bağlantı havuzu boyutu ve timeout ayarlarını kurarken kullan.
448. `perf-caching-strategy` — In-memory cache (TTLCache), Redis cache ve cache invalidation stratejisini uygularken kullan.
449. `perf-query-optimization` — PromQL ve LogQL sorgu verimliliği, recording rule ve index kullanımı kurallarını uygularken kullan.
450. `perf-startup-time` — Python CLI başlangıç süresi optimizasyonu, lazy import ve warm-up stratejisini uygularken kullan.
451. `perf-memory-leak-detection` — Python memory leak tespiti (tracemalloc, memray) ve nesne sayımı kurallarını yaparken kullan.
452. `perf-batch-processing` — Büyük veri kümesinde batch işleme, chunk boyutu ve bellek-hız dengesini optimize ederken kullan.
453. `perf-grpc-vs-rest` — gRPC ve REST performans karşılaştırması ve serileştirme maliyet analizini uygularken kullan.
454. `perf-jit-numba` — Numba JIT ile Python sayısal hesaplama hızlandırma kurallarını uygularken kullan.
455. `perf-load-shedding` — Yük taşma (load shedding) stratejisi, circuit breaker ve backpressure mekanizmasını kurarken kullan.
456. `perf-p99-latency-tuning` — p99 gecikme analizi, tail latency kaynaklarını belirleme ve azaltma adımlarını uygularken kullan.
457. `perf-database-index` — PostgreSQL index tasarımı, EXPLAIN ANALYZE okuma ve yavaş sorgu tespiti kurallarını uygularken kullan.
458. `perf-cdn-edge-cache` — CDN kenar önbellek yapılandırması ve cache-control header stratejisini kurarken kullan.
459. `perf-compression` — HTTP yanıt sıkıştırma (gzip, brotli, zstd) ve FastAPI middleware kurallarını uygularken kullan.
460. `perf-concurrency-model` — Thread, process ve asyncio eşzamanlılık modeli seçim kriterleri ve Python GIL etkisini anlarken kullan.

### Kategori 29: data-postgres (14 skill)
461. `data-postgres-schema-design` — PostgreSQL şema tasarımı, normalizasyon ve naming convention kurallarını uygularken kullan.
462. `data-postgres-migrations` — Alembic ile schema migration, geri alma prosedürü ve CI entegrasyonunu kurarken kullan.
463. `data-postgres-connection-pool` — asyncpg/psycopg3 bağlantı havuzu ve health check kurallarını kurarken kullan.
464. `data-postgres-query-perf` — EXPLAIN ANALYZE, index kullanımı ve yavaş sorgu günlüğü kurallarını uygularken kullan.
465. `data-postgres-backup-restore` — pg_dump/pg_basebackup ile yedekleme, PITR ve test geri yükleme prosedürünü uygularken kullan.
466. `data-postgres-replication` — Streaming replication, logical replication ve standby promotion kurallarını kurarken kullan.
467. `data-postgres-partitioning` — Tablo partitioning (range, list, hash) ve partition pruning kurallarını uygularken kullan.
468. `data-postgres-full-text-search` — PostgreSQL full-text search (tsvector, tsquery), index ve ranking stratejisini kurarken kullan.
469. `data-postgres-jsonb` — JSONB sütun tasarımı, GIN index ve JSONPath sorgusu kurallarını uygularken kullan.
470. `data-postgres-timeseries` — PostgreSQL ile zaman serisi veri modeli ve TimescaleDB hypertable kurarken kullan.
471. `data-postgres-security` — PostgreSQL rol yönetimi, row-level security ve SSL zorlama kurallarını uygularken kullan.
472. `data-postgres-vacuum-analyze` — VACUUM, AUTOVACUUM, ANALYZE ve bloat yönetimi kurallarını uygularken kullan.
473. `data-postgres-k8s-operator` — CloudNativePG operator ile k8s-native PostgreSQL yönetimini kurarken kullan.
474. `data-postgres-observability` — pg_stat_statements ve Prometheus postgres_exporter ile izleme kurarken kullan.

### Kategori 30: data-redis (10 skill)
475. `data-redis-data-structures` — Redis string, hash, list, set, sorted set, stream veri yapıları ve kullanım senaryolarını uygularken kullan.
476. `data-redis-cache-patterns` — Redis cache-aside, write-through ve write-behind kalıpları ile TTL stratejisini kurarken kullan.
477. `data-redis-pub-sub` — Redis Pub/Sub ve Redis Streams ile olay tabanlı mesajlaşma pipeline'ını kurarken kullan.
478. `data-redis-cluster` — Redis Cluster kurulumu, slot dağılımı ve failover kurallarını uygularken kullan.
479. `data-redis-sentinel-ha` — Redis Sentinel ile yüksek erişilebilirlik ve otomatik failover kurallarını uygularken kullan.
480. `data-redis-rate-limiting` — Redis ile token bucket/sliding window rate limiting implementasyonunu yazarken kullan.
481. `data-redis-distributed-lock` — Redis Redlock protokolü ile dağıtık kilit implementasyonu kurallarını uygularken kullan.
482. `data-redis-k8s-operator` — Redis Kubernetes operator ile k8s-native yönetimi kurarken kullan.
483. `data-redis-observability` — Redis INFO komutu, redis_exporter ve Grafana dashboard ile izleme kurarken kullan.
484. `data-redis-security` — Redis AUTH, TLS, ACL ve NetworkPolicy ile güvenli Redis erişimini kurarken kullan.

### Kategori 31: data-timescale (10 skill)
485. `data-timescale-hypertable` — TimescaleDB hypertable oluşturma, chunk interval seçimi ve zaman sütunu kurallarını uygularken kullan.
486. `data-timescale-compression` — TimescaleDB sütunsal sıkıştırma yapılandırması ve sorgu performansını kurarken kullan.
487. `data-timescale-retention` — TimescaleDB data retention politikası ve drop chunk kurallarını uygularken kullan.
488. `data-timescale-continuous-agg` — TimescaleDB continuous aggregate ile önceden hesaplanmış zaman serisi özeti kurarken kullan.
489. `data-timescale-caggs-realtime` — Real-time continuous aggregate ile canlı veri dahil özet sorgusu kurarken kullan.
490. `data-timescale-prometheus-bridge` — Prometheus remote_write → TimescaleDB bridge kurulumunu yaparken kullan.
491. `data-timescale-multi-node` — TimescaleDB multi-node (access node + data nodes) dağıtık kurulumunu yaparken kullan.
492. `data-timescale-observability` — TimescaleDB boyutu sorgulama ve Grafana dashboard kurarken kullan.
493. `data-timescale-backup` — TimescaleDB yedekleme ve PITR kurallarını uygularken kullan.
494. `data-timescale-k8s-deploy` — TimescaleDB'yi Kubernetes StatefulSet veya operator ile konuşlandırırken kullan.

### Kategori 32: python (18 skill)
495. `python-pyproject-toml` — pyproject.toml (PEP 621) ile proje metadata, bağımlılık grupları ve build system seçimini kurarken kullan.
496. `python-virtualenv-uv` — uv ile hızlı sanal ortam ve paket yönetimi, lock file ve workspace kurallarını uygularken kullan.
497. `python-typing-strict` — Python strict typing, Protocol, TypeAlias, ParamSpec ve type guard kullanımını yazarken kullan.
498. `python-dataclass-pydantic` — dataclass vs Pydantic model seçim kriterleri ve validation kurallarını uygularken kullan.
499. `python-async-patterns` — asyncio.gather, TaskGroup, asyncio.Queue ve structured concurrency kalıplarını uygularken kullan.
500. `python-context-managers` — contextlib.asynccontextmanager ve async with ile kaynak yönetimini yazarken kullan.
501. `python-logging-structlog` — structlog ile yapılandırılmış JSON log, bağlam bağlama ve log level yönetimini kurarken kullan.
502. `python-error-hierarchy` — Özel exception hiyerarşisi tasarımı, chaining (raise from) ve kullanıcı dostu hata mesajı kurallarını yazarken kullan.
503. `python-cli-typer` — Typer ile CLI komut yapısı, subcommand, option ve callback kurallarını yazarken kullan.
504. `python-cli-click` — Click ile CLI dekoratör tabanlı komut sistemi ve group kurallarını kurarken kullan.
505. `python-testing-pytest` — pytest fixture kapsamı, conftest, parametrize ve marker kullanım kurallarını yazarken kullan.
506. `python-packaging-wheel` — Wheel build, sdist/wheel yayınlama ve PyPI upload kurallarını uygularken kullan.
507. `python-docstring-standard` — Google/NumPy/Sphinx docstring formatı seçimi ve zorunlu bölümleri yazarken kullan.
508. `python-ruff-lint` — ruff lint ve format kuralları, seçilen rule set ve CI entegrasyonunu yapılandırırken kullan.
509. `python-mypy-strict` — mypy strict modda tip kontrolü, stub paketleri ve ignore direktifi kurallarını uygularken kullan.
510. `python-pre-commit` — pre-commit hook'ları (ruff, mypy, bandit) kurulumu ve CI kontrol entegrasyonunu yaparken kullan.
511. `python-dependency-pinning` — Bağımlılık kilitleme stratejisi ve güvenlik güncelleme akışını kurarken kullan.
512. `python-secrets-runtime` — Python çalışma zamanında secret okuma ve log maskeleme kurallarını uygularken kullan.

### Kategori 33: fastapi (18 skill)
513. `fastapi-app-structure` — FastAPI uygulama klasör yapısı, router, dependency ve lifespan kurallarını tasarlarken kullan.
514. `fastapi-dependency-injection` — FastAPI Depends() ile bağımlılık enjeksiyonu ve override kurallarını yazarken kullan.
515. `fastapi-background-tasks` — FastAPI BackgroundTasks ve asyncio.create_task ile arka plan iş tetikleme kurallarını uygularken kullan.
516. `fastapi-middleware` — FastAPI middleware (CORS, GZip, tracing, logging) zinciri tanımlama kurallarını uygularken kullan.
517. `fastapi-exception-handlers` — FastAPI özel exception handler ve HTTP hata yanıtı formatı kurallarını yazarken kullan.
518. `fastapi-openapi-customization` — FastAPI OpenAPI şeması özelleştirme, tag ve example ekleme kurallarını uygularken kullan.
519. `fastapi-security-oauth2` — FastAPI OAuth2PasswordBearer ve JWT token doğrulama ile korumalı endpoint kurallarını yazarken kullan.
520. `fastapi-security-apikey` — FastAPI API key header/query doğrulaması ve güvenlik kurallarını yazarken kullan.
521. `fastapi-websocket` — FastAPI WebSocket endpoint, bağlantı yönetimi ve mesaj yayıncısı (broadcast) kurallarını yazarken kullan.
522. `fastapi-streaming-response` — FastAPI StreamingResponse ile büyük veri ve LLM çıktısı akışı kurallarını uygularken kullan.
523. `fastapi-lifespan` — FastAPI lifespan context manager ile başlangıç/bitiş kaynak yönetimi kurallarını yazarken kullan.
524. `fastapi-testing` — httpx.AsyncClient + pytest-asyncio ile FastAPI test yazma kurallarını uygularken kullan.
525. `fastapi-pydantic-v2` — Pydantic v2 model_validator, field_serializer ve computed_field ile FastAPI entegrasyonunu yazarken kullan.
526. `fastapi-rate-limiting` — FastAPI slowapi/fastapi-limiter ile endpoint rate limiting kurallarını kurarken kullan.
527. `fastapi-health-checks` — FastAPI /health ve /ready endpoint tasarımı ve k8s probe entegrasyonunu kurarken kullan.
528. `fastapi-observability` — FastAPI'ye opentelemetry-instrumentation-fastapi ile trace/metric/log enstrümantasyonu ekleme kurallarını uygularken kullan.
529. `fastapi-versioning` — FastAPI API versiyonlama stratejisi (URL prefix, header) ve deprecation planı kurallarını uygularken kullan.
530. `fastapi-deployment` — FastAPI'yi uvicorn/gunicorn, Docker ve Kubernetes Deployment olarak konuşlandırma kurallarını uygularken kullan.

### Kategori 34: chaos (16 skill)
531. `chaos-principles` — Chaos Engineering prensipleri, deney döngüsü ve blast radius kontrolü kurallarını uygularken kullan.
532. `chaos-steady-state` — Chaos deneyi öncesi steady-state hipotezi tanımlama ve SLO tabanlı doğrulama kurallarını yazarken kullan.
533. `chaos-network-latency` — Servise gecikme enjeksiyonu (tc netem, Chaos Mesh) ve gözlemleme metrikleri kurallarını uygularken kullan.
534. `chaos-network-partition` — Ağ bölünmesi simülasyonu ve uygulama davranışı doğrulama kurallarını uygularken kullan.
535. `chaos-pod-failure` — Kubernetes pod rastgele öldürme ve kurtarma süresi doğrulamasını kurarken kullan.
536. `chaos-node-failure` — Kubernetes node failure simülasyonu, pod tahliyesi ve yeniden zamanlama gözlemini kurarken kullan.
537. `chaos-cpu-stress` — CPU spike enjeksiyonu ve circuit breaker davranışını gözlemlerken kullan.
538. `chaos-memory-pressure` — Bellek baskısı enjeksiyonu, OOM tepkisi ve yeniden başlatma kurtarma süresi doğrulamasını kurarken kullan.
539. `chaos-disk-io` — Disk I/O gecikme ve hata enjeksiyonu ile veritabanı yük dayanıklılık testini kurarken kullan.
540. `chaos-dns-failure` — DNS çözümleme hata enjeksiyonu ve servis keşif dayanıklılık testini kurarken kullan.
541. `chaos-dependency-failure` — Bağımlı servis hata enjeksiyonu ve fallback davranışı doğrulamasını kurarken kullan.
542. `chaos-chaos-mesh-setup` — Chaos Mesh kurulumu, CRD (NetworkChaos, PodChaos, IOChaos) ve dashboard kullanımını kurarken kullan.
543. `chaos-litmus-setup` — LitmusChaos kurulumu, ChaosEngine tanımı ve workflow tabanlı deney kurallarını uygularken kullan.
544. `chaos-game-days` — Game day planlama, senaryo kitabı hazırlama ve post-mortem rapor formatını uygularken kullan.
545. `chaos-observability-during` — Chaos deneyi sırasında Prometheus/Grafana/Tempo izleme ve hypothesis doğrulama kurallarını kurarken kullan.
546. `chaos-ci-integration` — CI pipeline'da otomatik chaos deney çalıştırma ve başarı kriteri kurallarını kurarken kullan.

### Kategori 35: gitops (16 skill)
547. `gitops-principles` — GitOps prensipleri, deklaratif yapılandırma ve reconciliation döngüsünü uygularken kullan.
548. `gitops-argocd-setup` — ArgoCD kurulumu, Application CRD ve sync policy kurallarını kurarken kullan.
549. `gitops-argocd-app-of-apps` — ArgoCD app-of-apps deseni ile çok uygulama yönetimi ve bootstrap kurallarını uygularken kullan.
550. `gitops-fluxcd-setup` — Flux CD kurulumu, HelmRelease, Kustomization ve GitRepository source kurallarını kurarken kullan.
551. `gitops-helm-release` — GitOps'ta Helm release yönetimi, values override ve otomatik güncelleme kurallarını kurarken kullan.
552. `gitops-image-automation` — Flux image automation ile container image güncellemesini Git commit'e dönüştürme kurallarını kurarken kullan.
553. `gitops-secret-management` — GitOps'ta secret yönetimi (Sealed Secrets, SOPS, External Secrets) kurallarını uygularken kullan.
554. `gitops-multi-env` — GitOps çok ortam (dev/staging/prod) stratejisi ve branch/path tabanlı ayrım kurallarını uygularken kullan.
555. `gitops-drift-detection` — GitOps ortam drift tespiti ve manuel override onay akışını kurarken kullan.
556. `gitops-rollback` — GitOps ile git revert tabanlı geri alma ve otomatik rollback trigger kurallarını uygularken kullan.
557. `gitops-ci-cd-separation` — CI (build/test/push) ve CD (deploy/sync) sorumluluklarının GitOps'ta ayrılması kurallarını uygularken kullan.
558. `gitops-policy-enforcement` — GitOps pull request'e OPA/Kyverno politika kapısı ekleme kurallarını kurarken kullan.
559. `gitops-observability` — ArgoCD/Flux metriklerini Prometheus'a aktarma ve sync durum dashboard kurarken kullan.
560. `gitops-disaster-recovery` — GitOps repo tabanlı felaket kurtarma planı ve state rekonstrüksiyonu kurallarını uygularken kullan.
561. `gitops-monorepo-strategy` — Monorepo'da GitOps path-based trigger ve per-service Kustomization kurallarını uygularken kullan.
562. `gitops-azure-devops` — Azure DevOps pipeline + GitOps entegrasyonu ve sync kontrol kurallarını kurarken kullan.

### Kategori 36: net (14 skill)
563. `net-dns-fundamentals` — DNS sorgu döngüsü, kayıt tipleri (A, CNAME, SRV, TXT) ve TTL stratejisini uygularken kullan.
564. `net-http2-http3` — HTTP/2 multiplexing, HTTP/3 QUIC avantajları ve FastAPI/Traefik'te etkinleştirme kurallarını uygularken kullan.
565. `net-grpc-design` — gRPC protobuf service tanımı, streaming modları ve hata kodu kullanım kurallarını yazarken kullan.
566. `net-websocket-design` — WebSocket protokolü, bağlantı yönetimi ve heartbeat/reconnect kurallarını uygularken kullan.
567. `net-load-balancer-algorithms` — Round-robin, least connection, IP hash yük dengeleme algoritmaları seçim kurallarını uygularken kullan.
568. `net-tcp-tuning` — Linux TCP ayarı (socket buffer, backlog, keepalive) ve yüksek bağlantı sayısı optimizasyonunu yaparken kullan.
569. `net-ssl-tls-handshake` — TLS handshake adımları, cipher suite seçimi ve HSTS/OCSP yapılandırmasını uygularken kullan.
570. `net-proxy-reverse-proxy` — Reverse proxy mimarisi, Traefik/nginx ile path routing ve header düzenleme kurallarını uygularken kullan.
571. `net-vpn-overlay` — WireGuard veya Tailscale ile overlay ağ kurulumu ve k8s servislerine erişim kurallarını uygularken kullan.
572. `net-firewall-nftables` — nftables kural tablosu tasarımı ve Kubernetes host firewall kurallarını uygularken kullan.
573. `net-bandwidth-shaping` — Linux tc qdisc ile bant genişliği şekillendirme ve QoS kurallarını uygularken kullan.
574. `net-ipam-design` — IP adres yönetimi (IPAM) tasarımı, subnet ayrımı ve conflict önleme kurallarını uygularken kullan.
575. `net-packet-capture` — tcpdump ve Wireshark ile ağ paketi yakalama ve sorun giderme kurallarını uygularken kullan.
576. `net-ebpf-observability` — eBPF tabanlı ağ gözlemlenebilirliği (Cilium, Pixie) ile kernel-level metrik toplama kurallarını uygularken kullan.

### Kategori 37: agentic-multi (14 skill)
577. `agentic-multi-agent-overview` — Çok-agent mimarisi, orchestrator-subagent deseni ve görev dağıtımı kurallarını tasarlarken kullan.
578. `agentic-multi-agent-communication` — Agent'lar arası mesajlaşma protokolü, A2A standartı ve payload şeması kurallarını uygularken kullan.
579. `agentic-multi-agent-task-routing` — Orchestrator'ın görevi doğru subagent'a yönlendirme mantığı ve seçim kriterleri kurallarını yazarken kullan.
580. `agentic-multi-agent-state-sharing` — Agent'lar arası paylaşımlı durum yönetimi, çakışma çözümü ve tutarlılık kurallarını uygularken kullan.
581. `agentic-multi-agent-tool-delegation` — Bir agent'ın araç çağrısını başka agent'a devretme ve sonuç birleştirme kurallarını yazarken kullan.
582. `agentic-multi-agent-debate` — Çok-agent tartışma (debate) deseni ile fikir birliği ve kalite artırma kurallarını uygularken kullan.
583. `agentic-multi-agent-parallelism` — Agent görevleri paralel çalıştırma, bağımlılık grafı ve fan-out/fan-in kurallarını yazarken kullan.
584. `agentic-multi-agent-critique` — Üretici-eleştirici agent deseni ile çıktı kalitesini iteratif olarak artırma kurallarını uygularken kullan.
585. `agentic-multi-agent-memory-shared` — Çok-agent senaryosunda paylaşılan bellek deposu ve eşzamanlı yazma çakışması kurallarını kurarken kullan.
586. `agentic-multi-agent-auth-boundary` — Farklı agent'ların izin sınırları ve araç erişim hakları kurallarını uygularken kullan.
587. `agentic-multi-agent-observability` — Çok-agent sisteminde trace korelasyonu ve per-agent metrik toplama kurallarını kurarken kullan.
588. `agentic-multi-agent-error-propagation` — Subagent hatası üst agent'a yayılma stratejisi, retry ve fallback kurallarını uygularken kullan.
589. `agentic-multi-agent-cost-control` — Çok-agent senaryosunda LLM maliyet kontrolü, token bütçesi ve kesme kurallarını uygularken kullan.
590. `agentic-multi-agent-testing` — Çok-agent sisteminin test stratejisi ve senaryo tabanlı doğrulama kurallarını yazarken kullan.

### Kategori 38: debug (16 skill)
591. `debug-python-pdb` — Python pdb/ipdb ile interaktif hata ayıklama, breakpoint ve post-mortem analiz kurallarını uygularken kullan.
592. `debug-python-remote` — debugpy ile uzak Python süreç hata ayıklama ve VS Code attach yapılandırmasını kurarken kullan.
593. `debug-k8s-pod` — Kubectl exec, ephemeral debug container ile k8s pod sorun gidermesini yaparken kullan.
594. `debug-k8s-network` — kubectl run debug pod, netshoot ve curl ile k8s ağ sorunlarını teşhis ederken kullan.
595. `debug-core-dump` — Python core dump yapılandırması, gdb ile analiz ve container ortamında etkinleştirme kurallarını uygularken kullan.
596. `debug-memory-dump` — Python bellek dökümü (guppy, objgraph) ve nesne referans zinciri analiz kurallarını uygularken kullan.
597. `debug-async-deadlock` — asyncio deadlock tespiti, event loop dump ve coroutine izleme kurallarını uygularken kullan.
598. `debug-distributed-trace` — Dağıtık sistemde trace korelasyonu ile sorunlu servis ve span tespiti kurallarını uygularken kullan.
599. `debug-llm-tool-call` — LLM araç çağrısı hatası, argüman ayrıştırma hatası ve döngü tespiti teşhis kurallarını uygularken kullan.
600. `debug-agent-loop-stuck` — Agent döngüsü takılı kaldığında takip, iptal ve kök neden tespiti kurallarını uygularken kullan.
601. `debug-config-mismatch` — Sentinel yapılandırma uyumsuzluğu (env vs YAML) tespit etme ve öncelik sırasını doğrulama kurallarını uygularken kullan.
602. `debug-api-request-replay` — Başarısız API isteğini yeniden oynatma (curl/httpie), header inceleme ve diff analizi kurallarını uygularken kullan.
603. `debug-log-correlation` — Log zaman damgası korelasyonu, request-id izleme ve çok servis log birleştirme kurallarını uygularken kullan.
604. `debug-oom-killer` — Linux OOM Killer tetiklenme analizi, dmesg okuma ve container limit ayarlama kurallarını uygularken kullan.
605. `debug-juju-hook-failure` — Juju hook hatası teşhisi ve debug-hooks ile interaktif inceleme kurallarını uygularken kullan.
606. `debug-ci-flaky-test` — CI'da kararsız (flaky) test tespiti, temel neden analizi ve karantina stratejisi kurallarını uygularken kullan.

### Kategori 39: docs (14 skill)
607. `docs-adr-workflow` — Architecture Decision Record (ADR) yazma akışı, şablon ve gözden geçirme kurallarını uygularken kullan.
608. `docs-changelog-format` — CHANGELOG.md formatı (Keep a Changelog), sürüm numaralandırma ve otomasyon kurallarını uygularken kullan.
609. `docs-api-reference-auto` — FastAPI/pydantic şemasından otomatik API referans belgesi üretimi ve yayınlama kurallarını uygularken kullan.
610. `docs-runbook-template` — Operasyonel runbook şablonu, adım-adım prosedür ve eskalasyon kurallarını yazarken kullan.
611. `docs-post-mortem-template` — Post-mortem rapor şablonu, blameless kültür ve action item takip kurallarını uygularken kullan.
612. `docs-diagram-as-code` — Mermaid, PlantUML veya D2 ile kod olarak mimari diyagram üretme kurallarını uygularken kullan.
613. `docs-skill-index-maintenance` — Sentinel skill kataloğu güncelleme, yeni skill ekleme ve eski skill arşivleme kurallarını uygularken kullan.
614. `docs-readme-structure` — README.md bölüm yapısı, hızlı başlangıç ve rozet ekleme kurallarını uygularken kullan.
615. `docs-contributing-guide` — CONTRIBUTING.md formatı, PR adımları ve code review kurallarını yazarken kullan.
616. `docs-version-matrix` — Bileşen versiyon uyumluluk tablosu ve destek ömrü kurallarını uygularken kullan.
617. `docs-glossary` — Proje terim sözlüğü oluşturma, tanım standardı ve cross-reference kurallarını uygularken kullan.
618. `docs-onboarding-checklist` — Yeni geliştirici onboarding kontrol listesi ve ilk katkı rehberini uygularken kullan.
619. `docs-license-compliance` — Açık kaynak lisans uyumu, bağımlılık lisans denetimi ve NOTICE dosyası kurallarını uygularken kullan.
620. `docs-security-policy` — SECURITY.md güvenlik açığı bildirme politikası ve CVE yönetim kurallarını yazarken kullan.

### Kategori 40: platform (16 skill)
621. `platform-idp-backstage` — Backstage IDP kurulumu, catalog, software template ve plugin ekleme kurallarını uygularken kullan.
622. `platform-paved-road` — Platform ekibi "paved road" araç seti, golden path template ve self-service kurallarını tasarlarken kullan.
623. `platform-cost-allocation` — Kubernetes namespace bazlı maliyet dağılımı (kubecost, opencost) ve bütçe alarm kurallarını kurarken kullan.
624. `platform-feature-flags` — Feature flag sistemi (LaunchDarkly, Unleash, Flagsmith) entegrasyonu ve kill switch kurallarını kurarken kullan.
625. `platform-slo-framework` — SLO çerçevesi tasarımı, error budget politikası ve SLO dashboard kurallarını kurarken kullan.
626. `platform-incident-management` — Incident management süreci, severity sınıflandırması ve PagerDuty entegrasyonu kurallarını uygularken kullan.
627. `platform-change-management` — Değişiklik yönetim süreci, onay akışı ve geri alma planı kurallarını uygularken kullan.
628. `platform-capacity-review` — Aylık kapasite gözden geçirme süreci ve karar belgesi şablonunu uygularken kullan.
629. `platform-multi-cluster` — Çok-küme yönetimi, merkezi kontrol düzlemi ve küme federasyon kurallarını tasarlarken kullan.
630. `platform-developer-portal` — Geliştirici portalı (Backstage/Port) servis kataloğu ve self-service kurallarını kurarken kullan.
631. `platform-toil-reduction` — SRE toil ölçümü, otomasyon önceliklendirme ve toil bütçesi kurallarını uygularken kullan.
632. `platform-chaos-maturity` — Chaos Engineering olgunluk modeli, seviye değerlendirmesi ve yol haritası kurallarını uygularken kullan.
633. `platform-finops-rightsizing` — FinOps right-sizing analizi, kaynak israfı tespiti ve öneri motoru kurallarını kurarken kullan.
634. `platform-environment-parity` — Dev/staging/prod ortam paritesini koruma ve config drift tespiti kurallarını uygularken kullan.
635. `platform-service-catalog` — Servis kataloğu tasarımı, sahiplik metadata, SLO ve bağımlılık graph kurallarını uygularken kullan.
636. `platform-api-gateway` — Merkezi API gateway (Kong, APISIX) kurulumu, rate limit ve auth plugin kurallarını kurarken kullan.

### Kategori 41: target-app (16 skill)
637. `target-app-fastapi-middleware-stack` — Test platformu FastAPI servislerine logging, tracing ve metrics middleware zinciri ekleme kurallarını uygularken kullan.
638. `target-app-postgres-integration` — Test platformu servisine asyncpg ile PostgreSQL entegrasyonu ve migration yönetimini kurarken kullan.
639. `target-app-redis-integration` — Test platformu servisine aioredis ile Redis entegrasyonu ve pub/sub kullanımını kurarken kullan.
640. `target-app-payment-simulation` — Ödeme servisi hata senaryoları, timeout ve fraud rate simülasyonunu yazarken kullan.
641. `target-app-inventory-simulation` — Envanter servisi out-of-stock, concurrency ve düşük stok alarm simülasyonunu yazarken kullan.
642. `target-app-orders-simulation` — Sipariş servisi sipariş akışı, kısmi hata ve retry simülasyonunu yazarken kullan.
643. `target-app-gateway-simulation` — API gateway trafik yönlendirme, circuit breaker ve auth hata simülasyonunu yazarken kullan.
644. `target-app-worker-simulation` — Worker servisi kuyruk tüketimi, dead-letter ve slow consumer simülasyonunu yazarken kullan.
645. `target-app-otel-custom-spans` — Test platformu servislerine özel span ve attribute ekleme kurallarını uygularken kullan.
646. `target-app-custom-metrics` — Test platformu servislerine özel Prometheus metric (counter, histogram, gauge) ekleme kurallarını uygularken kullan.
647. `target-app-health-endpoint` — Test platformu servislerine /health ve /ready endpoint ekleme ve bağımlılık kontrolü kurallarını uygularken kullan.
648. `target-app-auth-simulation` — Test platformu servislerine JWT doğrulama katmanı ve 401/403 hata simülasyonunu kurarken kullan.
649. `target-app-rate-limit-simulation` — Test platformu servislerine 429 rate limit simülasyonu ekleme kurallarını uygularken kullan.
650. `target-app-versioned-api` — Test platformu servislerinde API versiyonlama (/v1, /v2) ve migration kurallarını uygularken kullan.
651. `target-app-dark-launch` — Test platformu servisinde feature flag ile dark launch ve trafik bölme simülasyonunu kurarken kullan.
652. `target-app-distributed-transaction` — Çok servisli dağıtık işlem simülasyonu (saga deseni) ve başarısız telafi kurallarını yazarken kullan.

### Kategori 42: ci (16 skill)
653. `ci-github-actions-matrix` — GitHub Actions matrix build, Python sürüm matrisi ve koşullu adım kurallarını yazarken kullan.
654. `ci-github-actions-cache` — GitHub Actions pip/uv cache, cache key stratejisi ve invalidation kurallarını kurarken kullan.
655. `ci-github-actions-secrets` — GitHub Actions secret ekleme, environment scope ve güvenli injection kurallarını uygularken kullan.
656. `ci-github-actions-reusable` — Yeniden kullanılabilir GitHub Actions workflow ve composite action yazma kurallarını uygularken kullan.
657. `ci-github-actions-oidc` — GitHub Actions OIDC ile cloud kimlik doğrulaması (AWS, GCP) ve secret'sız deployment kurallarını kurarken kullan.
658. `ci-github-actions-self-hosted` — Self-hosted GitHub Actions runner kurulumu, etiketleme ve güvenlik kurallarını uygularken kullan.
659. `ci-docker-build-push` — Docker image build, multi-stage, layer cache ve registry push CI kurallarını uygularken kullan.
660. `ci-semantic-versioning` — Semantic versioning (semver) taahhüt tabanlı otomatik sürüm belirleme kurallarını kurarken kullan.
661. `ci-conventional-commits` — Conventional Commits standardı, commit lint CI ve CHANGELOG otomasyon kurallarını uygularken kullan.
662. `ci-pr-gate` — PR geçiş kapısı: lint, test, type check, coverage ve güvenlik tarama zorunluluğunu kurarken kullan.
663. `ci-deploy-k8s` — CI'dan Kubernetes'e kubectl/helm deploy ve ortam bazlı promotion kurallarını uygularken kullan.
664. `ci-dependency-update` — Dependabot / Renovate bot yapılandırması ve otomatik merge kurallarını kurarken kullan.
665. `ci-artifact-registry` — CI artifact kayıt yönetimi (GHCR, ECR), immutable tag ve temizlik politikası kurallarını kurarken kullan.
666. `ci-pipeline-observability` — CI pipeline süre, başarı oranı ve hata eğilimi Grafana dashboard kurallarını kurarken kullan.
667. `ci-pre-release` — Pre-release (alpha, beta, rc) yayın akışı, kanal stratejisi ve test onay kurallarını uygularken kullan.
668. `ci-rollback-gate` — CD pipeline'da otomatik rollback kapısı, metrik eşiği ve geri alma tetikleyici kurallarını kurarken kullan.

---

**Toplam: 668 skill** (42 kategori)

Mevcut 91 skill'e ek olarak **577 yeni skill** → Toplamda **668+** skill.

---

Listeyi onaylıyor musun? Onaylarsan sırayla oluşturmaya başlayacağım. Hangi kategoriden başlamamı istersin, yoksa 1'den başlayıp sırayla mı gidelim?
#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"


@dataclass(frozen=True)
class SkillSpec:
    name: str
    intent_tr: str  # canonical one-liner intent from skill-creator-ref.md / user list


SPECS: list[SkillSpec] = [
    # obs-prometheus (20)
    SkillSpec("obs-prometheus-scrape-config", "Prometheus scrape job ve hedef keşif kurallarını yapılandırırken kullan."),
    SkillSpec("obs-prometheus-recording-rules", "Sık sorgulanan metrikleri önceden hesaplayan recording rule yazarken kullan."),
    SkillSpec("obs-prometheus-alerting-rules", "Prometheus alerting rule sözdizimi ve threshold belirleme kurallarını yazarken kullan."),
    SkillSpec("obs-prometheus-remote-write", "Prometheus remote_write ve uzak depolama entegrasyonunu kurarken kullan."),
    SkillSpec("obs-prometheus-federation", "Çok-küme senaryolarında Prometheus federation ile merkezi metrik toplarken kullan."),
    SkillSpec("obs-prometheus-storage-tsdb", "TSDB retention politikası ve disk büyüme tahmini yaparken kullan."),
    SkillSpec("obs-prometheus-query-range", "PromQL query_range API parametrelerini ve sonuç yapısını kullanırken kullan."),
    SkillSpec("obs-prometheus-instant-query", "PromQL anlık sorgu endpoint'ini ve dönen veri modelini anlamak için kullan."),
    SkillSpec("obs-prometheus-labels-strategy", "Metrik label tasarımı, kardinalite riski ve normalleştirme kurallarını belirlerken kullan."),
    SkillSpec("obs-prometheus-histogram-summary", "Histogram ve Summary farkını, bucket tasarımını ve quantile hesabını anlatırken kullan."),
    SkillSpec("obs-prometheus-service-discovery", "Kubernetes SD, file SD ve static_config ile hedef keşfi yapılandırırken kullan."),
    SkillSpec("obs-prometheus-operator-crds", "ServiceMonitor/PodMonitor/PrometheusRule CRD'leri ile k8s-native izleme kurarken kullan."),
    SkillSpec("obs-prometheus-anomaly-detection", "PromQL ile z-score ve ratio trend tabanlı anomali tespiti yazarken kullan."),
    SkillSpec("obs-prometheus-api-auth", "Prometheus HTTP API'ye basic auth, TLS veya reverse proxy erişim güvenliği sağlarken kullan."),
    SkillSpec("obs-prometheus-capacity-planning", "Metrik sayısı ve scrape interval'e göre kaynak kapasitesi planlarken kullan."),
    SkillSpec("obs-prometheus-exemplars", "Trace-metric köprüsü için exemplar yapılandırması ve Grafana görselleştirmesini kurarken kullan."),
    SkillSpec("obs-prometheus-multi-tenancy", "Label tabanlı izolasyon ve tenant-aware sorgulama kurallarını uygularken kullan."),
    SkillSpec("obs-prometheus-backup-restore", "TSDB snapshot alma ve geri yükleme prosedürünü uygularken kullan."),
    SkillSpec("obs-prometheus-unit-testing", "promtool ile alerting/recording kural birim testini yazarken kullan."),
    SkillSpec("obs-prometheus-juju-charm-metrics", "Juju charm'larının sunduğu metrikleri ve scrape relation yapılandırmasını anlamak için kullan."),
    # obs-loki (20)
    SkillSpec("obs-loki-query-logql", "LogQL filtre, parser ve metric query sözdizimini yazarken kullan."),
    SkillSpec("obs-loki-label-strategy", "Loki label tasarımı, high-cardinality önleme ve index boyutu optimizasyonu yaparken kullan."),
    SkillSpec("obs-loki-push-api", "Loki push API'sine log gönderme payload ve label formatını kurarken kullan."),
    SkillSpec("obs-loki-storage-backend", "Loki depolama backend seçimi (filesystem, S3, BoltDB) ve yapılandırmasını kurarken kullan."),
    SkillSpec("obs-loki-compactor", "Loki compactor retention politikası ve indeks temizleme prosedürünü yapılandırırken kullan."),
    SkillSpec("obs-loki-ruler-alerts", "Loki ruler ile log tabanlı alerting kuralı yazarken kullan."),
    SkillSpec("obs-loki-multi-tenancy", "X-Scope-OrgID header ile çok kiracılı log izolasyonu yaparken kullan."),
    SkillSpec("obs-loki-chunk-cache", "Loki chunk cache (memcached/redis) entegrasyonu ile sorgu performansını artırırken kullan."),
    SkillSpec("obs-loki-structured-metadata", "OTel log attribute ile zenginleştirilmiş Loki sorguları yaparken kullan."),
    SkillSpec("obs-loki-pattern-detection", "Loki pattern sorguları ile log anomalisi ve hata kümeleme analizi yaparken kullan."),
    SkillSpec("obs-loki-ingester-config", "Loki ingester flush interval, chunk encoding ve WAL ayarlarını yapılandırırken kullan."),
    SkillSpec("obs-loki-query-frontend", "Loki query frontend sharding ve caching stratejisini ayarlarken kullan."),
    SkillSpec("obs-loki-promtail-config", "Promtail scrape config, pipeline stages ve multi-line log birleştirmeyi kurarken kullan."),
    SkillSpec("obs-loki-otel-collector-export", "OTEL Collector'dan Loki'ye log export pipeline'ını yapılandırırken kullan."),
    SkillSpec("obs-loki-grafana-datasource", "Grafana'da Loki datasource, derived field ve trace-log korelasyonunu kurarken kullan."),
    SkillSpec("obs-loki-troubleshoot-ingest", "Loki'ye log gelmiyor durumunda ingestion pipeline sorunlarını teşhis ederken kullan."),
    SkillSpec("obs-loki-troubleshoot-query", "Loki sorgu hatası, timeout ve boş sonuç durumlarında teşhis adımlarını uygularken kullan."),
    SkillSpec("obs-loki-chunk-encoding", "Loki sıkıştırma formatları (gzip, snappy, lz4, zstd) ve performans trade-off'larını seçerken kullan."),
    SkillSpec("obs-loki-index-gateway", "Loki index gateway bileşenini ayrı node olarak konuşlandırırken kullan."),
    SkillSpec("obs-loki-recording-rules", "Loki recording rules ile log metriği türeterek Prometheus'a bridge yaparken kullan."),
    # obs-tempo (18)
    SkillSpec("obs-tempo-trace-query", "Tempo trace arama API'si ve TraceQL sorgu sözdizimini kullanırken kullan."),
    SkillSpec("obs-tempo-traceql-advanced", "TraceQL span attribute filtresi ve structural operator kullanımını yazarken kullan."),
    SkillSpec("obs-tempo-storage-backend", "Tempo depolama backend seçimi (local, S3, GCS) ve parça yönetimini yapılandırırken kullan."),
    SkillSpec("obs-tempo-sampling-strategy", "Head-based ve tail-based sampling stratejisi ve OTEL Collector sampling yapılandırmasını yaparken kullan."),
    SkillSpec("obs-tempo-exemplars-grafana", "Tempo-Prometheus exemplar köprüsünü Grafana explore'da kurarken kullan."),
    SkillSpec("obs-tempo-distributor-config", "Tempo distributor ve receiver protokolleri (OTLP, Jaeger, Zipkin) yapılandırırken kullan."),
    SkillSpec("obs-tempo-compactor-retention", "Tempo compactor ve trace retention politikasını uygularken kullan."),
    SkillSpec("obs-tempo-multi-tenancy", "Tempo tenant header ile çok kiracılı trace izolasyonu yaparken kullan."),
    SkillSpec("obs-tempo-grafana-datasource", "Grafana'da Tempo datasource, trace-log korelasyonu ve service graph kurarken kullan."),
    SkillSpec("obs-tempo-service-graph", "Tempo service graph metriklerini Prometheus'a aktararak topoloji görselleştirmesi yaparken kullan."),
    SkillSpec("obs-tempo-span-metrics", "Tempo span metrics pipeline ile RED metriklerini türetirken kullan."),
    SkillSpec("obs-tempo-troubleshoot-ingest", "Tempo'ya trace gelmiyor durumunda ingestion sorunlarını teşhis ederken kullan."),
    SkillSpec("obs-tempo-troubleshoot-query", "Tempo sorgu hatası, boş trace ve timeout durumlarında teşhis adımlarını uygularken kullan."),
    SkillSpec("obs-tempo-otel-sdk-integration", "Uygulama tarafında OTEL SDK ile trace üretimi ve Tempo export yapılandırmasını yaparken kullan."),
    SkillSpec("obs-tempo-jaeger-compat", "Jaeger UI uyumluluğu gereken ortamlarda Tempo jaeger receiver kullanımını yaparken kullan."),
    SkillSpec("obs-tempo-pipeline-e2e", "OTEL SDK → Collector → Tempo → Grafana zincirini uçtan uca doğrularken kullan."),
    SkillSpec("obs-tempo-resource-sizing", "Tempo bileşen hafıza/CPU boyutlandırması ve disk büyüme tahmini yaparken kullan."),
    SkillSpec("obs-tempo-hot-cold-storage", "Tempo hot/cold storage katmanlaması ve object storage migration yaparken kullan."),
    # obs-grafana (22)
    SkillSpec("obs-grafana-dashboard-design", "Grafana dashboard panel seçimi, layout ve değişken tasarımı kurallarını uygularken kullan."),
    SkillSpec("obs-grafana-variables", "Template değişkenleri (query, custom, interval, datasource) oluşturup kullanırken kullan."),
    SkillSpec("obs-grafana-alerting-unified", "Grafana unified alerting, contact point ve notification policy kurarken kullan."),
    SkillSpec("obs-grafana-annotations", "Grafana annotation oluşturma ve event-driven annotation yaparken kullan."),
    SkillSpec("obs-grafana-datasource-proxy", "Grafana datasource proxy güvenliği ve auth forward kurallarını uygularken kullan."),
    SkillSpec("obs-grafana-provisioning", "YAML dosyaları ile dashboard/datasource/alert otomatik yüklemeyi kurarken kullan."),
    SkillSpec("obs-grafana-loki-explore", "Grafana Explore'da Loki log sorgusu, log context ve live tail kullanımını yaparken kullan."),
    SkillSpec("obs-grafana-tempo-explore", "Grafana Explore'da Tempo trace sorgusu ve service graph kullanımını yaparken kullan."),
    SkillSpec("obs-grafana-prometheus-explore", "Grafana Explore ile PromQL sorgusu ve metric browser kullanımını yaparken kullan."),
    SkillSpec("obs-grafana-slo-panel", "Grafana'da SLO/SLI paneli ve error budget görselleştirmesini tasarlarken kullan."),
    SkillSpec("obs-grafana-heatmap-panel", "Grafana heatmap panel ile histogram dağılımı ve latency band görselleştirmesini yaparken kullan."),
    SkillSpec("obs-grafana-stat-panel", "Grafana stat ve gauge panel konfigürasyonu ve threshold renk kurallarını uygularken kullan."),
    SkillSpec("obs-grafana-table-panel", "Grafana table panel ile transform, field override ve link yapılandırmasını yaparken kullan."),
    SkillSpec("obs-grafana-logs-panel", "Grafana logs panel konfigürasyonu ve label filtresi ayarlarını yaparken kullan."),
    SkillSpec("obs-grafana-trace-panel", "Grafana trace panel ile trace görselleştirmesi ve span detayı yapılandırmasını yaparken kullan."),
    SkillSpec("obs-grafana-api-http", "Grafana HTTP API ile dashboard CRUD, alert ve datasource yönetimini yaparken kullan."),
    SkillSpec("obs-grafana-rbac", "Grafana RBAC ile rol, team ve folder izin yönetimini yaparken kullan."),
    SkillSpec("obs-grafana-plugin-install", "Grafana plugin kurulumu, offline install ve version kilitlemeyi yaparken kullan."),
    SkillSpec("obs-grafana-ai-plugin", "Grafana LLM plugin ile doğal dil sorgulama entegrasyonunu yaparken kullan."),
    SkillSpec("obs-grafana-backup-restore", "Grafana dashboard/datasource backup ve geri yükleme prosedürünü uygularken kullan."),
    SkillSpec("obs-grafana-image-renderer", "Grafana image renderer kurulumu ve dashboard ekran görüntüsü alma özelliğini kurarken kullan."),
    SkillSpec("obs-grafana-juju-relation", "Juju grafana-source relation ile datasource otomatik kaydını kurarken kullan."),
    # obs-alertmanager (16)
    SkillSpec("obs-alertmanager-routing", "Alertmanager route ağacı, matchers ve continue flag yapılandırmasını kurarken kullan."),
    SkillSpec("obs-alertmanager-receivers", "Alertmanager receiver (email, Slack, PagerDuty, webhook) yapılandırmasını kurarken kullan."),
    SkillSpec("obs-alertmanager-inhibit", "Alertmanager inhibit_rules ile gereksiz alert bastırma mantığını kurarken kullan."),
    SkillSpec("obs-alertmanager-silence", "Alertmanager silence oluşturma ve API ile programatik bastırma yaparken kullan."),
    SkillSpec("obs-alertmanager-grouping", "Alert gruplama stratejisi (group_by, wait, interval, repeat) ayarlarken kullan."),
    SkillSpec("obs-alertmanager-high-availability", "Alertmanager HA cluster kurulumu ve duplicate supression yaparken kullan."),
    SkillSpec("obs-alertmanager-api", "Alertmanager v2 API ile alert listeleme ve silence CRUD yaparken kullan."),
    SkillSpec("obs-alertmanager-webhook-integration", "Alertmanager webhook receiver ile özel alert handler entegrasyonunu yaparken kullan."),
    SkillSpec("obs-alertmanager-slack-template", "Alertmanager Slack mesaj template özelleştirmesi ve rich formatting yaparken kullan."),
    SkillSpec("obs-alertmanager-pagerduty", "Alertmanager PagerDuty entegrasyonu ve severity mapping yapılandırmasını kurarken kullan."),
    SkillSpec("obs-alertmanager-opsgenie", "Alertmanager OpsGenie entegrasyonu ve responder mapping yaparken kullan."),
    SkillSpec("obs-alertmanager-alert-lifecycle", "Alert firing→resolved yaşam döngüsü ve flapping önleme kurallarını uygularken kullan."),
    SkillSpec("obs-alertmanager-troubleshoot", "Alertmanager'da bildirim gitmiyor ve route eşleşmiyor sorunlarını teşhis ederken kullan."),
    SkillSpec("obs-alertmanager-juju-relation", "Juju alertmanager relation ile Prometheus→Alertmanager bağlantısını kurarken kullan."),
    SkillSpec("obs-alertmanager-msteams", "Alertmanager Microsoft Teams entegrasyonu ve adaptive card template yaparken kullan."),
    SkillSpec("obs-alertmanager-runbook-url", "Alert runbook URL alanı kullanımı ve otomatik runbook oluşturma akışını kurarken kullan."),
    # obs-otel (4) - user list subset
    SkillSpec("obs-otel-collector-pipeline", "OTEL Collector receiver/processor/exporter pipeline mimarisini kurarken kullan."),
    SkillSpec("obs-otel-collector-receivers", "OTEL Collector receiver'ları (OTLP, Prometheus, Filelog, Jaeger) yapılandırırken kullan."),
    SkillSpec("obs-otel-collector-processors", "OTEL Collector processor'ları (batch, memory_limiter, attribute, filter) kurarken kullan."),
    SkillSpec("obs-otel-collector-exporters", "OTEL Collector exporter'ları (OTLP, Prometheus, Loki, debug) yapılandırırken kullan."),
]


def _assert_valid_name(name: str) -> None:
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        raise ValueError(f"Invalid skill name: {name!r}")


def _ui_display_name(name: str) -> str:
    # Keep it deterministic and short. Example: "Prometheus: Scrape Config"
    parts = name.split("-")
    if len(parts) < 3:
        return name
    domain = parts[1].capitalize()
    rest = " ".join(p.capitalize() for p in parts[2:])
    return f"{domain}: {rest}"


def _ui_short_description(spec: SkillSpec) -> str:
    # UI blurb (25–64 chars target). Keep Turkish.
    base = spec.intent_tr
    base = re.sub(r"\s+", " ", base).strip()
    base = base.replace("kullan.", "").strip()
    if len(base) <= 64:
        return base
    return (base[:61].rstrip() + "…")


def _references_for(name: str) -> list[str]:
    # Keep to repo-local, existing references only.
    if name.startswith("obs-prometheus-"):
        return [
            "skills/cos-deploy-prometheus",
            "skills/cos-relation-prometheus-grafana",
            "cli/skills/agentic-troubleshoot-prometheus",
        ]
    if name.startswith("obs-loki-"):
        return [
            "skills/cos-deploy-loki",
            "skills/cos-relation-loki-grafana",
            "cli/skills/agentic-troubleshoot-loki",
        ]
    if name.startswith("obs-tempo-"):
        # cos-deploy-tempo not present in current repo skills/ list; reference target-app or gateway docs instead.
        return [
            "skills/target-app-fastapi-otel-bootstrap",
            "skills/target-app-observability-lib",
        ]
    if name.startswith("obs-grafana-"):
        return [
            "skills/cos-deploy-grafana",
            "cli/skills/agentic-troubleshoot-grafana",
        ]
    if name.startswith("obs-alertmanager-"):
        return [
            "skills/cos-deploy-alertmanager",
            "cli/skills/agentic-troubleshoot-alertmanager",
        ]
    if name.startswith("obs-otel-"):
        return [
            "skills/target-app-fastapi-otel-bootstrap",
            "skills/target-app-observability-lib",
        ]
    return []


def _skill_md(spec: SkillSpec) -> str:
    _assert_valid_name(spec.name)
    triggers = [
        spec.name,
        spec.name.replace("-", " "),
        spec.name.split("-", 2)[1],
    ]
    trigger_hint = ", ".join(f"“{t}”" for t in triggers)
    return "\n".join(
        [
            "---",
            f"name: {spec.name}",
            (
                "description: "
                f"{spec.intent_tr} Kullanıcı {trigger_hint} gibi ifadelerle "
                "Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya "
                "troubleshooting istediğinde bu skill’e başvur."
            ),
            "---",
            "",
            "## Purpose",
            spec.intent_tr.rstrip("."),
            "",
            "## Workflow",
            "- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).",
            "- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.",
            "- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.",
            "- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.",
            "",
            "## References",
            *([f"- `{p}`" for p in _references_for(spec.name)] or ["- (repo içi uygun referans yoksa ekleme)"]),
            "",
        ]
    )


def _openai_yaml(spec: SkillSpec) -> str:
    _assert_valid_name(spec.name)
    return "\n".join(
        [
            "interface:",
            f'  display_name: "{_ui_display_name(spec.name)}"',
            f'  short_description: "{_ui_short_description(spec)}"',
            f'  default_prompt: "Use ${spec.name} to complete this task."',
            "",
            "policy:",
            "  allow_implicit_invocation: true",
            "",
        ]
    )


def write_skill(spec: SkillSpec, *, overwrite: bool) -> tuple[Path, bool]:
    skill_dir = SKILLS_DIR / spec.name
    skill_md_path = skill_dir / "SKILL.md"
    openai_path = skill_dir / "agents" / "openai.yaml"

    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "agents").mkdir(parents=True, exist_ok=True)

    created = False

    md_content = _skill_md(spec)
    if overwrite or not skill_md_path.exists():
        skill_md_path.write_text(md_content, encoding="utf-8")
        created = True

    yaml_content = _openai_yaml(spec)
    if overwrite or not openai_path.exists():
        openai_path.write_text(yaml_content, encoding="utf-8")
        created = True

    return skill_dir, created


def main() -> None:
    overwrite = True
    created = []
    for spec in SPECS:
        d, changed = write_skill(spec, overwrite=overwrite)
        if changed:
            created.append(d)

    # Minimal report for humans running the script.
    print(f"repo_root={REPO_ROOT}")
    print(f"skills_dir={SKILLS_DIR}")
    print(f"skills_written={len(created)}")
    for d in created:
        print(f"- {d.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()


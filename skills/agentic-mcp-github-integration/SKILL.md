---
name: agentic-mcp-github-integration
description: "GitHub MCP server araçlarını Sentinel workflow'una entegre etme; issue/PR okuma-yazma, kod arama ve CI durumu sorgulama için agent yapılandırması"
---

## Purpose
GitHub'ın resmi MCP server'ını kullanarak LLM agent'ların Sentinel repo'sundaki issue/PR işlemlerini, CI durumunu ve kod aramayı otomatikleştirmesini sağlamak.

## Workflow

### GitHub MCP Server Kurulumu
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Gerekli Token Yetkileri
```
repo:read          # kod okuma
issues:write       # issue oluşturma/güncelleme
pull_requests:read # PR okuma
actions:read       # CI durum okuma
```

### Yaygın Araç Çağrıları

#### Issue Arama ve Triage
```python
# Agent sistemine verilen örnek prompt
TRIAGE_SYSTEM_PROMPT = """
Sentinel monitoring projesi için GitHub issue triager'ısın.
Açık issueları öncelik sırasına koy:
1. github araçlarını kullanarak open issueları listele
2. Her issue için labels, comments ve linked PR'ları kontrol et
3. severity/priority etiketleri eksikse ekle
4. Benzer issueları grupla ve duplicate'leri işaretle
"""

# Araç çağrısı akışı:
# list_issues → get_issue → update_issue (labels ekle) → create_comment
```

#### PR Review Otomasyonu
```python
PR_REVIEW_PROMPT = """
Açık PR'ları incele ve şunları kontrol et:
- CHANGELOG güncellendi mi?
- Test coverage düştü mü? (CI check'e bak)
- Breaking change var mı? (BREAKING CHANGE: commit prefix)
- Reviewer atandı mı?

Eksik olanları PR comment olarak bildir.
"""
```

#### CI Durum Kontrolü
```python
# MCP araç çağrısı örneği (pseudo)
async def check_ci_for_pr(pr_number: int) -> str:
    # GitHub MCP araçları:
    # - get_pull_request_checks(pr_number)
    # - list_workflow_runs(branch=pr.head_branch)
    
    checks = await mcp.call_tool("get_pull_request_checks", {
        "owner": "sentinel-project",
        "repo": "sentinel-coming",
        "pull_number": pr_number
    })
    
    failed = [c for c in checks if c["conclusion"] == "failure"]
    return f"{len(failed)} check başarısız: {[c['name'] for c in failed]}"
```

### Sentinel-Spesifik Workflow: Alert → Issue
```python
# alert_to_issue.py — Prometheus alert tetiklendiğinde issue aç
import httpx

async def create_issue_from_alert(alert: dict):
    title = f"[ALERT] {alert['labels']['alertname']} - {alert['labels'].get('service', 'unknown')}"
    body = f"""
## Alert Detayları
- **Severity**: {alert['labels'].get('severity', 'unknown')}
- **Başlangıç**: {alert['startsAt']}
- **Açıklama**: {alert['annotations'].get('description', '-')}

## PromQL
```
{alert['annotations'].get('runbook_url', 'N/A')}
```

/cc @sentinel-oncall
"""
    # MCP aracı ile issue oluştur
    await mcp.call_tool("create_issue", {
        "owner": "org",
        "repo": "sentinel-coming",
        "title": title,
        "body": body,
        "labels": ["alert", alert['labels'].get('severity', 'unknown')]
    })
```

## Common mistakes
- Token'ı `env` yerine `args` içine yazmak — shell history'de görünür
- `repo` scope yerine `public_repo` kullanmak — private repo'larda araçlar 404 döner
- Her PR için ayrı `get_repository` çağrısı yapmak — `list_pull_requests` toplu çekimde daha verimli
- Rate limit kontrolü yapmamak — 5000 req/saat aşılınca tüm araçlar 403 döner; `x-ratelimit-remaining` header'ını izle

## References
- `skills/agentic-mcp-versioning`
- `skills/agentic-mcp-error-codes`

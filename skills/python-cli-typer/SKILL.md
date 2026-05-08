---
name: python-cli-typer
description: "Typer ile modern Python CLI uygulaması yazımı — Sentinel komut satırı araçları için tip güvenli CLI yapısı"
---

## Purpose
Typer, Python type hint'lerini kullanarak minimal boilerplate ile CLI komutları oluşturur. Sentinel'de `sentinel-cli` aracı Typer üzerine inşa edilmiştir; `inspect`, `trace`, `alert` gibi alt komutlar ayrı modüllerde tanımlanarak ana app'e dahil edilir. Rich entegrasyonu sayesinde terminal çıktısı formatlanmış tablolar ve renkli mesajlar içerir.

## Workflow

### 1. Uygulama yapısı

```
sentinel_cli/
├── __init__.py
├── main.py          # Ana app, alt komutlar burada birleşir
├── commands/
│   ├── trace.py
│   ├── alert.py
│   └── inspect.py
└── utils/
    └── output.py
```

### 2. Ana app ve alt komut kaydı

```python
# main.py
import typer
from commands import trace, alert, inspect

app = typer.Typer(
    name="sentinel",
    help="Sentinel observability CLI",
    no_args_is_help=True,
)

app.add_typer(trace.app, name="trace")
app.add_typer(alert.app, name="alert")
app.add_typer(inspect.app, name="inspect")

@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Ayrıntılı çıktı"),
    output: str = typer.Option("table", "--output", "-o", help="Çıktı formatı: table|json|yaml"),
):
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["output"] = output

if __name__ == "__main__":
    app()
```

### 3. Trace alt komutu

```python
# commands/trace.py
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Trace sorgulama komutları")
console = Console()

@app.command("get")
def get_trace(
    trace_id: str = typer.Argument(..., help="Trace ID"),
    service: str = typer.Option(None, "--service", "-s", help="Servis filtresi"),
    limit: int = typer.Option(10, "--limit", "-n", min=1, max=100),
):
    """Belirtilen trace ID'yi Tempo'dan getirir."""
    from sentinel_cli.client import tempo_client

    with console.status(f"[bold green]Trace {trace_id} aranıyor..."):
        spans = tempo_client.get_trace(trace_id, service=service, limit=limit)

    if not spans:
        typer.echo(f"Trace bulunamadı: {trace_id}", err=True)
        raise typer.Exit(code=1)

    table = Table(title=f"Trace: {trace_id}")
    table.add_column("Span ID", style="cyan")
    table.add_column("Service", style="green")
    table.add_column("Duration (ms)", justify="right")
    for span in spans:
        table.add_row(span.id, span.service, str(span.duration_ms))
    console.print(table)
```

### 4. Tip güvenli parametre örnekleri

```python
from enum import Enum

class OutputFormat(str, Enum):
    table = "table"
    json = "json"
    yaml = "yaml"

@app.command("list")
def list_alerts(
    severity: str = typer.Option("all", help="critical|warning|info|all"),
    since: str = typer.Option("1h", help="Zaman dilimi: 1h, 30m, 7d"),
    format: OutputFormat = typer.Option(OutputFormat.table, "--format"),
):
    ...
```

### 5. Test

```python
from typer.testing import CliRunner
from main import app

runner = CliRunner()

def test_trace_get_not_found():
    result = runner.invoke(app, ["trace", "get", "nonexistent-id"])
    assert result.exit_code == 1
    assert "bulunamadı" in result.output
```

## Common mistakes

- `typer.Argument` ile zorunlu parametreleri `typer.Option` olarak tanımlamak — kullanıcı `--` prefix beklemez
- `ctx.obj` kullanmadan global state paylaşmaya çalışmak — `@app.callback()` ile `ctx.ensure_object(dict)` şart
- `raise typer.Exit(code=1)` yerine `sys.exit(1)` kullanmak — Typer test runner'ı exit kodu yakalayamaz
- Rich Console'u her komut dosyasında ayrı oluşturmak — merkezi bir `console.py` modülünden import et

## References
- `skills/python-cli-click`
- `skills/python-testing-pytest`
- `skills/fastapi-app-structure`

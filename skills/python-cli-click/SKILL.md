---
name: python-cli-click
description: "Click ile Python CLI komut grubu ve option yönetimi — karmaşık komut ağaçları ve plugin sistemi gerektiren araçlar için"
---

## Purpose
Click, decorator tabanlı API'siyle komut grupları, multi-value option'lar ve lazy loading plugin sistemi için Typer'a göre daha düşük seviyeli kontrol sağlar. Sentinel'de özellikle dinamik plugin yükleme ve `pass_context` ile derinlemesine paylaşılan state gerektiren araçlarda tercih edilir.

## Workflow

### 1. Komut grubu ve `pass_context`

```python
# cli.py
import click
import json

@click.group()
@click.option("--config", "-c", default="sentinel.yaml", envvar="SENTINEL_CONFIG",
              type=click.Path(exists=True), help="Yapılandırma dosyası")
@click.option("--format", type=click.Choice(["table", "json", "yaml"]), default="table")
@click.pass_context
def cli(ctx, config, format):
    """Sentinel observability komut satırı aracı."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)
    ctx.obj["format"] = format

@cli.group()
def metrics():
    """Metrik sorgulama komutları."""
    pass

@metrics.command("query")
@click.argument("promql")
@click.option("--start", default="now-1h", help="Başlangıç zamanı")
@click.option("--end", default="now", help="Bitiş zamanı")
@click.option("--step", default="60s", help="Adım aralığı")
@click.pass_context
def metrics_query(ctx, promql, start, end, step):
    """PromQL sorgusu çalıştırır."""
    config = ctx.obj["config"]
    result = query_prometheus(config.prometheus_url, promql, start, end, step)
    output(result, format=ctx.obj["format"])
```

### 2. Multi-value option ve callback doğrulama

```python
def validate_labels(ctx, param, value):
    """key=value formatını doğrular."""
    labels = {}
    for item in value:
        if "=" not in item:
            raise click.BadParameter(f"'{item}' key=value formatında olmalı")
        k, v = item.split("=", 1)
        labels[k] = v
    return labels

@cli.command("annotate")
@click.option("--label", multiple=True, callback=validate_labels, is_eager=False,
              help="Etiket: key=value (tekrarlanabilir)")
@click.argument("service")
def annotate(service, label):
    click.echo(f"Service: {service}, Labels: {label}")
```

### 3. Lazy loading plugin sistemi

```python
# plugin_cli.py
import importlib
import click

class LazyCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return ["trace", "alert", "inspect", "chaos"]

    def get_command(self, ctx, name):
        try:
            mod = importlib.import_module(f"sentinel_cli.plugins.{name}")
            return mod.cli
        except ImportError:
            return None

@click.command(cls=LazyCLI)
def sentinel():
    """Sentinel plugin CLI."""
    pass
```

### 4. Confirmation prompt ve dangerous operations

```python
@cli.command("delete-alert")
@click.argument("alert_id")
@click.option("--yes", is_flag=True, help="Onay istemeden sil")
def delete_alert(alert_id, yes):
    if not yes:
        click.confirm(f"Alert {alert_id} silinecek. Devam?", abort=True)
    # silme işlemi
    click.secho(f"Alert {alert_id} silindi.", fg="green")
```

### 5. Output helper

```python
def output(data: list[dict], format: str = "table"):
    if format == "json":
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
    elif format == "yaml":
        import yaml
        click.echo(yaml.dump(data, allow_unicode=True))
    else:
        # basit tablo
        if not data:
            click.echo("Sonuç yok.")
            return
        headers = list(data[0].keys())
        widths = {h: max(len(h), max(len(str(r[h])) for r in data)) for h in headers}
        header_line = "  ".join(h.ljust(widths[h]) for h in headers)
        click.echo(header_line)
        click.echo("-" * len(header_line))
        for row in data:
            click.echo("  ".join(str(row[h]).ljust(widths[h]) for h in headers))
```

## Common mistakes

- `@click.pass_context` ile `@click.pass_obj` karıştırmak — `pass_obj` sadece `ctx.obj` verir, `pass_context` tam context
- `callback` ile option doğrulamasını yaparken `is_eager=True` kullanmak — help mesajı çıkmadan önce çalışır
- `click.Path(exists=True)` ile opsiyonel dosya path'i tanımlamak — dosya yoksa hata fırlatır, `exists=False` kullan
- Plugin sisteminde ImportError'ı sessizce yutmak — debug modunda stacktrace göster

## References
- `skills/python-cli-typer`
- `skills/python-testing-pytest`

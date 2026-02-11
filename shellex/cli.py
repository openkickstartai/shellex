"""CLI entry point for shellex."""
import subprocess
import click
from shellex.translator import translate
from shellex.config import load_config
from shellex.safety import check_safety, SafetyLevel


@click.command()
@click.argument("query")
@click.option("-e", "--explain", is_flag=True, help="Explain the command")
@click.option("-y", "--yes", is_flag=True, help="Execute without confirmation")
@click.option("-n", "--dry-run", is_flag=True, help="Show command only")
@click.option("--model", default=None, help="Ollama model to use")
def main(query, explain, yes, dry_run, model):
    """Translate natural language to shell commands."""
    config = load_config()
    model = model or config.get("model", "llama3.2")

    result = translate(query, model=model, shell=config.get("shell", "bash"))
    if not result:
        click.echo("Could not translate. Try rephrasing.", err=True)
        raise SystemExit(1)

    click.echo(f"\n  $ {result['command']}\n")

    if explain and result.get("explanation"):
        click.echo("  Explanation:")
        for line in result["explanation"].split("\n"):
            click.echo(f"    {line}")
        click.echo()

    if dry_run:
        return

    safety = check_safety(result["command"])
    if safety == SafetyLevel.DANGEROUS:
        click.echo("  WARNING: This command may be destructive!", err=True)
        if not click.confirm("  Are you absolutely sure?"):
            return
    elif not yes:
        if not click.confirm("  Execute?"):
            return

    try:
        proc = subprocess.run(result["command"], shell=True, text=True, capture_output=False)
        raise SystemExit(proc.returncode)
    except KeyboardInterrupt:
        click.echo("\nInterrupted.")
        raise SystemExit(130)

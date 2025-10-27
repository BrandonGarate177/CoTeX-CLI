from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from .config import load_config # Imports the load_config function from the config module
from .models import ModelManager # Imports the ModelManager class from the models module

app = typer.Typer(help="CoTeX – terminal-native, project-aware AI helper.")
con = Console()

def number_code(text: str) -> str:
    return "\n".join(f"{i+1:>4}: {line}" for i, line in enumerate(text.splitlines()))

@app.command()
def explain(path: str, function: str = typer.Option(None, "--function"), agent: bool = False):
    """Explain a file (optionally a function) for a teammate."""
    cfg = load_config()
    mm = ModelManager.from_config(cfg)

    p = Path(path)
    if not p.exists():
        raise typer.BadParameter(f"File not found: {p}")

    code = p.read_text(encoding="utf-8", errors="ignore")
    shown = number_code(code)

    prompt = f"""You are CoTeX. Explain this code for a teammate.
Include: purpose, inputs/outputs, side effects, and gotchas. Cite line numbers.

FILE: {p}
CODE (with line numbers):
{shown}
"""

    con.rule("[bold]CoTeX: explain")
    # For Phase 1, return a stub if no model configured
    try:
        out = mm.complete(prompt)
    except Exception as e:
        out = f"[stub] Model not configured yet.\n\nTop-level summary for {p.name}:\n" \
              f"- Lines: {len(code.splitlines())}\n" \
              f"- Bytes: {len(code.encode('utf-8'))}\n" \
              f"- Function flag: {function or '—'}\n\n" \
              f"(Set COTEX_PROVIDER / COTEX_MODEL to enable real LLM output.)"

    con.print(Panel.fit(out, title="Explanation"))
    if con.is_terminal and len(code) < 20000:
        con.rule("[bold]Snippet")
        con.print(Syntax(code, p.suffix.lstrip('.') or "text", line_numbers=True, word_wrap=True))

@app.command()
def index(rebuild: bool = False):
    """Stub: build or refresh a project index."""
    from .indexer import ensure_index
    ensure_index(rebuild=rebuild)
    con.print("[bold green]Indexed! (stub)")

@app.command()
def trace(symbol: str):
    con.print(f"trace for {symbol} – [yellow]coming soon[/yellow].")

@app.command()
def readme(update: bool = False):
    con.print("README generation – [yellow]coming soon[/yellow].")

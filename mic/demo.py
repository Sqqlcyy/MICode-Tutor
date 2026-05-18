from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def run_demo():
    from mic.compiler import compile_repo
    from mic.inspect import inspect_memory
    from mic.retrieval import search_memory
    from mic.pack import build_context_pack

    repo = Path("examples/edu_auth_service")
    out = Path("edu_auth_service.mic")

    console.print(Panel.fit("MICode Tutor Demo", style="bold cyan"))
    console.print("[bold]Compiling demo repo into .mic memory...[/bold]\n")

    mem = compile_repo(str(repo))
    mem.save(str(out))

    console.print(f"[green]✓ Created {out}[/green]\n")
    inspect_memory(str(out))

    query = "where is JWT authentication verified?"
    console.print(f"\n[bold]Search:[/bold] {query}")
    results = search_memory(str(out), query, top_k=5)
    for i, r in enumerate(results, 1):
        console.print(f"{i}. {r}")

    task = "write tests for expired refresh tokens"
    console.print(f"\n[bold]Context Pack for:[/bold] {task}")
    pack = build_context_pack(str(out), task, budget=2500)
    console.print(pack[:4500])

    console.print("\n[bold green]Demo complete.[/bold green]")
    console.print("Try:")
    console.print("  mic ask \"explain the auth flow\" --memory edu_auth_service.mic --model gemma4")
    console.print("  mic test \"write tests for expired refresh tokens\" --memory edu_auth_service.mic --model gemma4")

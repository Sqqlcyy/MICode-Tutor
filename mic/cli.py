from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="MICode Tutor: Offline codebase memory for Gemma 4")
from mic.backend import backend_app
app.add_typer(backend_app, name="backend")
console = Console()


@app.command("compile")
def compile_cmd(
    repo_path: str = typer.Argument(..., help="Path to the repository to compile."),
    out: str = typer.Option("repo.mic", "--out", "-o", help="Output .mic memory file."),
):
    """
    Compile a repository into a portable .mic memory file.
    """
    from mic.compiler import compile_repo

    memory = compile_repo(repo_path)
    memory.save(out)

    console.print(f"[green]✓ MIC memory written to {out}[/green]")
    console.print(
        f"[dim]Files={len(memory.files)} "
        f"Symbols={len(memory.symbols)} "
        f"Relations={len(memory.relations)} "
        f"StateTokens={len(memory.state_tokens)}[/dim]"
    )


@app.command()
def inspect(
    memory_path: str = typer.Argument(..., help="Path to .mic memory file."),
):
    """
    Inspect a .mic memory file.
    """
    from mic.inspect import inspect_memory

    inspect_memory(memory_path)


@app.command()
def search(
    query: str = typer.Argument(..., help="Natural language search query."),
    memory: str = typer.Option(..., "--memory", "-m", help="Path to .mic memory file."),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results to return."),
):
    """
    Search a .mic memory file without calling an LLM.
    """
    from mic.retrieval import search_memory

    results = search_memory(memory, query, top_k=top_k)

    if not results:
        console.print("[yellow]No results found.[/yellow]")
        raise typer.Exit(0)

    for i, r in enumerate(results, 1):
        console.print(f"{i}. {r}")


@app.command()
def pack(
    task: str = typer.Argument(..., help="Task/question to build context for."),
    memory: str = typer.Option(..., "--memory", "-m", help="Path to .mic memory file."),
    budget: int = typer.Option(1200, "--budget", "-b", help="Approximate token budget."),
    top_k: int = typer.Option(4, "--top-k", "-k", help="Number of retrieved items."),
    out: str | None = typer.Option(None, "--out", "-o", help="Write context pack to file."),
):
    """
    Generate an auditable MICode Context Pack.
    """
    from mic.pack import build_context_pack

    text = build_context_pack(memory, task, budget=budget, top_k=top_k)

    if out:
        Path(out).write_text(text, encoding="utf-8")
        console.print(f"[green]✓ Context pack written to {out}[/green]")
    else:
        console.print(text)


@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask Gemma using .mic memory."),
    memory: str = typer.Option(..., "--memory", "-m", help="Path to .mic memory file."),
    backend: str = typer.Option("ollama", "--backend", help="ollama | llamacpp | openai-compatible"),
    model: str = typer.Option("gemma4:latest", "--model", help="Local model name/tag."),
):
    """
    Ask Gemma using local .mic memory.
    """
    from mic.harness import ask_with_memory

    console.print(
        Panel.fit(
            f"[bold]MICode Tutor Ask[/bold]\n"
            f"backend={backend}\n"
            f"model={model}\n"
            f"memory={memory}",
            style="cyan",
        )
    )

    answer = ask_with_memory(memory, question, backend=backend, model=model)
    console.print(answer)


@app.command()
def test(
    task: str = typer.Argument(..., help="Test generation task."),
    memory: str = typer.Option(..., "--memory", "-m", help="Path to .mic memory file."),
    backend: str = typer.Option("ollama", "--backend", help="ollama | llamacpp | openai-compatible"),
    model: str = typer.Option("gemma4:latest", "--model", help="Local model name/tag."),
):
    """
    Generate tests using Gemma and .mic memory.
    """
    from mic.harness import generate_tests

    console.print(
        Panel.fit(
            f"[bold]MICode Tutor Test Generation[/bold]\n"
            f"backend={backend}\n"
            f"model={model}\n"
            f"memory={memory}",
            style="green",
        )
    )

    answer = generate_tests(memory, task, backend=backend, model=model)
    console.print(answer)


@app.command()
def plan(
    task: str = typer.Argument(..., help="Patch planning task."),
    memory: str = typer.Option(..., "--memory", "-m", help="Path to .mic memory file."),
    backend: str = typer.Option("ollama", "--backend", help="ollama | llamacpp | openai-compatible"),
    model: str = typer.Option("gemma4:latest", "--model", help="Local model name/tag."),
):
    """
    Generate a safe patch plan. Does not modify files.
    """
    from mic.harness import plan_with_memory

    console.print(
        Panel.fit(
            f"[bold]MICode Tutor Patch Plan[/bold]\n"
            f"backend={backend}\n"
            f"model={model}\n"
            f"memory={memory}",
            style="magenta",
        )
    )

    answer = plan_with_memory(memory, task, backend=backend, model=model)
    console.print(answer)


@app.command()
def patch(
    task: str = typer.Argument(..., help="Patch proposal task."),
    memory: str = typer.Option(..., "--memory", "-m", help="Path to .mic memory file."),
    backend: str = typer.Option("ollama", "--backend", help="ollama | llamacpp | openai-compatible"),
    model: str = typer.Option("gemma4:latest", "--model", help="Local model name/tag."),
    out: str | None = typer.Option(None, "--out", "-o", help="Write patch proposal to file."),
):
    """
    Generate a patch proposal for human review. Does not apply changes.
    """
    from mic.harness import generate_patch

    console.print(
        Panel.fit(
            f"[bold]MICode Tutor Patch Proposal[/bold]\n"
            f"backend={backend}\n"
            f"model={model}\n"
            f"memory={memory}\n"
            f"mode=proposal_only",
            style="yellow",
        )
    )

    answer = generate_patch(memory, task, backend=backend, model=model)

    if out:
        Path(out).write_text(answer, encoding="utf-8")
        console.print(f"[green]✓ Patch proposal written to {out}[/green]")
    else:
        console.print(answer)


@app.command()
def demo():
    """
    Run the built-in MICode Tutor demo.
    """
    from mic.demo import run_demo

    run_demo()


@app.command()
def doctor():
    """
    Check local MICode Tutor environment.
    """
    import inspect
    import mic
    import mic.cli
    import mic.gemma
    import mic.harness

    console.print(Panel.fit("MICode Tutor Doctor", style="bold cyan"))

    console.print(f"[bold]mic package:[/bold] {inspect.getfile(mic)}")
    console.print(f"[bold]mic.cli:[/bold] {inspect.getfile(mic.cli)}")
    console.print(f"[bold]mic.gemma:[/bold] {inspect.getfile(mic.gemma)}")
    console.print(f"[bold]mic.harness:[/bold] {inspect.getfile(mic.harness)}")

    console.print("\n[bold]Ollama endpoint:[/bold] http://localhost:11434")
    try:
        import requests

        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        console.print(f"[green]✓ Ollama reachable[/green] {r.text[:500]}")
    except Exception as e:
        console.print(f"[red]✗ Ollama not reachable:[/red] {e}")

    console.print("\n[bold]Current generate_ollama source snippet:[/bold]")
    src = inspect.getsource(mic.gemma.generate_ollama)
    console.print(src[:1600])


if __name__ == "__main__":
    app()

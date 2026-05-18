from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from mic.schema import MicMemory

console = Console()


def inspect_memory(memory_path: str):
    mem = MicMemory.load(memory_path)

    console.print(Panel.fit(f"{mem.format} v{mem.version} — {mem.kind}", style="bold cyan"))

    console.print(f"[bold]Repo:[/bold] {mem.repo.get('name')}")
    console.print(f"[bold]Languages:[/bold] {', '.join(mem.repo.get('languages', []))}")
    console.print(f"[bold]Files:[/bold] {len(mem.files)}")
    console.print(f"[bold]Symbols:[/bold] {len(mem.symbols)}")
    console.print(f"[bold]Relations:[/bold] {len(mem.relations)}")
    console.print(f"[bold]State tokens:[/bold] {len(mem.state_tokens)}")

    console.print("\n[bold green]Capabilities[/bold green]")
    for c in mem.capabilities:
        console.print(f"  ✓ {c}")

    table = Table(title="Top Files")
    table.add_column("Path")
    table.add_column("Summary")
    table.add_column("Exports")
    for f in mem.files[:10]:
        table.add_row(f.path, f.summary[:90], ", ".join(f.exports[:6]))
    console.print(table)

    if mem.symbols:
        st = Table(title="Top Symbols")
        st.add_column("Symbol")
        st.add_column("Kind")
        st.add_column("Path")
        st.add_column("Summary")
        for s in mem.symbols[:10]:
            st.add_row(s.name, s.kind, s.path, s.summary[:90])
        console.print(st)


import os
import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

backend_app = typer.Typer(help="Manage local Gemma runtimes: Ollama and llama.cpp")
console = Console()


DEFAULT_GGUF = "/root/autodl-tmp/models/micode-gemma4-zoo/gguf/gemma4-e4b-q4_k_m.gguf"
DEFAULT_OLLAMA_MODELS = "/root/autodl-tmp/ollama"
DEFAULT_LLAMA_CPP_DIR = "/root/autodl-tmp/llama.cpp"
DEFAULT_LLAMA_LOG = "/root/autodl-tmp/llama_server.log"


def run(cmd: list[str], check: bool = True, cwd: str | None = None):
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    return subprocess.run(cmd, check=check, cwd=cwd)


def shell(cmd: str, check: bool = True, cwd: str | None = None):
    console.print(f"[dim]$ {cmd}[/dim]")
    return subprocess.run(cmd, shell=True, check=check, cwd=cwd)


@backend_app.command("doctor")
def doctor():
    """
    Check local runtime environment.
    """
    console.print(Panel.fit("MICode Backend Doctor", style="bold cyan"))

    table = Table(title="Runtime checks")
    table.add_column("Component")
    table.add_column("Status")
    table.add_column("Details")

    # GPU
    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.check_output(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], text=True)
            table.add_row("GPU", "✓", out.strip())
        except Exception as e:
            table.add_row("GPU", "?", str(e))
    else:
        table.add_row("GPU", "not found", "nvidia-smi unavailable")

    # Ollama
    if shutil.which("ollama"):
        try:
            out = subprocess.check_output(["ollama", "--version"], text=True, stderr=subprocess.STDOUT)
            table.add_row("Ollama", "✓", out.strip())
        except Exception as e:
            table.add_row("Ollama", "?", str(e))
    else:
        table.add_row("Ollama", "not found", "Install from https://ollama.com or use offline package")

    # llama.cpp
    llama_server = Path(DEFAULT_LLAMA_CPP_DIR) / "build/bin/llama-server"
    if llama_server.exists():
        table.add_row("llama.cpp", "✓", str(llama_server))
    else:
        table.add_row("llama.cpp", "not built", str(llama_server))

    # GGUF
    ggufs = list(Path("/root/autodl-tmp").glob("**/*.gguf"))
    table.add_row("GGUF models", str(len(ggufs)), "\n".join(str(p) for p in ggufs[:5]))

    console.print(table)

    console.print("\n[bold]Recommended next steps[/bold]")
    console.print("1. If you have a GGUF model on USB/local disk:")
    console.print("   mic backend ollama-create --gguf /path/to/model.gguf --name gemma4:latest")
    console.print("2. Start Ollama:")
    console.print("   mic backend ollama-start")
    console.print("3. Or build/start llama.cpp:")
    console.print("   mic backend llamacpp-build")
    console.print("   mic backend llamacpp-start --gguf /path/to/model.gguf")


@backend_app.command("ollama-start")
def ollama_start(
    models_dir: str = typer.Option(DEFAULT_OLLAMA_MODELS, "--models-dir"),
    host: str = typer.Option("127.0.0.1:11434", "--host"),
    log: str = typer.Option("ollama.log", "--log"),
):
    """
    Start Ollama server with MICode-friendly local settings.
    """
    if not shutil.which("ollama"):
        console.print("[red]ollama not found. Install Ollama first or use llama.cpp backend.[/red]")
        raise typer.Exit(1)

    Path(models_dir).mkdir(parents=True, exist_ok=True)

    env_lines = [
        f"export OLLAMA_MODELS={models_dir}",
        f"export OLLAMA_HOST={host}",
        "export OLLAMA_KEEP_ALIVE=30m",
        "export OLLAMA_NUM_PARALLEL=1",
        "export OLLAMA_MAX_LOADED_MODELS=1",
        "export OLLAMA_FLASH_ATTENTION=true",
        "export OLLAMA_KV_CACHE_TYPE=q8_0",
    ]

    cmd = " && ".join(env_lines + [f"nohup ollama serve > {log} 2>&1 &"])
    shell("pkill ollama || true", check=False)
    shell(cmd)

    console.print(f"[green]✓ Ollama starting on {host}[/green]")
    console.print(f"[dim]log: {log}[/dim]")
    console.print("Check with: curl http://localhost:11434/api/tags")


@backend_app.command("ollama-create")
def ollama_create(
    gguf: str = typer.Option(DEFAULT_GGUF, "--gguf", help="Path to local GGUF model file."),
    name: str = typer.Option("gemma4:latest", "--name", help="Ollama model name/tag."),
    ctx: int = typer.Option(2048, "--ctx"),
    predict: int = typer.Option(512, "--predict"),
):
    """
    Create an Ollama model from a local GGUF file.

    Works with offline/USB-delivered GGUF models.
    """
    gguf_path = Path(gguf)
    if not gguf_path.exists():
        console.print(f"[red]GGUF not found:[/red] {gguf}")
        raise typer.Exit(1)

    modelfile = gguf_path.parent / f"Modelfile.{name.replace(':', '-')}"
    modelfile.write_text(f'''FROM {gguf_path}

PARAMETER temperature 0.2
PARAMETER num_ctx {ctx}
PARAMETER num_predict {predict}
PARAMETER num_batch 128

SYSTEM """
You are Gemma 4 running as a local offline coding tutor.
Use only the MICode Context Pack.
Cite file paths, symbol names, and line ranges when available.
Do not include hidden reasoning.
"""
''', encoding="utf-8")

    console.print(f"[green]✓ Wrote Modelfile:[/green] {modelfile}")
    run(["ollama", "create", name, "-f", str(modelfile)])
    run(["ollama", "list"], check=False)


@backend_app.command("ollama-test")
def ollama_test(
    model: str = typer.Option("gemma4:latest", "--model"),
):
    """
    Smoke-test Ollama chat endpoint with think=false.
    """
    import requests

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say hello in one sentence."}],
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 2048,
            "num_predict": 64,
            "num_batch": 128,
        },
    }

    r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    console.print(data.get("message", {}).get("content", data))


@backend_app.command("llamacpp-build")
def llamacpp_build(
    dir: str = typer.Option(DEFAULT_LLAMA_CPP_DIR, "--dir"),
    cuda: bool = typer.Option(True, "--cuda/--no-cuda"),
):
    """
    Clone and build llama.cpp.

    Requires internet unless llama.cpp is already present.
    """
    root = Path(dir)

    if not root.exists():
        run(["git", "clone", "https://github.com/ggerganov/llama.cpp", str(root)])
    else:
        console.print(f"[yellow]llama.cpp already exists:[/yellow] {root}")

    cmake_cmd = ["cmake", "-B", "build"]
    if cuda:
        cmake_cmd.append("-DGGML_CUDA=ON")

    run(cmake_cmd, cwd=str(root))
    run(["cmake", "--build", "build", "-j"], cwd=str(root))

    server = root / "build/bin/llama-server"
    if server.exists():
        console.print(f"[green]✓ Built llama-server:[/green] {server}")
    else:
        console.print("[red]llama-server not found after build.[/red]")


@backend_app.command("llamacpp-start")
def llamacpp_start(
    gguf: str = typer.Option(DEFAULT_GGUF, "--gguf"),
    dir: str = typer.Option(DEFAULT_LLAMA_CPP_DIR, "--dir"),
    port: int = typer.Option(8080, "--port"),
    ctx: int = typer.Option(2048, "--ctx"),
    ngl: int = typer.Option(99, "--ngl"),
    log: str = typer.Option(DEFAULT_LLAMA_LOG, "--log"),
):
    """
    Start llama.cpp server for local GGUF inference.
    """
    server = Path(dir) / "build/bin/llama-server"
    if not server.exists():
        console.print(f"[red]llama-server not found:[/red] {server}")
        console.print("Run: mic backend llamacpp-build")
        raise typer.Exit(1)

    gguf_path = Path(gguf)
    if not gguf_path.exists():
        console.print(f"[red]GGUF not found:[/red] {gguf}")
        raise typer.Exit(1)

    shell("pkill llama-server || true", check=False)

    # Try optimized flags. If unsupported, user can check log and rerun manually.
    cmd = (
        f"nohup {server} "
        f"-m {gguf_path} "
        f"--host 127.0.0.1 "
        f"--port {port} "
        f"-c {ctx} "
        f"-ngl {ngl} "
        f"-b 512 "
        f"-ub 256 "
        f"-fa "
        f"--jinja "
        f"> {log} 2>&1 &"
    )
    shell(cmd)

    console.print(f"[green]✓ llama.cpp server starting on port {port}[/green]")
    console.print(f"[dim]log: {log}[/dim]")
    console.print(f"Test: curl http://localhost:{port}/completion -H 'Content-Type: application/json' -d '{{\"prompt\":\"Say hello.\",\"n_predict\":32}}'")


@backend_app.command("modelcard")
def modelcard(
    gguf: str = typer.Option(DEFAULT_GGUF, "--gguf"),
    out: str = typer.Option("MODEL_BACKEND_CARD.md", "--out"),
):
    """
    Generate a local backend/model card for README or offline deployment docs.
    """
    gguf_path = Path(gguf)
    size = gguf_path.stat().st_size / (1024 ** 3) if gguf_path.exists() else 0

    text = f"""# MICode Tutor Local Backend Card

## Model Artifact

- GGUF: `{gguf_path}`
- Size: `{size:.2f} GiB`
- Intended model: Gemma 4 local instruction model
- Quantization: inferred from filename

## Supported Runtimes

### Ollama

Create model from local GGUF:

```bash
mic backend ollama-start
mic backend ollama-create --gguf {gguf_path} --name gemma4:latest
mic backend ollama-test --model gemma4:latest
```

Run MICode Tutor:

```bash
mic ask "Where is JWT verified?" \\
  --memory edu_auth_service.mic \\
  --backend ollama \\
  --model gemma4:latest
```

### llama.cpp

Build and start llama.cpp:

```bash
mic backend llamacpp-build
mic backend llamacpp-start --gguf {gguf_path}
```

Run MICode Tutor:

```bash
mic ask "Where is JWT verified?" \\
  --memory edu_auth_service.mic \\
  --backend llamacpp \\
  --model gemma4
```

## Offline / USB Deployment

This backend can be set up without cloud model downloads if the GGUF file is provided through:

- USB drive
- local school server
- preloaded classroom machine
- offline dataset package

## Why this matters

MICode Tutor targets classrooms and privacy-sensitive environments where cloud coding assistants are unavailable. The `.mic` memory file reduces repository context into compact evidence packs, making local quantized Gemma inference practical.
"""

    Path(out).write_text(text, encoding="utf-8")
    console.print(f"[green]✓ Wrote backend model card:[/green] {out}")
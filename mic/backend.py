import os
import shutil
import subprocess
import time
from pathlib import Path

import requests
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

backend_app = typer.Typer(help="Manage local Gemma runtimes: Ollama and llama.cpp")
console = Console()

DEFAULT_GGUF = "/root/autodl-tmp/models/micode-gemma4-zoo/gguf/gemma4-e4b-q4_k_m.gguf"
DEFAULT_E2B_GGUF = "/root/autodl-tmp/models/micode-gemma4-zoo/gguf/gemma4-e2b-q4_k_m.gguf"
DEFAULT_OLLAMA_MODELS = "/root/autodl-tmp/ollama"
DEFAULT_LLAMA_LOG = "/root/autodl-tmp/llama_cpp_python_server.log"
DEFAULT_LLAMA_PORT = 8080


def run(cmd: list[str], check: bool = True, cwd: str | None = None, env: dict | None = None):
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    return subprocess.run(cmd, check=check, cwd=cwd, env=env)


def shell(cmd: str, check: bool = True, cwd: str | None = None):
    console.print(f"[dim]$ {cmd}[/dim]")
    return subprocess.run(cmd, shell=True, check=check, cwd=cwd)


def has_glibcxx_3430(path: str) -> bool:
    try:
        out = subprocess.check_output(f"strings {path} | grep GLIBCXX_3.4.30", shell=True, text=True)
        return "GLIBCXX_3.4.30" in out
    except Exception:
        return False


def recommended_libstdcpp() -> str | None:
    candidates = [
        "/usr/lib/x86_64-linux-gnu/libstdc++.so.6",
        "/usr/local/lib64/libstdc++.so.6",
        "/usr/local/lib/libstdc++.so.6",
    ]
    for c in candidates:
        if Path(c).exists() and has_glibcxx_3430(c):
            return c
    return None


def wait_for_openai_server(port: int, timeout_s: int = 240) -> bool:
    url = f"http://127.0.0.1:{port}/v1/models"
    for i in range(timeout_s // 2):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                console.print("[green]✓ llama.cpp OpenAI-compatible server ready[/green]")
                console.print(r.text[:500])
                return True
        except Exception:
            pass
        console.print(f"[dim]waiting for llama.cpp server... {i + 1}[/dim]")
        time.sleep(2)
    return False


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

    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                text=True,
            )
            table.add_row("GPU", "✓", out.strip())
        except Exception as e:
            table.add_row("GPU", "?", str(e))
    else:
        table.add_row("GPU", "not found", "nvidia-smi unavailable")

    if shutil.which("ollama"):
        try:
            out = subprocess.check_output(["ollama", "--version"], text=True, stderr=subprocess.STDOUT)
            table.add_row("Ollama", "✓", out.strip())
        except Exception as e:
            table.add_row("Ollama", "?", str(e))
    else:
        table.add_row("Ollama", "not found", "Install Ollama or use llama.cpp backend")

    try:
        import llama_cpp  # noqa
        table.add_row("llama-cpp-python", "✓", "Python package importable")
    except Exception as e:
        table.add_row("llama-cpp-python", "?", str(e)[:120])

    conda_lib = str(Path(os.environ.get("CONDA_PREFIX", "/root/miniconda3")) / "lib/libstdc++.so.6")
    sys_lib = "/usr/lib/x86_64-linux-gnu/libstdc++.so.6"

    table.add_row(
        "conda libstdc++",
        "✓" if Path(conda_lib).exists() else "missing",
        f"{conda_lib} GLIBCXX_3.4.30={has_glibcxx_3430(conda_lib) if Path(conda_lib).exists() else False}",
    )
    table.add_row(
        "system libstdc++",
        "✓" if Path(sys_lib).exists() else "missing",
        f"{sys_lib} GLIBCXX_3.4.30={has_glibcxx_3430(sys_lib) if Path(sys_lib).exists() else False}",
    )

    ggufs = list(Path("/root/autodl-tmp").glob("**/*.gguf"))
    table.add_row("GGUF models", str(len(ggufs)), "\n".join(str(p) for p in ggufs[:6]))

    console.print(table)

    console.print("\n[bold]Recommended commands[/bold]")
    console.print("  mic backend install llamacpp")
    console.print("  mic backend llamacpp-start --gguf /path/to/model.gguf")
    console.print("  mic backend llamacpp-test")
    console.print("  mic backend ollama-start")
    console.print("  mic backend ollama-test --model gemma4:latest")


@backend_app.command("install")
def install_backend(name: str):
    """
    Guided backend installer.

    Examples:
      mic backend install llamacpp
      mic backend install ollama
    """
    if name not in {"llamacpp", "llama.cpp", "ollama"}:
        console.print(f"[red]Unknown backend:[/red] {name}")
        console.print("Supported: llamacpp, ollama")
        raise typer.Exit(1)

    if name == "ollama":
        console.print(Panel.fit("Ollama backend setup", style="bold cyan"))
        if shutil.which("ollama"):
            console.print("[green]✓ Ollama already installed[/green]")
            console.print("Next:")
            console.print("  mic backend ollama-start")
            console.print("  mic backend ollama-test --model gemma4:latest")
        else:
            console.print("[yellow]Ollama is platform-specific and not installed.[/yellow]")
            console.print("Install Ollama from https://ollama.com or use an offline package.")
        return

    console.print(Panel.fit("Installing llama.cpp backend via llama-cpp-python", style="bold cyan"))

    console.print("[bold]Step 1[/bold] Install llama-cpp-python server package")
    cuda_cmd = (
        'pip install "llama-cpp-python[server]" '
        "--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124"
    )
    r = subprocess.run(cuda_cmd, shell=True)

    if r.returncode != 0:
        console.print("[yellow]CUDA wheel install failed. Falling back to default pip install.[/yellow]")
        r = subprocess.run('pip install "llama-cpp-python[server]"', shell=True)

    if r.returncode != 0:
        console.print("[red]Failed to install llama-cpp-python.[/red]")
        raise typer.Exit(1)

    console.print("[green]✓ llama-cpp-python installed[/green]")

    console.print("[bold]Step 2[/bold] Check C++ runtime compatibility")
    lib = recommended_libstdcpp()
    if lib:
        console.print(f"[green]✓ Found compatible libstdc++:[/green] {lib}")
        Path(".micode_backend_env").write_text(f"MICODE_LLAMACPP_LD_PRELOAD={lib}\n", encoding="utf-8")
        console.print("[green]✓ Wrote .micode_backend_env[/green]")
    else:
        console.print("[yellow]No system libstdc++ with GLIBCXX_3.4.30 found.[/yellow]")
        console.print("If llama.cpp fails to start, run:")
        console.print("  conda install -y -c conda-forge 'libstdcxx-ng>=12'")

    console.print("\n[green]✓ llama.cpp backend install complete[/green]")
    console.print("Start server:")
    console.print(f"  mic backend llamacpp-start --gguf {DEFAULT_E2B_GGUF}")
    console.print("Test server:")
    console.print("  mic backend llamacpp-test")


@backend_app.command("llamacpp-start")
def llamacpp_start(
    gguf: str = typer.Option(DEFAULT_E2B_GGUF, "--gguf", help="Path to local GGUF model."),
    port: int = typer.Option(DEFAULT_LLAMA_PORT, "--port"),
    ctx: int = typer.Option(2048, "--ctx"),
    batch: int = typer.Option(512, "--batch"),
    gpu_layers: int = typer.Option(-1, "--gpu-layers"),
    log: str = typer.Option(DEFAULT_LLAMA_LOG, "--log"),
    wait: bool = typer.Option(True, "--wait/--no-wait"),
):
    """
    Start llama-cpp-python OpenAI-compatible server.

    This command automatically applies LD_PRELOAD when a newer system libstdc++
    is needed by CUDA llama.cpp wheels.
    """
    gguf_path = Path(gguf)
    if not gguf_path.exists():
        console.print(f"[red]GGUF not found:[/red] {gguf}")
        raise typer.Exit(1)

    lib = recommended_libstdcpp()
    preload = f"LD_PRELOAD={lib} " if lib else ""

    shell("pkill -f llama_cpp.server || true", check=False)

    cmd = (
        f"nohup env {preload}python -m llama_cpp.server "
        f"--model {gguf_path} "
        f"--host 127.0.0.1 "
        f"--port {port} "
        f"--n_ctx {ctx} "
        f"--n_batch {batch} "
        f"--n_gpu_layers {gpu_layers} "
        f"> {log} 2>&1 &"
    )

    shell(cmd)

    console.print(f"[green]✓ llama-cpp-python server starting on port {port}[/green]")
    console.print(f"[dim]model: {gguf_path}[/dim]")
    console.print(f"[dim]log: {log}[/dim]")
    if lib:
        console.print(f"[dim]auto LD_PRELOAD: {lib}[/dim]")

    if wait:
        ok = wait_for_openai_server(port, timeout_s=240)
        if not ok:
            console.print("[red]llama.cpp server did not become ready. Last log lines:[/red]")
            shell(f"tail -120 {log}", check=False)
            raise typer.Exit(1)


@backend_app.command("llamacpp-test")
def llamacpp_test(
    port: int = typer.Option(DEFAULT_LLAMA_PORT, "--port"),
):
    """
    Smoke-test llama.cpp OpenAI-compatible server.
    """
    payload = {
        "model": "gemma4",
        "messages": [{"role": "user", "content": "Say hello in one sentence."}],
        "temperature": 0.2,
        "max_tokens": 64,
    }

    r = requests.post(f"http://127.0.0.1:{port}/v1/chat/completions", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    console.print(data["choices"][0]["message"]["content"])


@backend_app.command("ollama-start")
def ollama_start(
    models_dir: str = typer.Option(DEFAULT_OLLAMA_MODELS, "--models-dir"),
    host: str = typer.Option("127.0.0.1:11434", "--host"),
    log: str = typer.Option("ollama.log", "--log"),
):
    """
    Start Ollama server with MICode-friendly settings.
    """
    if not shutil.which("ollama"):
        console.print("[red]ollama not found. Install Ollama first or use llama.cpp backend.[/red]")
        raise typer.Exit(1)

    Path(models_dir).mkdir(parents=True, exist_ok=True)

    shell("pkill ollama || true", check=False)

    cmd = (
        f"export OLLAMA_MODELS={models_dir} && "
        f"export OLLAMA_HOST={host} && "
        "export OLLAMA_KEEP_ALIVE=30m && "
        "export OLLAMA_NUM_PARALLEL=1 && "
        "export OLLAMA_MAX_LOADED_MODELS=1 && "
        "export OLLAMA_FLASH_ATTENTION=true && "
        "export OLLAMA_KV_CACHE_TYPE=q8_0 && "
        f"nohup ollama serve > {log} 2>&1 &"
    )
    shell(cmd)

    console.print(f"[green]✓ Ollama starting on {host}[/green]")
    console.print(f"[dim]log: {log}[/dim]")


@backend_app.command("ollama-create")
def ollama_create(
    gguf: str = typer.Option(DEFAULT_GGUF, "--gguf", help="Path to local GGUF model file."),
    name: str = typer.Option("gemma4:latest", "--name", help="Ollama model name/tag."),
    ctx: int = typer.Option(2048, "--ctx"),
    predict: int = typer.Option(512, "--predict"),
):
    """
    Create an Ollama model from a local GGUF file.
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
    Smoke-test Ollama chat endpoint.
    """
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


@backend_app.command("modelcard")
def modelcard(
    gguf: str = typer.Option(DEFAULT_GGUF, "--gguf"),
    out: str = typer.Option("MODEL_BACKEND_CARD.md", "--out"),
):
    """
    Generate a local backend/model card.
    """
    gguf_path = Path(gguf)
    size = gguf_path.stat().st_size / (1024 ** 3) if gguf_path.exists() else 0

    text = f"""# MICode Tutor Local Backend Card

## Model Artifact

- GGUF: `{gguf_path}`
- Size: `{size:.2f} GiB`
- Runtime options: Ollama, llama.cpp via llama-cpp-python

## Ollama

```bash
mic backend ollama-start
mic backend ollama-create --gguf {gguf_path} --name gemma4:latest
mic backend ollama-test --model gemma4:latest
```

## llama.cpp

```bash
mic backend install llamacpp
mic backend llamacpp-start --gguf {gguf_path}
mic backend llamacpp-test
```

## MICode Tutor

```bash
mic ask "Where is JWT verified?" \\
  --memory edu_auth_service.mic \\
  --backend ollama \\
  --model gemma4:latest

mic ask "Where is JWT verified?" \\
  --memory edu_auth_service.mic \\
  --backend llamacpp \\
  --model gemma4
```

## Offline Deployment

GGUF models can be delivered by USB drive, local school server, or preloaded classroom machine.
"""
    Path(out).write_text(text, encoding="utf-8")
    console.print(f"[green]✓ Wrote backend model card:[/green] {out}")
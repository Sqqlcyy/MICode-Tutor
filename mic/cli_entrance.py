import ast
import json
import re
import time
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import Any

import requests
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pydantic import BaseModel, Field

app = typer.Typer(help="MICode Tutor: Offline codebase memory for Gemma 4")
console = Console()


# =========================
# Schema
# =========================

class MicFile(BaseModel):
    id: str
    path: str
    language: str = "python"
    role: str = ""
    imports: list[str] = Field(default_factory=list)
    exports: list[str] = Field(default_factory=list)
    is_test: bool = False
    summary: str = ""


class MicSymbol(BaseModel):
    id: str
    kind: str
    name: str
    path: str
    start_line: int = 0
    end_line: int = 0
    signature: str = ""
    summary: str = ""
    calls: list[str] = Field(default_factory=list)
    called_by: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    evidence: str = ""


class MicRelation(BaseModel):
    source: str
    target: str
    type: str
    confidence: float = 1.0


class MicStateToken(BaseModel):
    state_id: str
    target_id: str
    state_type: str = "hybrid_text_state"
    tokens: list[str] = Field(default_factory=list)


class MicMemory(BaseModel):
    format: str = "MIC"
    version: str = "0.1"
    kind: str = "Machine-Interpretable Code"
    created_by: str = "MICSDK"
    repo: dict[str, Any] = Field(default_factory=dict)

    capabilities: list[str] = Field(default_factory=lambda: [
        "repo_qa",
        "symbol_lookup",
        "architecture_explanation",
        "test_generation",
        "patch_planning",
        "error_triage",
    ])

    memory_layers: dict[str, Any] = Field(default_factory=lambda: {
        "file_cards": True,
        "symbol_cards": True,
        "relations": True,
        "summaries": True,
        "evidence_refs": True,
        "state_tokens": True,
        "embeddings": False,
        "mii_neural_state": "future",
    })

    files: list[MicFile] = Field(default_factory=list)
    symbols: list[MicSymbol] = Field(default_factory=list)
    relations: list[MicRelation] = Field(default_factory=list)
    state_tokens: list[MicStateToken] = Field(default_factory=list)
    agent_recipes: list[dict[str, Any]] = Field(default_factory=list)

    def save(self, path: str):
        Path(path).write_text(
            json.dumps(self.model_dump(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str):
        return cls(**json.loads(Path(path).read_text(encoding="utf-8")))


# =========================
# Utils
# =========================

IGNORE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".ruff_cache"
}

TEXT_EXTS = {".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".sh", ".ts", ".tsx", ".js"}


def stable_id(*parts: str) -> str:
    raw = "::".join(parts)
    h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    clean = re.sub(r"[^a-zA-Z0-9_]+", "_", "_".join(parts))[:48]
    return f"{clean}_{h}"


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def iter_repo_files(repo_path: str):
    root = Path(repo_path)
    for p in root.rglob("*"):
        if p.is_file() and not should_ignore(p) and p.suffix in TEXT_EXTS:
            yield p


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except Exception:
            return ""
    except Exception:
        return ""


def line_slice(text: str, start: int, end: int) -> str:
    lines = text.splitlines()
    start = max(1, start)
    end = min(len(lines), end)
    return "\n".join(lines[start - 1:end])


def simple_tokens(text: str, max_tokens: int = 48) -> list[str]:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    words = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+", text.lower())
    stop = {
        "the", "a", "an", "and", "or", "to", "of", "in", "for", "with",
        "is", "are", "on", "by", "from", "this", "that", "def", "class",
        "return", "import", "as", "if", "else", "elif", "true", "false", "none"
    }
    out, seen = [], set()
    for w in words:
        if w in stop or len(w) <= 1:
            continue
        if w not in seen:
            out.append(w)
            seen.add(w)
        if len(out) >= max_tokens:
            break
    return out


def rough_summary_from_path(path: str) -> str:
    p = path.lower()
    if "auth" in p:
        return "Authentication-related code."
    if "config" in p:
        return "Configuration and settings code."
    if "test" in p:
        return "Tests and validation code."
    if "middleware" in p:
        return "Middleware and request processing code."
    if "db" in p or "database" in p:
        return "Database or persistence code."
    if "main" in p:
        return "Application entrypoint."
    return "Repository source file."


# =========================
# Parser / Compiler
# =========================

def parse_python_file(root: Path, path: Path):
    rel = str(path.relative_to(root)).replace("\\", "/")
    text = read_text_safe(path)

    try:
        tree = ast.parse(text)
    except SyntaxError:
        f = MicFile(
            id=stable_id("file", rel),
            path=rel,
            language="python",
            role=rough_summary_from_path(rel),
            is_test=("test" in rel.lower()),
            summary=rough_summary_from_path(rel),
        )
        return f, [], []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

    symbols = []
    exports = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            kind = "class" if isinstance(node, ast.ClassDef) else "function"
            start = getattr(node, "lineno", 1)
            end = getattr(node, "end_lineno", start)
            evidence = line_slice(text, start, end)
            doc = ast.get_docstring(node) or ""

            if kind == "function":
                args = [a.arg for a in node.args.args]
                signature = f"def {name}({', '.join(args)})"
            else:
                signature = f"class {name}"

            summary = doc.strip().split("\n")[0] if doc else f"{kind.title()} `{name}` defined in `{rel}`."

            symbols.append(MicSymbol(
                id=stable_id("sym", rel, name),
                kind=kind,
                name=name,
                path=rel,
                start_line=start,
                end_line=end,
                signature=signature,
                summary=summary,
                evidence=evidence[:5000],
            ))
            exports.append(name)

    file_summary = rough_summary_from_path(rel)
    if exports:
        file_summary += f" Defines: {', '.join(exports[:10])}."

    f = MicFile(
        id=stable_id("file", rel),
        path=rel,
        language="python",
        role=rough_summary_from_path(rel),
        imports=sorted(set([x for x in imports if x])),
        exports=exports,
        is_test=("test" in rel.lower()),
        summary=file_summary,
    )

    return f, symbols, []


def parse_text_file(root: Path, path: Path):
    rel = str(path.relative_to(root)).replace("\\", "/")
    text = read_text_safe(path)
    title = ""

    for line in text.splitlines()[:30]:
        if line.strip().startswith("#"):
            title = line.strip("# ").strip()
            break

    f = MicFile(
        id=stable_id("file", rel),
        path=rel,
        language=path.suffix.lstrip(".") or "text",
        role=rough_summary_from_path(rel),
        summary=title or rough_summary_from_path(rel),
        is_test=("test" in rel.lower()),
    )
    return f, [], []


def parse_file(root: Path, path: Path):
    if path.suffix == ".py":
        return parse_python_file(root, path)
    return parse_text_file(root, path)


def build_state_for_file(f: MicFile) -> MicStateToken:
    base = f"{f.path} {f.role} {f.summary} {' '.join(f.imports)} {' '.join(f.exports)}"
    return MicStateToken(
        state_id=stable_id("state", f.id),
        target_id=f.id,
        state_type="hybrid_file_state",
        tokens=simple_tokens(base, 40),
    )


def build_state_for_symbol(s: MicSymbol) -> MicStateToken:
    base = f"{s.path} {s.name} {s.kind} {s.signature} {s.summary} {s.evidence[:1200]}"
    return MicStateToken(
        state_id=stable_id("state", s.id),
        target_id=s.id,
        state_type="hybrid_symbol_state",
        tokens=simple_tokens(base, 64),
    )


def infer_test_links(symbols: list[MicSymbol]):
    tests = [s for s in symbols if "test" in s.path.lower() or s.name.startswith("test_")]
    normals = [s for s in symbols if s not in tests]

    for s in normals:
        linked = []
        for t in tests:
            hay = f"{t.name} {t.summary} {t.evidence}".lower()
            if s.name.lower() in hay:
                linked.append(f"{t.path}::{t.name}")
        s.tests = linked[:5]


def infer_relations(symbols: list[MicSymbol]) -> list[MicRelation]:
    relations = []
    by_name = {s.name: s for s in symbols}

    for s in symbols:
        ev = s.evidence or ""
        for name, target in by_name.items():
            if name == s.name:
                continue
            if f"{name}(" in ev:
                s.calls.append(name)
                target.called_by.append(f"{s.path}::{s.name}")
                relations.append(MicRelation(
                    source=f"{s.path}::{s.name}",
                    target=f"{target.path}::{target.name}",
                    type="calls",
                    confidence=0.65,
                ))
    return relations


def compile_repo(repo_path: str) -> MicMemory:
    root = Path(repo_path).resolve()
    if not root.exists():
        raise FileNotFoundError(repo_path)

    files, symbols, relations = [], [], []

    for p in iter_repo_files(str(root)):
        f, syms, rels = parse_file(root, p)
        files.append(f)
        symbols.extend(syms)
        relations.extend(rels)

    infer_test_links(symbols)
    relations.extend(infer_relations(symbols))

    state_tokens = []
    for f in files:
        state_tokens.append(build_state_for_file(f))
    for s in symbols:
        state_tokens.append(build_state_for_symbol(s))

    langs = sorted(set(f.language for f in files if f.language))

    return MicMemory(
        repo={
            "name": root.name,
            "root": str(root),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "languages": langs,
            "files_count": len(files),
            "symbols_count": len(symbols),
            "relations_count": len(relations),
        },
        files=files,
        symbols=symbols,
        relations=relations,
        state_tokens=state_tokens,
        agent_recipes=[
            {
                "name": "repo_qa",
                "description": "Search MIC memory, build context pack, ask Gemma 4 for grounded answer.",
                "tools": ["mic_search", "mic_pack", "gemma_generate"],
            },
            {
                "name": "generate_tests",
                "description": "Retrieve target symbol and existing tests, then ask Gemma 4 to generate tests.",
                "tools": ["mic_search", "mic_pack", "gemma_generate"],
            },
            {
                "name": "patch_planning",
                "description": "Retrieve related files and symbols, then ask Gemma 4 for a safe patch plan.",
                "tools": ["mic_search", "mic_pack", "gemma_generate"],
            }
        ],
    )


# =========================
# Inspect
# =========================

def inspect_memory(path: str):
    mem = MicMemory.load(path)
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

    st = Table(title="Top Symbols")
    st.add_column("Symbol")
    st.add_column("Kind")
    st.add_column("Path")
    st.add_column("Summary")
    for s in mem.symbols[:10]:
        st.add_row(s.name, s.kind, s.path, s.summary[:90])
    console.print(st)


# =========================
# Retrieval
# =========================

@dataclass
class SearchResult:
    target_id: str
    target_type: str
    title: str
    path: str
    score: float
    summary: str
    evidence: str = ""
    start_line: int = 0
    end_line: int = 0

    def __str__(self):
        loc = self.path
        if self.start_line:
            loc += f":{self.start_line}-{self.end_line}"
        return f"[{self.score:.3f}] {self.title} | {loc} | {self.summary[:120]}"


def overlap_score(q_tokens: set[str], text: str) -> float:
    toks = set(simple_tokens(text, 160))
    if not q_tokens or not toks:
        return 0.0
    return len(q_tokens & toks) / max(1, len(q_tokens))


def search_memory(memory_path: str, query: str, top_k: int = 5) -> list[SearchResult]:
    mem = MicMemory.load(memory_path)
    q = query.lower()
    q_tokens = set(simple_tokens(query, 80))
    state_by_target = {s.target_id: s.tokens for s in mem.state_tokens}

    results = []

    for s in mem.symbols:
        blob = f"{s.name} {s.kind} {s.path} {s.signature} {s.summary} {s.evidence[:1200]} {' '.join(state_by_target.get(s.id, []))}"
        score = 2.0 * overlap_score(q_tokens, blob)

        if s.name.lower() in q:
            score += 2.0
        if "auth" in q and "auth" in s.path.lower():
            score += 0.9
        if "jwt" in q and ("jwt" in blob.lower() or "token" in blob.lower()):
            score += 1.0
        if "config" in q and "config" in s.path.lower():
            score += 0.9
        if "test" in q and ("test" in s.path.lower() or s.name.startswith("test_")):
            score += 0.8
        if "refresh" in q and "refresh" in blob.lower():
            score += 0.8

        if score > 0:
            results.append(SearchResult(
                target_id=s.id,
                target_type="symbol",
                title=f"{s.path}::{s.name}",
                path=s.path,
                score=score,
                summary=s.summary,
                evidence=s.evidence,
                start_line=s.start_line,
                end_line=s.end_line,
            ))

    for f in mem.files:
        blob = f"{f.path} {f.role} {f.summary} {' '.join(f.imports)} {' '.join(f.exports)} {' '.join(state_by_target.get(f.id, []))}"
        score = 1.2 * overlap_score(q_tokens, blob)

        if "auth" in q and "auth" in f.path.lower():
            score += 0.7
        if "config" in q and "config" in f.path.lower():
            score += 0.7
        if "test" in q and f.is_test:
            score += 0.5
        if "refresh" in q and "refresh" in blob.lower():
            score += 0.5

        if score > 0:
            results.append(SearchResult(
                target_id=f.id,
                target_type="file",
                title=f.path,
                path=f.path,
                score=score,
                summary=f.summary,
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_k]


# =========================
# Pack / Gemma
# =========================

def build_context_pack(memory_path: str, task: str, budget: int = 4000, top_k: int = 8) -> str:
    mem = MicMemory.load(memory_path)
    results = search_memory(memory_path, task, top_k=top_k)

    lines = []
    lines.append("# MICode Context Pack\n")
    lines.append(f"Task: {task}\n")

    lines.append("## Repo")
    lines.append(f"- Name: {mem.repo.get('name')}")
    lines.append(f"- Languages: {', '.join(mem.repo.get('languages', []))}")
    lines.append(f"- Files: {len(mem.files)}")
    lines.append(f"- Symbols: {len(mem.symbols)}\n")

    lines.append("## Relevant Results")
    for i, r in enumerate(results, 1):
        loc = r.path
        if r.start_line:
            loc += f":{r.start_line}-{r.end_line}"
        lines.append(f"{i}. **{r.title}**")
        lines.append(f"   - Type: {r.target_type}")
        lines.append(f"   - Location: `{loc}`")
        lines.append(f"   - Score: {r.score:.3f}")
        lines.append(f"   - Summary: {r.summary}")
    lines.append("")

    lines.append("## Evidence Snippets")
    used = 0
    max_chars = budget * 4

    for r in results:
        if not r.evidence:
            continue
        snippet = r.evidence.strip()
        if used + len(snippet) > max_chars:
            snippet = snippet[:max(0, max_chars - used)]
        if not snippet:
            break

        lines.append(f"### {r.title}")
        if r.start_line:
            lines.append(f"Location: `{r.path}:{r.start_line}-{r.end_line}`")
        else:
            lines.append(f"Location: `{r.path}`")
        lines.append("```python")
        lines.append(snippet)
        lines.append("```\n")

        used += len(snippet)
        if used >= max_chars:
            break

    lines.append("## Instructions for Gemma 4")
    lines.append("- Answer only using the MICode Context Pack above.")
    lines.append("- Cite file paths, symbol names, and line ranges when available.")
    lines.append("- If context is insufficient, say what is missing.")
    lines.append("- Prefer clear explanations for students and practical next steps for developers.")
    lines.append("- Do not claim you inspected files that are not in this context.")

    return "\n".join(lines)


SYSTEM_PROMPT = """You are Gemma 4 running as an offline coding tutor.

You do not have internet access.
You must answer using only the MICode Context Pack provided by the local MICSDK.
Always cite file paths, symbol names, and line ranges when available.
If the context is insufficient, say what is missing.
Prefer clear explanations for students and practical next steps for developers.
Do not claim you inspected files that are not in the context.
"""


def call_ollama(prompt: str, model: str = "gemma4") -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0.2, "num_ctx": 8192},
        },
        timeout=180,
    )
    r.raise_for_status()
    return r.json().get("response", "")


def generate(prompt: str, backend: str, model: str) -> str:
    if backend == "ollama":
        try:
            return call_ollama(prompt, model)
        except Exception as e:
            return (
                "[MICode Tutor fallback]\n"
                "Could not reach local Ollama/Gemma backend.\n"
                f"Error: {e}\n\n"
                "Below is the prompt that would be sent to Gemma 4:\n\n"
                "----- PROMPT START -----\n"
                f"{prompt}\n"
                "----- PROMPT END -----\n"
            )

    return f"[Unsupported backend: {backend}]\n\n{prompt}"


def ask_with_memory(memory_path: str, question: str, backend: str, model: str) -> str:
    pack = build_context_pack(memory_path, question, 4000)
    prompt = f"""{SYSTEM_PROMPT}

{pack}

Question:
{question}

Answer with:
1. Short answer
2. Explanation
3. Evidence
4. Next steps if relevant
"""
    return generate(prompt, backend, model)


def test_with_memory(memory_path: str, task: str, backend: str, model: str) -> str:
    pack = build_context_pack(memory_path, task, 6000)
    prompt = f"""{SYSTEM_PROMPT}

{pack}

Task:
{task}

Generate tests grounded in the context.

Output:
1. Target test file
2. Test code
3. Why these tests are needed
4. Evidence used
"""
    return generate(prompt, backend, model)


def plan_with_memory(memory_path: str, task: str, backend: str, model: str) -> str:
    pack = build_context_pack(memory_path, task, 5000)
    prompt = f"""{SYSTEM_PROMPT}

{pack}

Task:
{task}

Produce a safe patch plan. Do not write code yet.

Output:
1. Files likely to change
2. Symbols involved
3. Step-by-step plan
4. Risks
5. Tests to add
"""
    return generate(prompt, backend, model)


# =========================
# CLI
# =========================

@app.command("compile")
def compile_cmd(
    repo_path: str,
    out: str = typer.Option("repo.mic", "--out", "-o"),
):
    """Compile a repository into a .mic memory file."""
    mem = compile_repo(repo_path)
    mem.save(out)
    console.print(f"[green]✓ MIC memory written to {out}[/green]")


@app.command()
def inspect(memory_path: str):
    """Inspect a .mic memory file."""
    inspect_memory(memory_path)


@app.command()
def search(
    query: str,
    memory: str = typer.Option(..., "--memory", "-m"),
    top_k: int = typer.Option(5, "--top-k", "-k"),
):
    """Search a .mic memory file."""
    results = search_memory(memory, query, top_k)
    for i, r in enumerate(results, 1):
        console.print(f"{i}. {r}")


@app.command()
def pack(
    task: str,
    memory: str = typer.Option(..., "--memory", "-m"),
    budget: int = typer.Option(4000, "--budget", "-b"),
    out: str | None = typer.Option(None, "--out", "-o"),
):
    """Generate a context pack from .mic memory."""
    text = build_context_pack(memory, task, budget)
    if out:
        Path(out).write_text(text, encoding="utf-8")
        console.print(f"[green]✓ Context pack written to {out}[/green]")
    else:
        console.print(text)


@app.command()
def ask(
    question: str,
    memory: str = typer.Option(..., "--memory", "-m"),
    backend: str = typer.Option("ollama", "--backend"),
    model: str = typer.Option("gemma4", "--model"),
):
    """Ask Gemma 4 using local .mic memory."""
    console.print(ask_with_memory(memory, question, backend, model))


@app.command()
def test(
    task: str,
    memory: str = typer.Option(..., "--memory", "-m"),
    backend: str = typer.Option("ollama", "--backend"),
    model: str = typer.Option("gemma4", "--model"),
):
    """Generate tests using Gemma 4 and .mic memory."""
    console.print(test_with_memory(memory, task, backend, model))


@app.command()
def plan(
    task: str,
    memory: str = typer.Option(..., "--memory", "-m"),
    backend: str = typer.Option("ollama", "--backend"),
    model: str = typer.Option("gemma4", "--model"),
):
    """Generate a safe patch plan."""
    console.print(plan_with_memory(memory, task, backend, model))


@app.command()
def demo():
    """Run the MICode Tutor demo."""
    repo = Path("examples/edu_auth_service")
    out = Path("edu_auth_service.mic")

    console.print(Panel.fit("MICode Tutor Demo", style="bold cyan"))
    console.print("[bold]Compiling demo repo into .mic memory...[/bold]\n")

    mem = compile_repo(str(repo))
    mem.save(str(out))
    console.print(f"[green]✓ Created {out}[/green]\n")

    inspect_memory(str(out))

    q = "where is JWT authentication verified?"
    console.print(f"\n[bold]Search:[/bold] {q}")
    for i, r in enumerate(search_memory(str(out), q, 5), 1):
        console.print(f"{i}. {r}")

    task = "write tests for expired refresh tokens"
    console.print(f"\n[bold]Context Pack:[/bold] {task}")
    pack_text = build_context_pack(str(out), task, 2500)
    console.print(pack_text[:4500])

    console.print("\n[bold green]Demo complete.[/bold green]")
    console.print("Try:")
    console.print("  mic ask \"explain the auth flow\" --memory edu_auth_service.mic --model gemma4")
    console.print("  mic test \"write tests for expired refresh tokens\" --memory edu_auth_service.mic --model gemma4")


if __name__ == "__main__":
    app()

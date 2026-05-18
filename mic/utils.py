import hashlib
import re
from pathlib import Path


IGNORE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".idea", ".vscode"
}

TEXT_EXTS = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".sh", ".ts", ".tsx", ".js"
}


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
        "return", "import", "as", "if", "else", "elif", "true", "false",
        "none", "self", "cls"
    }
    out = []
    seen = set()
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
    if "readme" in p:
        return "Project documentation."
    return "Repository source file."

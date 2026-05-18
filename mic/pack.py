from pathlib import Path
from mic.schema import MicMemory
from mic.retrieval import search_memory


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
            snippet = snippet[: max(0, max_chars - used)]
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
    lines.append("- If the context is insufficient, say what is missing.")
    lines.append("- Prefer clear explanations for students and practical next steps for developers.")
    lines.append("- Do not claim you inspected files that are not in this context.")

    return "\n".join(lines)


def save_context_pack(memory_path: str, task: str, out: str, budget: int = 4000):
    text = build_context_pack(memory_path, task, budget=budget)
    Path(out).write_text(text, encoding="utf-8")
    return out

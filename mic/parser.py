import ast
from pathlib import Path
from mic.schema import MicFile, MicSymbol
from mic.utils import stable_id, read_text_safe, line_slice, rough_summary_from_path


def _rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def _annotation_to_str(node) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef, qualified_name: str) -> str:
    args = []
    for a in node.args.args:
        ann = _annotation_to_str(a.annotation)
        if ann:
            args.append(f"{a.arg}: {ann}")
        else:
            args.append(a.arg)

    ret = _annotation_to_str(node.returns)
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    sig = f"{prefix} {qualified_name}({', '.join(args)})"
    if ret:
        sig += f" -> {ret}"
    return sig


def parse_python_file(root: Path, path: Path):
    rel = _rel(root, path)
    text = read_text_safe(path)

    try:
        tree = ast.parse(text)
    except SyntaxError:
        file_card = MicFile(
            id=stable_id("file", rel),
            path=rel,
            language="python",
            role=rough_summary_from_path(rel),
            is_test=("test" in rel.lower()),
            summary=rough_summary_from_path(rel),
        )
        return file_card, [], []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

    symbols = []
    exports = []

    # top-level functions/classes + class methods
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            start = getattr(node, "lineno", 1)
            end = getattr(node, "end_lineno", start)
            evidence = line_slice(text, start, end)
            doc = ast.get_docstring(node) or ""
            summary = doc.strip().split("\n")[0] if doc else f"Function `{name}` defined in `{rel}`."
            signature = _function_signature(node, name)

            symbols.append(MicSymbol(
                id=stable_id("sym", rel, name),
                kind="function",
                name=name,
                path=rel,
                start_line=start,
                end_line=end,
                signature=signature,
                summary=summary,
                evidence=evidence[:6000],
            ))
            exports.append(name)

        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            c_start = getattr(node, "lineno", 1)
            c_end = getattr(node, "end_lineno", c_start)
            c_evidence = line_slice(text, c_start, min(c_end, c_start + 80))
            c_doc = ast.get_docstring(node) or ""
            c_summary = c_doc.strip().split("\n")[0] if c_doc else f"Class `{class_name}` defined in `{rel}`."

            symbols.append(MicSymbol(
                id=stable_id("sym", rel, class_name),
                kind="class",
                name=class_name,
                path=rel,
                start_line=c_start,
                end_line=c_end,
                signature=f"class {class_name}",
                summary=c_summary,
                evidence=c_evidence[:6000],
            ))
            exports.append(class_name)

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method_name = f"{class_name}.{item.name}"
                    start = getattr(item, "lineno", 1)
                    end = getattr(item, "end_lineno", start)
                    evidence = line_slice(text, start, end)
                    doc = ast.get_docstring(item) or ""
                    summary = doc.strip().split("\n")[0] if doc else f"Method `{method_name}` defined in `{rel}`."
                    signature = _function_signature(item, method_name)

                    symbols.append(MicSymbol(
                        id=stable_id("sym", rel, method_name),
                        kind="method",
                        name=method_name,
                        path=rel,
                        start_line=start,
                        end_line=end,
                        signature=signature,
                        summary=summary,
                        evidence=evidence[:6000],
                    ))
                    exports.append(method_name)

    file_summary = rough_summary_from_path(rel)
    if exports:
        file_summary += f" Defines: {', '.join(exports[:12])}."

    file_card = MicFile(
        id=stable_id("file", rel),
        path=rel,
        language="python",
        role=rough_summary_from_path(rel),
        imports=sorted(set([x for x in imports if x])),
        exports=exports,
        is_test=("test" in rel.lower()),
        summary=file_summary,
    )

    return file_card, symbols, []


def parse_text_file(root: Path, path: Path):
    rel = _rel(root, path)
    text = read_text_safe(path)

    title = ""
    for line in text.splitlines()[:30]:
        if line.strip().startswith("#"):
            title = line.strip("# ").strip()
            break

    file_card = MicFile(
        id=stable_id("file", rel),
        path=rel,
        language=path.suffix.lstrip(".") or "text",
        role=rough_summary_from_path(rel),
        exports=[],
        imports=[],
        is_test=("test" in rel.lower()),
        summary=title or rough_summary_from_path(rel),
    )
    return file_card, [], []


def parse_file(root: Path, path: Path):
    if path.suffix == ".py":
        return parse_python_file(root, path)
    return parse_text_file(root, path)

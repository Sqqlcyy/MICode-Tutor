from pathlib import Path
from datetime import datetime
from mic.schema import MicMemory, MicStateToken, MicRelation
from mic.parser import parse_file
from mic.utils import iter_repo_files, stable_id, simple_tokens


def _build_state_tokens_for_file(file_card):
    base = f"{file_card.path} {file_card.role} {file_card.summary} {' '.join(file_card.exports)} {' '.join(file_card.imports)}"
    return MicStateToken(
        state_id=stable_id("state", file_card.id),
        target_id=file_card.id,
        state_type="hybrid_file_state",
        tokens=simple_tokens(base, max_tokens=40),
    )


def _build_state_tokens_for_symbol(sym):
    base = f"{sym.path} {sym.name} {sym.kind} {sym.signature} {sym.summary} {sym.evidence[:1200]}"
    return MicStateToken(
        state_id=stable_id("state", sym.id),
        target_id=sym.id,
        state_type="hybrid_symbol_state",
        tokens=simple_tokens(base, max_tokens=64),
    )


def _infer_test_links(symbols):
    test_symbols = [s for s in symbols if "test" in s.path.lower() or s.name.startswith("test_")]
    normal_symbols = [s for s in symbols if s not in test_symbols]

    for sym in normal_symbols:
        linked = []
        for t in test_symbols:
            hay = f"{t.name} {t.summary} {t.evidence}".lower()
            if sym.name.lower() in hay:
                linked.append(f"{t.path}::{t.name}")
        sym.tests = linked[:5]


def _infer_relations(symbols):
    relations = []
    by_name = {s.name: s for s in symbols}

    for sym in symbols:
        evidence = sym.evidence or ""
        for name, target in by_name.items():
            if name == sym.name:
                continue
            if f"{name}(" in evidence:
                sym.calls.append(name)
                target.called_by.append(f"{sym.path}::{sym.name}")
                relations.append(MicRelation(
                    source=f"{sym.path}::{sym.name}",
                    target=f"{target.path}::{target.name}",
                    type="calls",
                    confidence=0.65,
                ))

    return relations


def compile_repo(repo_path: str) -> MicMemory:
    root = Path(repo_path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repo path not found: {repo_path}")

    files = []
    symbols = []
    relations = []

    for p in iter_repo_files(str(root)):
        file_card, syms, rels = parse_file(root, p)
        files.append(file_card)
        symbols.extend(syms)
        relations.extend(rels)

    _infer_test_links(symbols)
    relations.extend(_infer_relations(symbols))

    state_tokens = []
    for f in files:
        state_tokens.append(_build_state_tokens_for_file(f))
    for s in symbols:
        state_tokens.append(_build_state_tokens_for_symbol(s))

    languages = sorted(set([f.language for f in files if f.language]))

    memory = MicMemory(
        repo={
            "name": root.name,
            "root": str(root),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "languages": languages,
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
    return memory

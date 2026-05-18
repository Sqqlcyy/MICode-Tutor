from dataclasses import dataclass
from mic.schema import MicMemory
from mic.utils import simple_tokens


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


def _overlap_score(q_tokens: set[str], text: str) -> float:
    toks = set(simple_tokens(text, max_tokens=160))
    if not q_tokens or not toks:
        return 0.0
    return len(q_tokens & toks) / max(1, len(q_tokens))


def _state_score(q_tokens: set[str], tokens: list[str]) -> float:
    return _overlap_score(q_tokens, " ".join(tokens))


def search_memory(memory_path: str, query: str, top_k: int = 5) -> list[SearchResult]:
    mem = MicMemory.load(memory_path)
    q = query.lower()
    q_tokens = set(simple_tokens(query, max_tokens=80))
    state_by_target = {s.target_id: s.tokens for s in mem.state_tokens}

    results: list[SearchResult] = []

    for s in mem.symbols:
        blob = f"{s.name} {s.kind} {s.path} {s.signature} {s.summary} {s.evidence[:1200]}"
        score = 0.0
        score += 2.0 * _overlap_score(q_tokens, blob)
        score += 1.2 * _state_score(q_tokens, state_by_target.get(s.id, []))

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
        blob = f"{f.path} {f.role} {f.summary} {' '.join(f.exports)} {' '.join(f.imports)}"
        score = 0.0
        score += 1.2 * _overlap_score(q_tokens, blob)
        score += 0.8 * _state_score(q_tokens, state_by_target.get(f.id, []))

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

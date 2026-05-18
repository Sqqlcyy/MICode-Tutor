import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field


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
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)

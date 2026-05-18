# Relationship Between MICode and MII

MICode Tutor is an applied codebase-memory system inspired by our broader Machine-Interpretable Information (MII) research direction.

MII asks a general question:

> What is the native file format for neural agents?

Instead of repeatedly passing raw text to models, MII explores compiling documents into persistent machine-interpretable protocol states.

MICode applies this principle to software repositories.

## MII

MII is a general document-to-state research direction. Its long-term goal is to compile documents into compact machine-readable states that can support retrieval, reasoning, and reconstruction.

## MICode

MICode is the codebase-specific engineering artifact used in this project. It compiles repositories into `.mic` memory files containing:

- files,
- symbols,
- line ranges,
- imports and exports,
- tests,
- relations,
- evidence snippets,
- and agent recipes.

MICode v0.1 is intentionally inspectable and symbolic-textual. It does not depend on hidden `.mii` neural states.

## Why This Matters

For code understanding, trust is essential. Developers and students need to know what evidence the model used. MICode therefore exposes the memory and context pack before local Gemma 4 answers.

This makes MICode a practical residual-memory implementation:

```text
compiled codebase memory + sparse evidence snippets + local model reasoning
```

## Future Direction

Future versions may explore deeper neural state representations and richer MII-style memory compilers. The current `.mic` format is the first practical step: transparent, portable, local, and easy to audit.

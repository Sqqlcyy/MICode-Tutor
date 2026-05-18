# MICode Tutor

**Offline Codebase Memory for Gemma 4**

MICode Tutor compiles a repository into a portable `.mic` Machine-Interpretable Code memory file, then lets local Gemma 4 read that memory for repo Q&A, learning, test generation, and safe patch planning.

> AI coding tutors should work without the cloud.

---

## Why MICode Tutor?

Modern AI coding assistants are powerful, but they often assume:

- reliable cloud access,
- paid API keys,
- and permission to upload private code.

That leaves many students, independent builders, open-source maintainers, and privacy-sensitive teams behind.

MICode Tutor takes a local-first approach:

```text
repo
→ .mic memory artifact
→ symbol-aware retrieval
→ auditable context pack
→ local Gemma 4 via Ollama or llama.cpp
```

Gemma does **not** blindly inspect the entire repository. MICSDK prepares a compact evidence pack first. Gemma reasons over that evidence.

---

## What MICode Tutor Does

MICode Tutor is not a prompt wrapper that dumps source code into an LLM.

When you run:

```bash
mic compile examples/edu_auth_service --out edu_auth_service.mic
```

MICSDK builds a `.mic` memory file containing:

- file cards,
- symbol cards,
- classes, functions, and methods,
- imports and exports,
- line ranges,
- test references,
- call relations,
- evidence snippets,
- lightweight state tokens,
- repo capabilities,
- and agent recipes for Q&A, testing, and patch planning.

You can inspect it locally:

```bash
mic inspect edu_auth_service.mic
```

You can search it without calling any model:

```bash
mic search "where is JWT authentication verified?" --memory edu_auth_service.mic
```

You can see exactly what Gemma will receive:

```bash
mic pack "where is JWT verified?" \
  --memory edu_auth_service.mic \
  --budget 500 \
  --top-k 3 \
  --out context_jwt.md
```

Then you can ask local Gemma:

```bash
mic ask "where is JWT verified?" \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest
```

---

## Demo Scenario

The included demo repository is an educational Python authentication service:

```text
examples/edu_auth_service/
  app/
    main.py
    config.py
    auth/
      token.py
      password.py
      routes.py
    middleware/
      auth_required.py
    security/
      rate_limit.py
    db/
      users.py
  tests/
    test_auth.py
    test_config.py
```

The demo supports questions such as:

```bash
mic ask "where is JWT verified?" --memory edu_auth_service.mic --backend ollama --model gemma4:latest

mic ask "explain this repo to a beginner. Give a 5-step learning path." \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest

mic test "write a pytest for expired refresh tokens." \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest

mic plan "add Redis-based rate limiting to login. What files change and what tests are needed?" \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest
```

---

## Quickstart

### 1. Install

```bash
git clone https://github.com/<your-org>/micode-tutor.git
cd micode-tutor
pip install -e .
```

### 2. Run the built-in demo

```bash
mic demo
```

### 3. Compile the demo repo

```bash
mic compile examples/edu_auth_service --out edu_auth_service.mic
```

### 4. Inspect the `.mic` memory

```bash
mic inspect edu_auth_service.mic
```

Expected output includes repository metadata such as:

```text
Files: 17
Symbols: 355
Relations: 46
State tokens: 372
```

### 5. Search locally without an LLM

```bash
mic search "where is JWT authentication verified?" --memory edu_auth_service.mic
```

### 6. Ask local Gemma 4

```bash
mic ask "where is JWT verified?" \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest
```

---

## Local Model Backends

MICode Tutor supports multiple local Gemma runtimes.

### Ollama

Ollama is the easiest way to run Gemma locally.

```bash
mic ask "where is JWT verified?" \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest
```

If you already have a local GGUF model, MICode Tutor can create an Ollama model from it:

```bash
mic backend ollama-start

mic backend ollama-create \
  --gguf /path/to/gemma4-e4b-q4_k_m.gguf \
  --name gemma4:latest

mic backend ollama-test --model gemma4:latest
```

This supports offline or USB-delivered model artifacts.

### llama.cpp

llama.cpp is a lower-level GGUF inference runtime suitable for resource-constrained environments.

```bash
mic backend llamacpp-build

mic backend llamacpp-start \
  --gguf /path/to/gemma4-e4b-q4_k_m.gguf
```

Then:

```bash
mic ask "where is JWT verified?" \
  --memory edu_auth_service.mic \
  --backend llamacpp \
  --model gemma4
```

### Backend Doctor

Check local runtime status:

```bash
mic backend doctor
```

This reports GPU availability, Ollama status, llama.cpp build status, and local GGUF model files.

---

## Why Both Ollama and llama.cpp?

They serve different deployment needs.

| Backend | Best for | Why |
|---|---|---|
| Ollama | teachers, students, developers | easiest local deployment and model management |
| llama.cpp | low-resource machines, CPU/GPU edge deployment | direct GGUF runtime with low-level control |
| GGUF | offline model distribution | can be delivered by USB/local disk/classroom server |

MICode Tutor uses the same `.mic` memory and context pack with either backend.

---

## Safety and Trust

MICode Tutor is designed as a **human-in-the-loop** coding tutor.

It does not automatically mutate your repository.

Safety features:

- local `.mic` memory file,
- no cloud API required,
- no code upload,
- inspectable memory,
- auditable context packs,
- evidence citations with file paths and line ranges,
- patch planning instead of automatic edits,
- test generation for human review.

Example:

```bash
mic pack "where is JWT verified?" \
  --memory edu_auth_service.mic \
  --out context_jwt.md
```

This shows exactly what context Gemma receives.

---

## Commands

```bash
# Compile repo into .mic memory
mic compile examples/edu_auth_service --out edu_auth_service.mic

# Inspect memory
mic inspect edu_auth_service.mic

# Local search without LLM
mic search "where is JWT authentication verified?" --memory edu_auth_service.mic

# Build an auditable context pack
mic pack "write tests for expired refresh tokens" --memory edu_auth_service.mic

# Ask local Gemma 4
mic ask "explain the auth flow" --memory edu_auth_service.mic --backend ollama --model gemma4:latest

# Generate tests
mic test "write tests for expired refresh tokens" --memory edu_auth_service.mic --backend ollama --model gemma4:latest

# Generate a safe patch plan
mic plan "add Redis-based rate limiting to login" --memory edu_auth_service.mic --backend ollama --model gemma4:latest

# Backend setup
mic backend doctor
mic backend ollama-start
mic backend ollama-create --gguf /path/to/model.gguf --name gemma4:latest
mic backend llamacpp-build
mic backend llamacpp-start --gguf /path/to/model.gguf
```

---

## Architecture

```text
┌────────────────────┐
│ Source Repository  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ MIC Compiler       │
│ files, symbols,    │
│ relations, tests   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ .mic Memory File   │
│ portable, local,   │
│ inspectable        │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Symbol-Aware       │
│ Retrieval          │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Context Pack       │
│ evidence + lines   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Local Gemma 4      │
│ Ollama / llama.cpp │
└────────────────────┘
```

---

## Digital Equity Use Case

MICode Tutor is designed for low-connectivity and privacy-sensitive environments.

A realistic deployment is:

```text
one local classroom server
+ quantized Gemma 4 model
+ Ollama or llama.cpp
+ shared .mic course repositories
+ many students using lightweight terminals
```

Students do not need cloud API keys.  
Private code does not leave the machine.  
Teachers can distribute `.mic` memory files with course repositories.

---

## Current Scope

MICode Tutor v0.1 is a research alpha.

It is not a replacement for Cursor, Claude Code, or full autonomous coding agents.

It demonstrates a focused capability:

> Compile a repository into portable machine memory so local Gemma 4 can explain, teach, test, and plan safely offline.

---

## Limitations

- Python-focused parser in v0.1.
- Retrieval is lightweight and symbolic-textual, not learned neural retrieval.
- Patch generation is proposal-only and does not apply edits.
- Local inference speed depends on model size, quantization, runtime, and hardware.
- Offline model setup still requires a local GGUF or preinstalled runtime.

---

## Roadmap

- richer multi-language parsers,
- MCP server integration,
- LangChain / LlamaIndex retriever adapters,
- GitHub Action to generate `.mic` on pull requests,
- offline classroom bundle,
- improved benchmark suite,
- learned neural MIC compiler research,
- GUI / lightweight web UI,
- safer patch application with sandboxed test execution.

---

## Project Philosophy

Codebases should be compiled into machine-interpretable memory before agents reason over them.

MICode Tutor is the first small step toward that idea.

---

## License

MIT License.

---

## Citation

If you use MICode Tutor, please cite:

```text
MICode Tutor: Offline Codebase Memory for Gemma 4.
Built for the Google DeepMind Gemma 4 Good Hackathon, 2026.
```# MICode-Tutor

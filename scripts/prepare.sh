#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

BASE="/root/autodl-tmp/micode-tutor"
E4B_DIR="$BASE/gemma-4-E4B-it-GGUF"
E2B_DIR="$BASE/gemma-4-E2B-it-GGUF"

ZOO="/root/autodl-tmp/models/micode-gemma4-zoo"
GGUF="$ZOO/gguf"
MODS="$ZOO/modelfiles"
CARDS="$ZOO/cards"

mkdir -p "$GGUF" "$MODS" "$CARDS"

echo "== MICode Tutor Gemma 4 Model Zoo Prep =="
echo "Base: $BASE"
echo "Zoo:  $ZOO"
echo

move_first() {
  local target="$1"
  shift

  if [ -f "$GGUF/$target.gguf" ]; then
    echo "✓ already exists: $GGUF/$target.gguf"
    return 0
  fi

  for pattern in "$@"; do
    for f in $pattern; do
      if [ -f "$f" ]; then
        echo "→ keeping $target"
        echo "  from: $f"
        mv -n "$f" "$GGUF/$target.gguf"
        echo "  to:   $GGUF/$target.gguf"
        return 0
      fi
    done
  done

  echo "⚠ missing: $target"
  return 1
}

# 1. Main demo model: balanced quality/speed
move_first "gemma4-e4b-q4_k_m" \
  "$E4B_DIR/gemma-4-E4B-it-Q4_K_M.gguf" \
  "$E4B_DIR/"*Q4_K_M*.gguf || true

# 2. Higher quality model for test/plan/code generation
move_first "gemma4-e4b-q6_k" \
  "$E4B_DIR/gemma-4-E4B-it-Q6_K.gguf" \
  "$E4B_DIR/"*Q6_K*.gguf \
  "$E4B_DIR/"*Q8_0*.gguf || true

# 3. Smaller classroom / edge model
move_first "gemma4-e2b-q4_k_m" \
  "$E2B_DIR/gemma-4-E2B-it-Q4_K_M.gguf" \
  "$E2B_DIR/"*Q4_K_M*.gguf \
  "$E2B_DIR/"*Q4_0*.gguf \
  "$E4B_DIR/"*Q3_K_M*.gguf || true

# 4. Ultra-low footprint model
move_first "gemma4-e2b-iq4_xs" \
  "$E2B_DIR/gemma-4-E2B-it-IQ4_XS.gguf" \
  "$E2B_DIR/"*IQ4_XS*.gguf \
  "$E2B_DIR/"*Q3_K_S*.gguf \
  "$E4B_DIR/"*UD-IQ2_M*.gguf \
  "$E4B_DIR/"*IQ4_XS*.gguf || true

# Optional multimodal projector, not used in main demo
if [ -f "$E4B_DIR/mmproj-F16.gguf" ]; then
  mv -n "$E4B_DIR/mmproj-F16.gguf" "$GGUF/mmproj-F16.gguf"
  echo "✓ kept optional mmproj-F16.gguf"
elif [ -f "$GGUF/mmproj-F16.gguf" ]; then
  echo "✓ optional mmproj-F16.gguf already exists"
else
  echo "· no mmproj-F16 found, skipping"
fi

echo
echo "== Deleting unused cloned model directories =="
rm -rf "$E4B_DIR" "$E2B_DIR"
sync

write_modelfile() {
  local name="$1"
  local file="$2"
  local ctx="$3"
  local predict="$4"
  local batch="$5"

  cat > "$MODS/Modelfile.$name" <<EOF2
FROM $file

PARAMETER temperature 0.2
PARAMETER num_ctx $ctx
PARAMETER num_predict $predict
PARAMETER num_batch $batch

SYSTEM """
You are Gemma 4 running as a local offline coding tutor.

You do not have internet access.
You answer using only the MICode Context Pack provided by the local MICSDK.
Always cite file paths, symbol names, and line ranges when available.
If context is insufficient, say what is missing.
Do not claim you inspected files that are not in the context.
"""
EOF2
}

echo
echo "== Writing Ollama Modelfiles =="

[ -f "$GGUF/gemma4-e4b-q4_k_m.gguf" ] && \
  write_modelfile "e4b-q4" "$GGUF/gemma4-e4b-q4_k_m.gguf" 2048 512 64

[ -f "$GGUF/gemma4-e4b-q6_k.gguf" ] && \
  write_modelfile "e4b-q6" "$GGUF/gemma4-e4b-q6_k.gguf" 4096 768 64

[ -f "$GGUF/gemma4-e2b-q4_k_m.gguf" ] && \
  write_modelfile "e2b-q4" "$GGUF/gemma4-e2b-q4_k_m.gguf" 2048 512 64

[ -f "$GGUF/gemma4-e2b-iq4_xs.gguf" ] && \
  write_modelfile "e2b-iq4-xs" "$GGUF/gemma4-e2b-iq4_xs.gguf" 2048 384 64

echo
echo "== Writing model card =="

cat > "$ZOO/MODEL_CARD.md" <<'EOF2'
# MICode Tutor Gemma 4 Local Model Zoo

This directory contains a minimal local model zoo for MICode Tutor.

MICode Tutor uses `.mic` repository memory to reduce context length and make local Gemma inference practical for offline coding education.

## Kept Models

| Model | Purpose | Backend |
|---|---|---|
| `gemma4-e4b-q4_k_m.gguf` | Main hackathon demo: balanced speed and quality | Ollama / llama.cpp |
| `gemma4-e4b-q6_k.gguf` | Higher-quality test generation and patch planning | Ollama / llama.cpp |
| `gemma4-e2b-q4_k_m.gguf` | Lower-resource classroom server / digital equity demo | Ollama / llama.cpp |
| `gemma4-e2b-iq4_xs.gguf` | Ultra-low footprint edge demo | llama.cpp preferred |
| `mmproj-F16.gguf` | Optional multimodal projector, not required for MICode Tutor text demo | future |

## Why multiple quantizations?

MICode Tutor targets different offline environments:

1. **Main local demo:** E4B Q4_K_M gives fast, high-quality responses.
2. **Safe second-development:** E4B Q6_K improves planning and test generation.
3. **Digital equity:** E2B Q4_K_M supports low-resource classroom servers.
4. **Extreme edge:** IQ4/low-bit variants demonstrate deployment on constrained hardware.

## Ollama Usage

Create the main demo model:

```bash
ollama create mic-gemma4:e4b-q4 -f modelfiles/Modelfile.e4b-q4

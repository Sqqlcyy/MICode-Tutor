#!/usr/bin/env bash
set -e

clear
echo "============================================================"
echo "MICode Tutor: Offline Codebase Memory for Gemma 4"
echo "repo -> .mic memory -> local search -> context pack -> Gemma"
echo "No cloud API. No code upload. Inspectable evidence."
echo "============================================================"
sleep 2

echo
echo "STEP 1 — Compile a repository into .mic code memory"
echo "$ mic compile examples/edu_auth_service --out edu_auth_service.mic"
mic compile examples/edu_auth_service --out edu_auth_service.mic
sleep 2

echo
echo "STEP 2 — Inspect the memory artifact"
echo "$ mic inspect edu_auth_service.mic"
mic inspect edu_auth_service.mic
sleep 3

echo
echo "STEP 3 — Search locally without calling any LLM"
echo "$ mic search \"Where is JWT verified?\" --memory edu_auth_service.mic"
mic search "Where is JWT verified?" --memory edu_auth_service.mic
sleep 3

echo
echo "STEP 4 — Build an auditable context pack"
echo "$ mic pack \"Where is JWT verified?\" --memory edu_auth_service.mic --budget 500 --top-k 5 --out context_jwt.md"
mic pack "Where is JWT verified?" \
  --memory edu_auth_service.mic \
  --budget 500 \
  --top-k 5 \
  --out context_jwt.md
sleep 2

echo
echo "STEP 5 — Show exactly what Gemma will receive"
echo "$ head -80 context_jwt.md"
head -80 context_jwt.md
sleep 4

echo
echo "STEP 6 — Ask local Gemma 4 through Ollama"
echo "$ mic ask \"Where is JWT verified?\" --memory edu_auth_service.mic --backend ollama --model gemma4:latest"
mic ask "Where is JWT verified?" \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest

echo
echo "STEP 7 — Safe patch planning, not automatic mutation"
echo "$ mic plan \"Add Redis-based rate limiting to login.\" --memory edu_auth_service.mic --backend ollama --model gemma4:latest"
mic plan "Add Redis-based rate limiting to login." \
  --memory edu_auth_service.mic \
  --backend ollama \
  --model gemma4:latest

echo
echo "============================================================"
echo "MICode retrieves. Gemma reasons and teaches."
echo "AI coding tutors should work without the cloud."
echo "============================================================"


SYSTEM_PROMPT = """You are Gemma 4 running as an offline coding tutor.

You do not have internet access.
You must answer using only the MICode Context Pack provided by the local MICSDK.
Always cite file paths, symbol names, and line ranges when available.
If the context is insufficient, say what is missing.
Prefer clear explanations for students and practical next steps for developers.
Do not claim you inspected files that are not in the context.
"""


def ask_prompt(context_pack: str, question: str) -> str:
    return f"""{SYSTEM_PROMPT}

{context_pack}

Question:
{question}

Answer with:
1. Short answer
2. Explanation
3. Evidence
4. Next steps if relevant
"""


def plan_prompt(context_pack: str, task: str) -> str:
    return f"""{SYSTEM_PROMPT}

{context_pack}

Task:
{task}

Produce a safe patch plan. Do not write code yet.

Output:
1. Files likely to change
2. Symbols involved
3. Step-by-step plan
4. Risks
5. Tests to add
"""


def test_prompt(context_pack: str, task: str) -> str:
    return f"""{SYSTEM_PROMPT}

{context_pack}

Task:
{task}

Generate a pytest example grounded strictly in the context.

Hard rules:
- Use only functions, classes, imports, and files visible in the MICode Context Pack.
- Do not invent modules such as `your_module`.
- Do not invent methods that are not shown.
- Prefer the existing style in `tests/test_auth.py`.
- If testing token expiration, prefer constructing a payload with `exp` in the past and asserting that `refresh_token(...)` or `verify_jwt(...)` raises.
- Keep the code minimal and directly runnable within this demo repo if possible.

Output:
1. Target test file
2. Test code
3. Evidence used
"""

def patch_prompt(context_pack: str, task: str) -> str:
    return f"""{SYSTEM_PROMPT}

{context_pack}

Task:
{task}

Generate a minimal unified diff.

Rules:
- Only modify files present in the context.
- Keep patch small.
- Include explanation after the diff.
- If context is insufficient, do not invent missing APIs.
"""

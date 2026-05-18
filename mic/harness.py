from mic.pack import build_context_pack
from mic.gemma import generate_with_backend
from mic.prompts import ask_prompt, plan_prompt, test_prompt, patch_prompt


def ask_with_memory(memory_path: str, question: str, backend: str = "ollama", model: str = "gemma4:latest") -> str:
    pack = build_context_pack(memory_path, question, budget=4096, top_k=3)
    prompt = ask_prompt(pack, question)
    return generate_with_backend(prompt, backend=backend, model=model)


def plan_with_memory(memory_path: str, task: str, backend: str = "ollama", model: str = "gemma4:latest") -> str:
    pack = build_context_pack(memory_path, task, budget=4096, top_k=4)
    prompt = plan_prompt(pack, task)
    return generate_with_backend(prompt, backend=backend, model=model)


def generate_tests(memory_path: str, task: str, backend: str = "ollama", model: str = "gemma4:latest") -> str:
    pack = build_context_pack(memory_path, task, budget=4096, top_k=4)
    prompt = test_prompt(pack, task)
    return generate_with_backend(prompt, backend=backend, model=model)


def generate_patch(memory_path: str, task: str, backend: str = "ollama", model: str = "gemma4:latest") -> str:
    pack = build_context_pack(memory_path, task, budget=4096, top_k=4)
    prompt = patch_prompt(pack, task)
    return generate_with_backend(prompt, backend=backend, model=model)

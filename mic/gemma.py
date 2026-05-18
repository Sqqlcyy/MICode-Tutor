import os
import json
import requests


def _ollama_options(mode: str = "ask") -> dict:
    if mode == "test":
        return {
            "temperature": 0.2,
            "num_ctx": 4096,
            "num_predict": 5120,
            "num_batch": 128,
        }
    if mode == "plan":
        return {
            "temperature": 0.2,
            "num_ctx": 4096,
            "num_predict": 5120,
            "num_batch": 128,
        }
    return {
        "temperature": 0.2,
        "num_ctx": 2048,
        "num_predict": 2560,
        "num_batch": 128,
    }


def generate_ollama(prompt: str, model: str = "gemma4:latest", timeout: int = 900, mode: str = "ask") -> str:
    """
    Stable Ollama backend for Gemma 4.

    Default: non-streaming, returns complete answer.
    Set MIC_STREAM=1 for video streaming. In streaming mode, tokens are printed
    live and the returned string is empty to avoid duplicate console output.
    """
    use_stream = os.getenv("MIC_STREAM", "0") == "1"
    url = "http://localhost:11434/api/chat"

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": use_stream,
        "think": False,
        "options": _ollama_options(mode),
    }

    if use_stream:
        chunks = []
        last = {}

        with requests.post(url, json=payload, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                data = json.loads(line.decode("utf-8"))
                last = data
                token = data.get("message", {}).get("content", "")
                if token:
                    print(token, end="", flush=True)
                    chunks.append(token)
                if data.get("done"):
                    break

        print()
        done_reason = last.get("done_reason", "")
        if done_reason == "length":
            print("\n[Note: output stopped because num_predict limit was reached.]")
        return ""

    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()

    content = data.get("message", {}).get("content", "").strip()
    thinking = data.get("message", {}).get("thinking", "")
    done_reason = data.get("done_reason", "")

    if content:
        if done_reason == "length":
            content += "\n\n[Note: output stopped because num_predict limit was reached.]"
        return content

    if thinking:
        return (
            "[Ollama produced thinking but no final answer. "
            "Try think=false, larger num_predict, or shorter context.]"
        )

    return "[Ollama returned an empty response.]"


def generate_llamacpp(prompt: str, timeout: int = 900) -> str:
    """
    llama.cpp backend through llama-server OpenAI-compatible chat endpoint.
    Assumes llama-server is running on http://localhost:8080.
    """
    url = "http://localhost:8080/v1/chat/completions"
    payload = {
        "model": "gemma4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 512,
    }
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

def generate_openai_compatible(prompt: str, model: str = "gemma4", timeout: int = 900) -> str:
    url = "http://localhost:8080/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 512,
    }
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()


def generate_with_backend(prompt: str, backend: str = "ollama", model: str = "gemma4:latest", mode: str = "ask") -> str:
    try:
        if backend == "ollama":
            return generate_ollama(prompt, model=model, mode=mode)

        if backend == "llamacpp":
            return generate_llamacpp(prompt)

        if backend in {"openai-compatible", "openai"}:
            return generate_openai_compatible(prompt, model=model)

        return f"[Unsupported backend: {backend}]\n\n{prompt}"

    except Exception as e:
        return (
            "[MICode Tutor fallback]\n"
            f"Could not reach backend `{backend}`.\n"
            f"Error: {e}\n\n"
            "----- PROMPT START -----\n"
            f"{prompt}\n"
            "----- PROMPT END -----\n"
        )

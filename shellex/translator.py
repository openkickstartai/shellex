"""Translate natural language to shell commands using Ollama."""
import json
import requests
from typing import Optional, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """You are a shell command translator. Given a natural language description,
return the exact shell command that accomplishes the task.

Rules:
- Output ONLY valid shell commands for the specified shell
- Prefer standard Unix tools (find, grep, awk, sed, sort, etc.)
- Use pipes when combining multiple operations
- Never use sudo unless explicitly requested

Respond in JSON: {"command": "...", "explanation": "..."}
"""


def translate(query: str, model: str = "llama3.2", shell: str = "bash") -> Optional[Dict]:
    """Translate a natural language query to a shell command."""
    prompt = f"Shell: {shell}\nTask: {query}\n\nRespond with JSON only."
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": model,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }, timeout=30)
        resp.raise_for_status()
        text = resp.json().get("response", "")
        result = json.loads(text)
        if "command" not in result:
            return None
        return result
    except (requests.RequestException, json.JSONDecodeError, KeyError):
        return None

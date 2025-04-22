# ollama.py

import subprocess
import json

import os

# Manually add Ollama binary path if missing
if "//usr/local/bin/ollama" not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + "/usr/local/bin/ollama"


def estimate_tokens(text):
    return int(len(text) / 4)  # Rough rule: 1 token ≈ 4 chars


def build_german_prompt(text):
    return f"""
You are a German language learning assistant. The user gives you German text. You will:
1. Estimate the CEFR level of the text (e.g., B2, C1),
2. Rewrite the text in a simplified B1-B2 German version (~400 words),
3. List 30 vocabulary words with short explanations,
4. Identify 5 grammar structures.

German text:
{text}

Return all outputs in a clean, organized format.
"""


def ollama_request(text, model="llama3.2", num_tokens=1200):
    full_prompt = build_german_prompt(text)
    payload = {"prompt": full_prompt, "options": {"num_predict": num_tokens}}

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=json.dumps(payload).encode("utf-8"),
            capture_output=True,
            timeout=120,
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        return f"❌ Ollama error: {e}"


def stop_model(model="llama3.2"):
    try:
        subprocess.run(["ollama", "stop", model])
    except Exception as e:
        print(f"⚠️ Could not stop model {model}: {e}")

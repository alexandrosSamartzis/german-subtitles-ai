# ollama.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import subprocess
import json
from app.prompts import GERMAN_ANALYSIS_PROMPT as GAP


def estimate_tokens(text):
    return int(len(text) / 4)  # Rough rule: 1 token ≈ 4 chars


def ollama_request(model, text, num_tokens=800):
    full_prompt = f"{GAP}{text}"
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

# main.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.ollama import ollama_request
import os

# (Optional) if Ollama isn't found, manually add it to PATH
os.environ["PATH"] += os.pathsep + "/usr/local/bin"  # Replace if needed

text = "Der Papst ist am Ostersonntag gestorben. Tausende Menschen beteten auf dem Petersplatz."

models_to_test = ["mistral"] 

for model in models_to_test:
    print(f"\n🔍 Testing model: {model}")
    try:
        response = ollama_request(text, model=model, num_tokens=1200)
        print("✅ SUCCESS:\n", response[:], "...\n")
    except Exception as e:
        print("❌ FAILED:", e)

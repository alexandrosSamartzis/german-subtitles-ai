import subprocess
import json
import os


def ollama_request(prompt, model="llama3.2", num_tokens=800):
    # Prepare JSON input for the CLI
    full_prompt = {"prompt": prompt, "options": {"num_predict": num_tokens}}

    # Call Ollama using JSON input
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=json.dumps(full_prompt).encode("utf-8"),
            capture_output=True,
            timeout=120,  # Optional: limit runaway calls
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        print("⚠️ Ollama call failed:", e)
        return "Error: Could not get response from local model."


# Load subtitle text file
file_path = "/text.txt"

if not os.path.exists(file_path):
    print("❌ Error: subtitle_text.txt file not found.")
    exit()

with open(file_path, "r", encoding="utf-8") as file:
    german_text = file.read().strip()

if not german_text:
    print("❌ Error: subtitle_text.txt is empty.")
    exit()


def estimate_tokens(text):
    return int(len(text) / 4)  # Rough: 1 token ≈ 4 characters


# Example
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    tokens = estimate_tokens(content)
    print(f"Estimated tokens: {tokens}")

# Prompt to simplify the sentence
prompt = f"""
You are a German language learning assistant. The user gives you German text. You will: 1. Estimate the CEFR level of the text (e.g., B2, C1), 2. Rewrite the text in a simplified B1-B2 German version with around 400 words, 

German sentence:
{german_text}

Return only the simplified sentence.
"""
# Choose a model: Change this manually or via future UI
selected_model = ["yi:6b", "deepseek-coder:6.7b", "llama3:8b", "mistral"]

# Run the request
result = ollama_request(prompt, model=selected_model[1], num_tokens=800)
print("Simplified output:\n", result)


def stop_ollama_models():
    subprocess.run(["ollama", "stop", "llama3.2"])


# Add this at the end of your script
stop_ollama_models()

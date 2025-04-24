# api.py
import os
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
# from prompts import GERMAN_ANALYSIS_PROMPT
from .ollama import ollama_request as ol_req
from .prompts import GERMAN_ANALYSIS_PROMPT as GAP


def analyze_german_text_with_chatgpt(text: str) -> str:
    """
    Sends text to ChatGPT (GPT-4o) using OpenAI API.
    Returns AI analysis or error message.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "❌ API key missing. Please check your environment variables."

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": GAP + text,
            },
        ],
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP error: {http_err}"
    except Exception as e:
        return f"❌ Error calling OpenAI API: {e}"


def analyze_with_deepseek(text: str) -> str:
    """
    Sends text to DeepSeek using DeepSeek API.
    Returns AI analysis or error message.
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "❌ API key missing. Please check your environment variables."

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {"role": "user", "content": GAP + text},
        ],
        "temperature": 0.7,
    }
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP error: {http_err}"
    except Exception as e:
        return f"❌ Error calling DeepSeek API: {e}"


def analyze_with_local_model(model_name: str, text: str, token_limit: int = 800) -> str:
    """
    Uses Ollama to analyze German text with selected local model.
    """
    return ol_req(model=model_name, text=text, num_tokens=token_limit)


__all__ = [
    "analyze_german_text_with_chatgpt",
    "analyze_with_local_model",
    "analyze_with_deepseek",
]

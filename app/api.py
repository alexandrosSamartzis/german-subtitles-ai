#
# 
# ✅ Ideally this will be moved to environment or .env file later
# i# 🔒 Keep this safe when pushing to GitHubv
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OpenAI API key is not set in environment variables.")
import requests
import json
# Check key is valid
if not api_key or not api_key.startswith("sk-"):
    raise ValueError("❌ OpenAI API key is missing or malformed.")

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def analyze_german_text_with_chatgpt(text: str) -> str:
    system_message = (
        "You are a German language learning assistant. "
        "The user gives you German text. You will: "
        "1. Estimate the CEFR level of the text (e.g., B2, C1), "
        "2. Rewrite the text in a simplified B1-B2 version, "
        "3. List the top 50 vocabulary words to learn (with definitions), "
        "4. Identify 5 key grammar points used in the text."
    )

    prompt = f"Here is the text:\n\n{text}"

    try:
        response = requests.post(
            url,
            headers=headers,
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
        )
        
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.exceptions.RequestException as req_err:
        return f"❌ Request error: {req_err}"
    except KeyError:
        return f"❌ Unexpected response format:\n{response.text}"
    except Exception as e:
        return f"❌ General error: {e}"
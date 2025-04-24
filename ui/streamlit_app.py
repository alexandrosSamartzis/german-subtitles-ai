# ui/streamlit_app.py
# import all packages
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
from app.parser import find_latest_subtitle_url
from app.fetcher import download_html_to_text, extract_text_between_tags
from app.api import analyze_with_local_model, analyze_german_text_with_chatgpt
import app.api as aapi

# , analyze_with_deepseek


# Add Ollama path if not already in PATH
os.environ["PATH"] += os.pathsep + "/usr/local/bin"

load_dotenv()
st.set_page_config(page_title="German Subtitle Simplifier", layout="wide")

st.title("🇩🇪 German? Simplify IT")
st.markdown(
    """
Welcome! This app helps language learners by analyzing real-world German subtitles from Tagesschau.
It uses AI to simplify the text, extract vocabulary, and highlight grammar insights.
"""
)
# User input: Subtitle XML URL
subtitle_url = st.text_input("Enter the XML URL")

# 🧠 Custom Prompt
st.markdown("### 🧠 Custom Prompt (Optional)")
custom_prompt = st.text_area(
    "Write your own question or instruction to the AI (leave blank to use the default).",
    placeholder="e.g., Please summarize this subtitle in easier German...",
)

# Toggle for model
model_options = [
    "ChatGPT (GPT-4o 🤖)",
    "DeepSeek (Online) 🌐",
    "Mistral 🧠 (local)",
    "Yi:6B 🌸",
    "LLaMA3.2 (Lite) 🐑",
]


model_choice = st.radio(
    "🎛️ Choose a Model:", options=model_options, index=0, horizontal=False
)
if model_choice == "ChatGPT (GPT-4o 🤖)":
    st.markdown("### 🤖 GPT-4o (Cloud)")
    st.write("- 🔍 Most accurate and versatile")
    st.write("- 🌐 Requires internet and API key")
    st.write("- ⚠️ Paid & rate-limited")

elif model_choice == "Mistral 🧠 (local)":
    st.markdown("### Mistral 🧠 (Offline)")
    st.write("- 🔧 Fast, small, and accurate")
    st.write("- ✅ No API cost, runs on your Mac")
    st.write("- 🧪 Best for general summarization")

elif model_choice == "DeepSeek (Online) 🌐":
    st.markdown("### DeepSeek (Online) 🌐")
    st.write("- 🌍 Hosted API access (like ChatGPT)")
    st.write("- 💡 Good general reasoning")
    st.write("- 🔄 Uses your dynamic or default prompt")

elif model_choice == "Yi:6B 🌸":
    st.markdown("### Yi:6B 🌸")
    st.write("- 🧠 Lightweight multilingual model")
    st.write("- 🔤 May perform well on German")
    st.write("- ⚠️ Less documentation, experimental")

elif model_choice == "LLaMA3.2 (Lite) 🐑":
    st.markdown("### LLaMA3.2: Lite 🐑")
    st.write("- ⚡ Very lightweight version")
    st.write("- 🔄 Fast responses, low GPU use")
    st.write("- 📉 Less accurate on nuance")

else:
    st.info("Please select a model to continue.")
    st.stop()

st.markdown("### 🛑 App Controls")

if st.button("❌ Close App"):
    st.warning("Shutting down Streamlit app...")
    os.system("pkill -f streamlit")
    os._exit(0)

# Run button
if st.button("Run Analysis"):
    st.info("🔄 Starting analysis...")

    # Step 1: Resolve the subtitle source
    if subtitle_url.strip() == "":
        st.info("📡 No URL provided. Fetching latest from Tagesschau...")
        subtitle_url_final = find_latest_subtitle_url()
    else:
        subtitle_url_final = subtitle_url.strip()
        st.success(f"✅ Using subtitle from: {subtitle_url_final}")

    if not subtitle_url_final:
        st.error("❌ Could not find a valid subtitle URL.")
        st.stop()

    # Step 2: Download and extract subtitle text
    try:
        xml_raw = download_html_to_text(subtitle_url_final)
        subtitles = extract_text_between_tags(xml_raw)
        cleaned_text = "\n".join(subtitles)

        if not cleaned_text:
            st.error("❌ No subtitle text found in the XML.")
            st.stop()

        st.subheader("📄 Original Subtitle Text")
        st.text_area("Extracted Subtitles", cleaned_text, height=250)

    except Exception as e:
        st.error(f"❌ Error fetching subtitles: {e}")
        st.stop()

    # Step 3: Route to model
    st.subheader("🧠 AI Analysis")

    try:
        if model_choice == "ChatGPT (GPT-4o 🤖)":
            with st.spinner("🔗 Connecting to ChatGPT..."):
                response = analyze_german_text_with_chatgpt(cleaned_text)

        elif model_choice == "DeepSeek (Online) 🌐":
            with st.spinner("💡 DeepSeek is analyzing your text..."):
                response = aapi.analyze_with_deepseek(cleaned_text)

        elif model_choice == "Mistral 🧠 (local)":
            with st.spinner("🧠 Running Mistral locally..."):
                response = analyze_with_local_model("mistral", cleaned_text)

        elif model_choice == "Yi:6B 🌸":
            with st.spinner("🌸 Running Yi locally..."):
                response = analyze_with_local_model("yi:6b", cleaned_text)

        elif model_choice == "LLaMA3.2 (Lite) 🐑":
            with st.spinner("🐑 Running LLaMA3.2 locally..."):
                response = analyze_with_local_model("llama3.2:latest", cleaned_text)

        else:
            st.error("❌ Model not recognized.")
            st.stop()

        # Step 4: Display the result
        st.success("✅ Analysis complete!")
        st.text_area("AI Response", response, height=400)

        # Create filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        model_id = (
            model_choice.split()[0]
            .lower()
            .replace(":", "")
            .replace("(", "")
            .replace(")", "")
        )
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        output_file_init = output_dir / f"output_subtitles_{timestamp}.txt"
        output_file = output_dir / f"{model_id}_response_{timestamp}.txt"

        # Add model header and save
        full_output = f"📌 Model used: {model_choice}\n\n{response}"

        with open(output_file_init, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_output)

        # Notify user
        st.success(f"💾 Saved response to `{output_file.name}`")
        st.download_button("📥 Download", full_output, file_name=output_file.name)

    except Exception as e:
        st.error(f"❌ Error running model: {e}")

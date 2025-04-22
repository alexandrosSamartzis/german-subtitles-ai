# ui/streamlit_app.py
# import all packages
import streamlit as st
from pathlib import Path
import os

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

# Toggle for model

use_local_model = st.toggle("Use Local Model (instead of ChatGPT)")
model = (
    st.markdown(
        "### ✅ <span style='color:green'>Local Model Enabled</span>",
        unsafe_allow_html=True,
    )
    if use_local_model
    else st.markdown(
        "### 🌐 <span style='color:red'>ChatGPT (Online)\
                                                                    Enabled</span>",
        unsafe_allow_html=True,
    )
)
st.divider()

st.markdown("### 🛑 App Controls")

if st.button("❌ Close App"):
    st.warning("Shutting down Streamlit app...")
    os.system("pkill -f streamlit")
    os._exit(0)

# Run button
if st.button("Run Analysis"):
    if subtitle_url.strip() == "":
        st.warning("The app has collected the last episode from Tageschau.")
    else:
        st.info(f"🔄 Processing subtitles:")
        # Here we will add logic to:
        # 1. Fetch XML
        # 2. Extract text
        # 3. Analyze with ChatGPT or local model
        # 4. Display results

        # Placeholder output for now
        st.success(
            "✅ Subtitle processed! (This is a placeholder for the AI response.)"
        )
        st.code(
            "Simplified text, vocabulary, and grammar will appear here.",
            language="text",
        )

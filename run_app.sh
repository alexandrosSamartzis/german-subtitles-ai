#!/bin/zsh

# Activate conda and environment
source ~/miniconda3/etc/profile.d/conda.sh  # Or ~/anaconda3/... depending on your install
conda activate german-subtitles-ai

# Navigate to project folder (adjust if needed)
cd ~/Users/alexandros/IT/german-subtitles-ai-folder/gerlearn

# Run the Streamlit app
streamlit run ui/streamlit_app.py


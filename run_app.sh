##!/bin/zsh
#
## Activate conda and environment
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate subtitle-clean
#
## Navigate to project folder (adjust if needed)
cd ~/IT/german-subtitles-ai-folder/gerlearn
#
## Run the Streamlit app
streamlit run ui/streamlit_app.py
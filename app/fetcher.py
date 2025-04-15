# fetcher data from url
import requests

def download_html_to_text(url):
    # Download the HTML content
    response = requests.get(url)
    response.encoding = 'utf-8'  # ✅ Fix encoding for German characters
    return response.text
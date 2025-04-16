# parser
import requests
import re


def find_latest_subtitle_url():
    """
    Scrape the Tagesschau homepage and find the most recent untertitel-XXXXX.xml subtitle URL.
    """
    homepage_url = "https://www.tagesschau.de/"
    response = requests.get(homepage_url)
    if response.status_code != 200:
        print("❌ Failed to load homepage.")
        return None
    response.encoding = "utf-8"  # 👈 Force correct encoding
    text = response.text

    # Search for pattern like 'untertitel-73358.xml'
    matches = re.findall(r"untertitel-\d+\.xml", text)

    if matches:
        # Use the first one found (likely the most recent)
        subtitle_path = matches[0]
        full_url = f"https://www.tagesschau.de/multimedia/video/{subtitle_path}"
        print(f"✅ Found subtitle URL: {full_url}")
        return full_url
    else:
        print("❌ No subtitle URL found.")
        return None

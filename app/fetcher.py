# fetcher data from url
import requests
import re


def download_html_to_text(url):
    # Download the HTML content
    response = requests.get(url)
    response.encoding = "utf-8"  # ✅ Fix encoding for German characters
    return response.text


def extract_text_between_tags(xml_content: str) -> list[str]:
    """
    Extracts all subtitle lines from XML content using regex.
    Looks for <tt:span style="textWhite">...</tt:span>
    """
    pattern = r'<tt:span style="textWhite">(.*?)</tt:span>'
    return re.findall(pattern, xml_content)

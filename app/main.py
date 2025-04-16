from docx import Document
import re
from parser import find_latest_subtitle_url
from pathlib import Path
from datetime import datetime
from fetcher import download_html_to_text
from api import analyze_german_text_with_chatgpt
from pathlib import Path


def extract_text_between_tags(xml_content):
    # Regex pattern to find text within <tt:span style="textWhite">...</tt:span>
    pattern = r"<tt:span style=\"textWhite\">(.*?)</tt:span>"
    return re.findall(pattern, xml_content)


def save_extracted_text_to_docx(text_list, output_path):
    doc = Document()
    for text in text_list:
        doc.add_paragraph(text)
    doc.save(output_path)
    print(f"✅ DOCX saved to: {output_path}")


# Combine subtitles into a single string


def main():
    # Step 1: Get the latest subtitle XML URL
    xml_url = find_latest_subtitle_url()
    if not xml_url:
        exit("❌ Could not find subtitle XML.")

    # Step 2: Download XML content
    xml_content = download_html_to_text(xml_url)

    # Step 3: Extract subtitle lines
    extracted_texts = extract_text_between_tags(xml_content)

    # Optional print
    print("📝 Extracted Texts:")
    for line in extracted_texts:
        print(line)

    # Step 4: Save results to DOCX
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"subtitles_{timestamp}.docx"
    save_extracted_text_to_docx(extracted_texts, output_file)
    analysis = analyze_german_text_with_chatgpt(extracted_texts)

    # Save result
    output_path = Path("data") / f"chatgpt_analysis_{timestamp}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(analysis)

    print(f"📊 ChatGPT analysis saved to: {output_path}")


if __name__ == "__main__":
    main()

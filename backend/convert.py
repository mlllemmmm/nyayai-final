import os
import pdfplumber

RAW_FOLDER = "data/raw_acts"
OUTPUT_FOLDER = "data/processed_text"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for filename in os.listdir(RAW_FOLDER):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(RAW_FOLDER, filename)
        txt_filename = filename.replace(".pdf", ".txt")
        txt_path = os.path.join(OUTPUT_FOLDER, txt_filename)

        print(f"Converting {filename}...")

        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved {txt_filename}")

print("All acts converted successfully!")
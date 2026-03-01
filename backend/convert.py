import os
import pdfplumber

# ---------------- FOLDERS ---------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_FOLDER = os.path.join(BASE_DIR, "data", "raw_acts")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "data", "processed_text")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Raw folder:", RAW_FOLDER)
print("Output folder:", OUTPUT_FOLDER)

# ---------------- CONVERSION ---------------- #
for filename in os.listdir(RAW_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(RAW_FOLDER, filename)
    txt_filename = filename.replace(".pdf", ".txt")
    txt_path = os.path.join(OUTPUT_FOLDER, txt_filename)

    # Skip if already converted
    if os.path.exists(txt_path):
        print(f"Skipping {filename} (already converted)")
        continue

    print(f"Converting {filename}...")

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()

                if page_text:
                    # Basic cleaning
                    page_text = page_text.strip()
                    text += page_text + "\n\n"
                else:
                    print(f"⚠ Warning: No text extracted on page {page_number} of {filename}")

        if not text.strip():
            print(f"❌ No readable text found in {filename}. It may be a scanned PDF.")
            continue

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Saved {txt_filename}")

    except Exception as e:
        print(f"❌ Error processing {filename}: {str(e)}")

print("\nAll conversions completed!")
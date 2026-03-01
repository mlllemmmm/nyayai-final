import os
import re
import shutil
from sentence_transformers import SentenceTransformer
import chromadb

# ---------------- CONFIG ---------------- #
DATA_FOLDER = "data/processed_text"
VECTOR_PATH = "vector_db"
COLLECTION_NAME = "nyayaai_acts"

# ---------------- Clean Old DB ---------------- #
if os.path.exists(VECTOR_PATH):
    print("Deleting old vector database...")
    shutil.rmtree(VECTOR_PATH)

# ---------------- Load Embedding Model ---------------- #
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- Create Chroma Client ---------------- #
client = chromadb.PersistentClient(path=VECTOR_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)

# ---------------- Section Splitter ---------------- #
def split_by_sections(text):
    """
    Splits Indian bare act text by numbered sections like:
    1.
    2.
    3.
    """
    pattern = r'\n(?=\d+\.\s)'
    sections = re.split(pattern, text)

    structured_sections = []

    for sec in sections:
        sec = sec.strip()

        # Skip small junk chunks
        if len(sec) < 100:
            continue

        match = re.match(r'(\d+)\.\s*(.*)', sec)
        if match:
            section_number = match.group(1)

            # Embed section number inside text
            section_text = f"Section {section_number}:\n{sec}"

            structured_sections.append((section_number, section_text))

    return structured_sections


# ---------------- Ingestion ---------------- #
print("Starting ingestion...")

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".txt"):
        filepath = os.path.join(DATA_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        sections = split_by_sections(text)

        print(f"Ingesting {filename} ({len(sections)} sections)...")

        for section_number, section_text in sections:

            embedding = model.encode(section_text).tolist()

            collection.add(
                documents=[section_text],
                embeddings=[embedding],
                metadatas=[{
                    "act": filename.replace(".txt", ""),
                    "section": section_number
                }],
                ids=[f"{filename}_section_{section_number}"]
            )

print("All acts embedded successfully!")
print("Total documents in collection:", collection.count())
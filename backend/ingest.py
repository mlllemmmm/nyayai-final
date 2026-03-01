import os
from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create persistent Chroma client
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_or_create_collection("nyayaai_acts")

DATA_FOLDER = "data/processed_text"

def chunk_text(text, chunk_size=800):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".txt"):
        filepath = os.path.join(DATA_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        print(f"Ingesting {filename}...")

        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk)

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"act": filename.replace(".txt", "")}],
                ids=[f"{filename}_{i}"]
            )

print("All acts embedded successfully!")
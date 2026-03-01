from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from groq import Groq
import os
import re

# ---------------- Load Environment ---------------- #
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

groq_client = Groq(api_key=api_key)

# ---------------- FastAPI Setup ---------------- #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Load Vector DB ---------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_PATH = os.path.join(BASE_DIR, "vector_db")

client = chromadb.PersistentClient(path=VECTOR_PATH)
collection = client.get_collection("nyayaai_acts")

print("Collection Count:", collection.count())

# ---------------- Request Models ---------------- #
class Question(BaseModel):
    question: str

class ActRequest(BaseModel):
    act_name: str


# ---------------- Utility Functions ---------------- #

def extract_section(query: str):
    match = re.search(r'section\s*(\d+[A-Za-z]*)', query, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def detect_act_intent(query: str):
    query = query.lower()

    ROUTING = {
        "transfer_of_property": [
            "landlord", "tenant", "lease", "rent",
            "eviction", "notice", "vacate", "terminate", "property"
        ],
        "ipc": [
            "murder", "theft", "assault", "harassment",
            "cheating", "violence", "threat", "criminal"
        ],
        "consumeract": [
            "consumer", "defective product", "refund",
            "unfair trade practice"
        ],
        "protection_of_womendv": [
            "domestic violence", "husband beating",
            "in-laws harassment", "abuse by husband"
        ],
        "child_marriage": [
            "child marriage"
        ],
        "motorvehicles": [
            "accident", "drunk driving", "license",
            "rash driving"
        ],
        "rightoinformation": [
            "rti", "right to information"
        ],
        "dpdp": [
            "data protection", "privacy", "personal data"
        ],
        "firbail": [
            "fir", "bail", "anticipatory bail"
        ],
        "married_womans_act": [
            "married woman property"
        ],
        "protection_of_children": [
            "child abuse", "minor protection"
        ]
    }

    for act_key, keywords in ROUTING.items():
        if any(word in query for word in keywords):
            return act_key

    return None


# ---------------- RAG Pipeline ---------------- #

def rag_pipeline(user_query: str):

    try:
        print("RAG PIPELINE CALLED")

        section_number = extract_section(user_query)
        detected_act = detect_act_intent(user_query)

        # -------- 1️⃣ If Section Mentioned -------- #
        if section_number:
            print("Section detected:", section_number)

            results = collection.query(
                query_texts=[user_query],
                where={"section": section_number},
                n_results=5,
                include=["documents", "metadatas", "distances"]
            )

        # -------- 2️⃣ If Act Intent Detected -------- #
        elif detected_act:
            print("Act routed to:", detected_act)

            results = collection.query(
                query_texts=[user_query],
                where={"act": detected_act},
                n_results=8,
                include=["documents", "metadatas", "distances"]
            )

        # -------- 3️⃣ Otherwise Semantic Search -------- #
        else:
            rewrite_prompt = f"""
You are a legal query optimizer.

Convert the user's question into a structured Indian legal search query.
Include relevant legal keywords and concepts.

User Query: {user_query}

Return only the improved search query.
"""

            rewrite_response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": rewrite_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0
            )

            expanded_query = rewrite_response.choices[0].message.content.strip()

            results = collection.query(
                query_texts=[expanded_query],
                n_results=8,
                include=["documents", "metadatas", "distances"]
            )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return "No relevant legal information found in the database."

        # -------- Deduplicate Sections -------- #
        seen_sections = set()
        filtered_docs = []

        for doc, meta in zip(documents, metadatas):
            section = meta.get("section", "")
            if section not in seen_sections:
                seen_sections.add(section)
                filtered_docs.append((doc, meta))

        # -------- Build Retrieved Context -------- #
        retrieved_text = ""

        for i, (doc, meta) in enumerate(filtered_docs):
            act_name = meta.get("act", "Unknown Act")
            section = meta.get("section", "Unknown Section")

            retrieved_text += f"""
[Source {i+1}]
Act: {act_name}
Section: {section}

{doc}

"""

        # -------- Final Prompt -------- #
        final_prompt = f"""
You are NyayaAI, an expert Indian legal assistant.

STRICT RULES:
- Use ONLY the provided legal text.
- Do NOT introduce new laws.
- Quote sections accurately.
- If law not found, clearly say so.

---------------------------------------
USER QUESTION:
{user_query}
---------------------------------------

LEGAL TEXT:
{retrieved_text}

---------------------------------------

Respond strictly in this format:

### Relevant Law
(Quote exact section text and mention Act + Section + Source number)

### Explanation
(Simple explanation in plain English)

### What You Can Do
(Practical legal steps based strictly on cited law)
"""

        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1
        )

        answer = chat_completion.choices[0].message.content

        # -------- Optional Confidence Check -------- #
        if distances and min(distances) > 1.5:
            answer += "\n\n⚠️ Low confidence retrieval. Consider rephrasing your question."

        return answer

    except Exception as e:
        return f"Error generating response: {str(e)}"


# ---------------- Ask Endpoint ---------------- #

@app.post("/ask")
def ask(question: Question):
    answer = rag_pipeline(question.question)
    return {"answer": answer}


# ---------------- Explain Act Endpoint ---------------- #

@app.post("/explain-act")
def explain_act(request: ActRequest):

    results = collection.query(
        query_texts=[request.act_name],
        where={"act": request.act_name},
        n_results=30,
        include=["documents", "metadatas"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {"answer": "Act not found in database."}

    combined_text = ""

    for doc, meta in zip(documents, metadatas):
        section = meta.get("section", "Unknown Section")
        combined_text += f"\nSection {section}:\n{doc}\n"

    summary_prompt = f"""
You are NyayaAI.

Summarize the following Act in simple language.
Highlight:
- Key rights
- Offences
- Remedies

ACT CONTENT:
{combined_text}
"""

    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": summary_prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.1
    )

    return {"answer": chat_completion.choices[0].message.content}
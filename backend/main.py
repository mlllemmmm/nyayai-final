from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from groq import Groq
import os
import re
import tempfile
import base64
import edge_tts

# ---------------- Load Environment ---------------- #
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

groq_client = Groq(api_key=GROQ_API_KEY)

# ---------------- FastAPI Setup ---------------- #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    return match.group(1) if match else None


def detect_act_intent(query: str):
    query = query.lower()

    ROUTING = {
        "transfer_of_property": [
            "landlord", "tenant", "lease", "rent",
            "eviction", "notice", "vacate", "terminate"
        ],
        "ipc": [
            "murder", "theft", "assault", "harassment",
            "cheating", "violence", "threat", "criminal"
        ],
        "consumeract": [
            "consumer", "refund", "defective product",
            "unfair trade practice"
        ],
        "protection_of_womendv": [
            "domestic violence", "husband beating",
            "in-laws harassment"
        ],
        "child_marriage": ["child marriage"],
        "motorvehicles": ["accident", "drunk driving", "license"],
        "rightoinformation": ["rti", "right to information"],
        "dpdp": ["data protection", "privacy", "personal data"],
        "firbail": ["fir", "bail", "anticipatory bail"],
        "married_womans_act": ["married woman property"],
        "protection_of_children": ["child abuse", "minor protection"]
    }

    for act_key, keywords in ROUTING.items():
        if any(word in query for word in keywords):
            return act_key

    return None


# ---------------- RAG Pipeline ---------------- #

def rag_pipeline(user_query: str):
    try:
        section_number = extract_section(user_query)
        detected_act = detect_act_intent(user_query)

        # 1️⃣ Section-specific search
        if section_number:
            results = collection.query(
                query_texts=[user_query],
                where={"section": section_number},
                n_results=5,
                include=["documents", "metadatas"]
            )

        # 2️⃣ Act-based routing
        elif detected_act:
            results = collection.query(
                query_texts=[user_query],
                where={"act": detected_act},
                n_results=8,
                include=["documents", "metadatas"]
            )

        # 3️⃣ Semantic fallback
        else:
            results = collection.query(
                query_texts=[user_query],
                n_results=8,
                include=["documents", "metadatas"]
            )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:
            return "No relevant legal information found in the database."

        retrieved_text = ""
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            act_name = meta.get("act", "Unknown Act")
            section = meta.get("section", "Unknown Section")

            retrieved_text += f"""
[Source {i+1}]
Act: {act_name}
Section: {section}

{doc}

"""

        final_prompt = f"""
You are NyayaAI, an Indian legal assistant.

Use ONLY the provided legal text.

USER QUESTION:
{user_query}

LEGAL TEXT:
{retrieved_text}

Respond in this format:

### Relevant Law
(Quote section + Act + Source number)

### Explanation
(Simple explanation)

### What You Can Do
(Practical steps)
"""

        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"


# ---------------- Ask Endpoint ---------------- #

@app.post("/ask")
def ask(question: Question):
    return {"answer": rag_pipeline(question.question)}


# ---------------- Explain Act Endpoint ---------------- #

@app.post("/explain-act")
def explain_act(request: ActRequest):
    return {"answer": rag_pipeline(request.act_name)}


# ---------------- Voice Query Endpoint ---------------- #

@app.post("/api/voice-query")
async def voice_query(audio: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
        tmp_file.write(await audio.read())
        tmp_path = tmp_file.name

    try:
        # 1️⃣ Transcribe using Groq Whisper
        with open(tmp_path, "rb") as audio_file:
            transcript_response = groq_client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=("audio.webm", audio_file.read())
            )

        transcript = transcript_response.text

        # 2️⃣ Get legal answer
        text_response = rag_pipeline(transcript)

        # 3️⃣ Convert to speech
        tts_path = tmp_path + "_tts.mp3"
        communicate = edge_tts.Communicate(text_response, "en-IN-NeerjaNeural")
        await communicate.save(tts_path)

        with open(tts_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        os.remove(tts_path)

        return {
            "transcript": transcript,
            "text_response": text_response,
            "audio_base64": audio_base64
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
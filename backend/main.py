from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
import os
import tempfile
import base64

# ---------------- Load Environment ---------------- #
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# ---------------- Initialize AI Clients ---------------- #
groq_client = Groq(api_key=api_key)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- FastAPI Setup ---------------- #
# ---------------- FastAPI Setup ---------------- #
from fastapi import FastAPI, UploadFile, File
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Load Vector DB ---------------- #
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_collection("nyayaai_acts")

# ---------------- Request Models ---------------- #
class Question(BaseModel):
    question: str

class ActRequest(BaseModel):
    act_name: str


# ---------------- RAG Pipeline ---------------- #
def rag_pipeline(user_query: str):

    # Retrieve relevant chunks
    results = collection.query(
        query_texts=[user_query],
        n_results=5
    )

    if not results["documents"] or not results["documents"][0]:
        return "No relevant legal information found in the database."

    retrieved_text = " ".join(results["documents"][0])

    prompt = f"""
You are NyayaAI, a professional Indian legal assistant.

STRICT RULES:
- Use ONLY the legal text provided below.
- Do NOT use outside knowledge.
- Do NOT guess or assume.
- If the answer is not clearly present in the legal text, say:
  "The provided legal text does not contain sufficient information to answer this question."
- Do NOT fabricate sections, case laws, or punishments.
- Do NOT hallucinate.

FORMAT YOUR RESPONSE STRICTLY AS:

1. Relevant Law:
(Quote directly from the provided legal text)

2. What it means:
(Simple explanation in plain English)

3. What the person can do:
(Practical guidance strictly based on the text)

---------------------------------------

User Question:
{user_query}

---------------------------------------

Legal Text:
{retrieved_text}
"""

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2   # Low temperature = less hallucination
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"


# ---------------- RAG Ask Endpoint ---------------- #
@app.post("/ask")
def ask(question: Question):

    answer = rag_pipeline(question.question)

    return {
        "answer": answer
    }


# ---------------- RAG Explain Act Endpoint ---------------- #
@app.post("/explain-act")
def explain_act(request: ActRequest):

    answer = rag_pipeline(request.act_name)

    return {
        "answer": answer
    }


# ---------------- Voice Query Endpoint ---------------- #
import edge_tts
import asyncio

@app.post("/api/voice-query")
async def voice_query(audio: UploadFile = File(...)):
    # 1. Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
        tmp_file.write(await audio.read())
        tmp_path = tmp_file.name

    try:
        # 2. Transcribe using Groq Whisper
        with open(tmp_path, "rb") as audio_file:
            transcript_response = groq_client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=("audio.webm", audio_file.read())
            )
        transcript = transcript_response.text

        # 3. Get legal text based on transcript
        results = collection.query(
            query_texts=[transcript],
            n_results=5
        )

        retrieved_text = "No relevant legal information found in the database."
        if results["documents"] and results["documents"][0]:
            retrieved_text = " ".join(results["documents"][0])

        # 4. Generate AI response focused on spoken context (using Groq Llama 3)
        system_prompt = f"""
You are NyayAI, a calm and clear Indian legal guidance assistant.
Explain laws simply.
Suggest practical next steps.
Avoid legal jargon.
Do not claim to be a lawyer.
Keep spoken responses under 90 seconds.

Use ONLY the legal text provided below. Do NOT hallucinate.

Legal Text:
{retrieved_text}
"""
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        text_response = chat_completion.choices[0].message.content

        # 5. Convert response back to speech using edge-tts (Free Microsoft TTS)
        tts_tmp_path = tmp_path + "_tts.mp3"
        communicate = edge_tts.Communicate(text_response, "en-IN-NeerjaNeural")  # Indian English female voice
        await communicate.save(tts_tmp_path)
        
        # Read the generated audio file and convert to base64
        with open(tts_tmp_path, "rb") as tts_file:
            audio_data = tts_file.read()
            
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Cleanup TTS file
        if os.path.exists(tts_tmp_path):
            os.remove(tts_tmp_path)

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
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from groq import Groq
import os

# ---------------- Load Environment ---------------- #
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# ---------------- Initialize Groq ---------------- #
groq_client = Groq(api_key=api_key)

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
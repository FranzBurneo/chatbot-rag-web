from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.llms import LlamaCpp
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODELO LLM LOCAL ===
model_path = "./models/openhermes-2.5-mistral-7b.Q5_K_M.gguf"
llm = LlamaCpp(
    model_path=model_path,
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=40,
    temperature=0.3,
    max_tokens=512,
    top_p=0.95,
    use_mlock=False,
    use_mmap=True,
    verbose=False
)

# === EMBEDDINGS Y VECTORSTORE ===
#embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")

vectorstore = Chroma(
    persist_directory="db",
    collection_name="creditos",
    embedding_function=embedding
)

# === PROMPT PERSONALIZADO ===
custom_prompt = PromptTemplate.from_template("""
Eres el chatbot de CoopMego. Responde preguntas en español, de forma directa y clara, usando únicamente el siguiente contexto:

{context}

No respondas preguntas que no estén explícitamente solicitadas. No incluyas preguntas nuevas en tus respuestas.

Pregunta: {question}
Respuesta:
""")

# === QA CHAIN ===
retriever = vectorstore.as_retriever(search_type="similarity", k=2)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": custom_prompt}
)

greetings = ["hola", "buenos días", "buenas", "buenas tardes", "saludos", "me puedes ayudar"]

@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    question = data.get("question", "").lower().strip()

    if any(greet in question for greet in greetings):
        return {
            "answer": "¡Hola! Soy el chatbot de CoopMego. Estoy aquí para ayudarte con información sobre créditos, tasas de interés y otros servicios. ¿En qué puedo ayudarte?"
        }

    result = qa_chain.run(question)
    return {"answer": result}
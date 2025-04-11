from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CONFIGURACIÓN DEL MODELO LOCAL ===
model_path = "./models/openhermes-2.5-mistral-7b.Q4_K_M.gguf"
llm = Llama(
    model_path=model_path,
    n_ctx=4096,               # Más contexto, útil para RAG
    n_threads=4,              # ⚠️ Menor uso de CPU
    n_gpu_layers=20,          # ⚠️ Menor carga en GPU
    verbose=False
)

# === CONFIGURACIÓN DE CHROMA ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="db",
    collection_name="creditos",
    embedding_function=embedding
)

# === ENDPOINT DEL CHAT ===
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    question = data.get("question", "")

    # Recuperar contexto relevante
    docs = vectorstore.similarity_search(question, k=2)
    context = "\n".join(doc.page_content for doc in docs)

    # Construcción del prompt
    prompt = (
        "Eres un asistente de créditos amigable y experto en temas financieros.\n"
        "Usa el siguiente contexto para responder la pregunta del usuario en español.\n\n"
        f"{context}\n\n"
        f"Pregunta: {question}\n"
        "Respuesta:"
    )

    # Generar respuesta
    output = llm(
        prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        stop=["Pregunta:", "Usuario:"],
    )

    answer = output["choices"][0]["text"].strip()
    return {"answer": answer}
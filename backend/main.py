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
model_path = "./models/openhermes-2.5-mistral-7b.Q4_K_M.gguf"
llm = LlamaCpp(
    model_path=model_path,
    n_ctx=2048,               
    n_threads=6,              
    n_gpu_layers=30,          
    temperature=0.7,
    max_tokens=400,           
    top_p=0.95,
    stop=["Usuario:", "Pregunta:"],
    use_mlock=False,
    use_mmap=True,
    verbose=False
)

# === EMBEDDINGS Y VECTORSTORE (más compatible) ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="db",
    collection_name="creditos",
    embedding_function=embedding
)

# === PROMPT PERSONALIZADO ===
custom_prompt = PromptTemplate.from_template(
    """Eres un asistente experto en créditos que responde en español basándote solo en el siguiente contexto:

{context}

Pregunta del usuario: {question}

Respuesta:"""
)

# === QA CHAIN ===
retriever = vectorstore.as_retriever(search_type="similarity", k=2)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": custom_prompt}
)

# === ENDPOINT ===
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    question = data.get("question", "")
    result = qa_chain.run(question)
    return {"answer": result}
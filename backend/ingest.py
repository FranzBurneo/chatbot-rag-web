from langchain_community.document_loaders import UnstructuredHTMLLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# === CARGAR DOCUMENTOS HTML Y CLASIFICAR POR TIPO DE CRÉDITO ===
docs_info = [
    ("docs/credito_negocio.html", "Crédito para negocios"),
    ("docs/credito_personal.html", "Crédito personal")
]

documents = []
for file_path, tipo_credito in docs_info:
    loader = UnstructuredHTMLLoader(file_path)
    loaded_docs = loader.load()
    for doc in loaded_docs:
        doc.metadata["tipo_credito"] = tipo_credito
    documents.extend(loaded_docs)

# === CARGAR DOCUMENTO ADICIONAL DE SIMULADORES (sin clasificación) ===
simuladores = TextLoader("docs/simuladores.md").load()
documents.extend(simuladores)

# === DIVISIÓN EN CHUNKS ===
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# === EMBEDDINGS ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === GUARDAR EN CHROMA ===
db = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="db",
    collection_name="creditos"
)

print("✅ Ingesta finalizada: documentos clasificados y base vectorial generada.")
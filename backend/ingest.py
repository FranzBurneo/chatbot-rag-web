from langchain_community.document_loaders import UnstructuredHTMLLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# === Cargar documentos HTML ===
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

# === Cargar documento adicional de simuladores ===
simuladores = TextLoader("docs/simuladores.md").load()
documents.extend(simuladores)

# === Cargar PDFs con información de tasas ===
pdf_files = [
    "docs/tasas-de-interés-activas-y-pasivas-1.pdf",
    "docs/tasas-de-interés-y-tarifarios-de-productos-y-servicios-1.pdf"
]

for pdf_file in pdf_files:
    pdf_loader = PyPDFLoader(pdf_file)
    pdf_docs = pdf_loader.load()
    for doc in pdf_docs:
        doc.metadata["tipo_documento"] = "tasas_y_tarifas"
    documents.extend(pdf_docs)

# === División en chunks ===
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# === Embeddings ===
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === Guardar en Chroma ===
db = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="db",
    collection_name="creditos"
)

print("✅ Ingesta finalizada: documentos HTML, simuladores y PDFs cargados y base vectorial generada.")
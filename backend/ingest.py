from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import re

# === Cargar HTML ===
docs_info = [
    ("docs/credito_negocio.html", "Crédito para negocios"),
    ("docs/credito_personal.html", "Crédito personal")
]

documents = []
for path, tipo in docs_info:
    loader = UnstructuredHTMLLoader(path)
    loaded = loader.load()
    for doc in loaded:
        doc.page_content = re.sub(r"Pregunta del usuario:\s*", "", doc.page_content, flags=re.IGNORECASE)
        doc.page_content = re.sub(r"Respuesta:\s*", "", doc.page_content, flags=re.IGNORECASE)
        doc.metadata["tipo_credito"] = tipo
    documents.extend(loaded)

# === Simuladores ===
documents.extend(TextLoader("docs/recursos_utiles.md", encoding="utf-8").load())

# === PDFs ===
pdfs = [
    "docs/tasas-de-interés-activas-y-pasivas-1.pdf",
    "docs/tasas-de-interés-y-tarifarios-de-productos-y-servicios-1.pdf"
]
for file in pdfs:
    loader = PyPDFLoader(file)
    pdf_docs = loader.load()
    for doc in pdf_docs:
        doc.metadata["tipo_documento"] = "tasas_y_tarifas"
    documents.extend(pdf_docs)

# === Chunking ===
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# === Embeddings (versión final y correcta) ===
embedding = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")

# === Guardar en Chroma ===
db = Chroma.from_documents(
    docs, embedding,
    persist_directory="db",
    collection_name="creditos"
)

print("✅ Ingesta completada correctamente.")
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# 1. Cargar los HTMLs desde la carpeta /docs
loaders = [
    UnstructuredHTMLLoader("docs/credito_negocio.html"),
    UnstructuredHTMLLoader("docs/credito_personal.html"),
]

documents = []
for loader in loaders:
    documents.extend(loader.load())

# 2. Dividir el texto en chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# 3. Crear embeddings
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Guardar en Chroma (no se usa db.persist())
db = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="db",
    collection_name="creditos"
)

print("✅ Base de datos vectorial generada correctamente.")
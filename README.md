# 🧠 Asistente de Créditos - Chatbot RAG

Este proyecto es un chatbot conversacional que responde preguntas sobre productos crediticios utilizando técnicas de RAG (Retrieval-Augmented Generation) y un modelo LLM local (`OpenHermes-2.5-Mistral`) corriendo con `llama-cpp-python`.

---

## 🚀 Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) - Backend del chatbot
- [LangChain](https://www.langchain.com/) - Orquestación del flujo RAG
- [ChromaDB](https://www.trychroma.com/) - Vectorstore local persistente
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - Carga del modelo en `.gguf`
- [HuggingFace Transformers](https://huggingface.co/) - Embeddings (`MiniLM-L6-v2`)
- [React + Chakra UI](https://chakra-ui.com/) - Frontend moderno y adaptable

---

## 📦 Instalación del backend

### 1. Clona el repositorio

```bash
https://github.com/FranzBurneo/chatbot-rag-web.git
cd chatbot-rag-web/backend
```

### 2. Crea y activa el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

### 4. Descarga el modelo GGUF

Descarga `openhermes-2.5-mistral-7b.Q4_K_M.gguf` desde:
https://huggingface.co/NousResearch/OpenHermes-2.5-Mistral-7B-GGUF

Y colócalo en la carpeta:

```
backend/models/openhermes-2.5-mistral-7b.Q4_K_M.gguf
```

---

## 📄 Carga de documentos (RAG)

Coloca los HTMLs informativos en `backend/docs/`, por ejemplo:

- `credito_negocio.html`
- `credito_personal.html`

Luego ejecuta:

```bash
python ingest.py
```

Esto cargará los documentos, los dividirá en chunks y los almacenará como vectores en `backend/db/`.

---

## ▶️ Ejecución del backend

```bash
uvicorn main:app --reload --port 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 💬 Ejecución del frontend (React + Chakra UI)

Desde la carpeta del frontend:

```bash
npm install
npm run dev
```

Asegúrate de que la URL `http://localhost:5173` tenga acceso CORS en `main.py`.

---

## ⚙️ Ajustes para optimizar rendimiento

Si quieres reducir consumo de CPU (aunque tome más tiempo), ajusta en `main.py`:

```python
n_threads=4
n_gpu_layers=0
n_ctx=4096
```

---

## 🧪 Preguntas de prueba

Puedes preguntarle cosas como:

- ¿Qué tipos de crédito ofrecen?
- ¿Cuánto tiempo dura el plazo de pago?
- ¿Cuáles son los requisitos para crédito personal?
- ¿Puedo elegir el día de pago de mi cuota?
- ¿Hay costos por cancelación anticipada?

---

## 📁 Estructura del proyecto

```
chatbot-rag-web/
├── backend/
│   ├── main.py
│   ├── ingest.py
│   ├── requirements.txt
│   ├── db/                  # Chroma persistido
│   ├── docs/                # HTMLs con la información
│   └── models/              # Modelo GGUF
└── frontend/                # Aplicación React
```

---

## 👤 Autores

**Franz Burneo Monteros**
**[David Burneo Valencia](https://github.com/daburneo1)** 
Ingeniero en Sistemas
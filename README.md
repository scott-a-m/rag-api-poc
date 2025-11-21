# RAG API - Proof of Concept

This is a proof of concept for a Retrieval-Augmented Generation (RAG) API built with FastAPI.

It provides endpoints to:
- upload PDF documents and create embeddings from their text,
- query the uploaded documents via an LLM-backed RAG flow,
- inspect and manage the Chroma vector store used for retrieval.

## Quick facts

- Language: Python
- Web framework: FastAPI
- Vector DB: Chroma (persisted to local `chroma/` directory)
- Embeddings & LLM adapters: Ollama-based adapters (via `langchain_ollama` / `langchain_chroma`)

## Project structure

- `app.py` - FastAPI application and route definitions (entrypoint)
- `dependencies.py` - dependency providers for FastAPI (factories and adapters)
- `services/` - core business logic:
	- `embeddings_service.py` - creates chunks and writes embeddings to Chroma
	- `vector_db_service.py` - wraps Chroma usage (add, retrieve, stats, delete)
	- `rag_query_service.py` - thin service delegating RAG queries to an adapter
	- `file_service.py` - helpers for saving/validating/removing uploaded files
- `adapters/` - adapter implementations for loaders, splitters and RAG handler
	- `adapters/loaders/loader_adapters.py` - wraps `PyPDFLoader` and `TextLoader`
- `factories/pdf_loader_factory.py` - factory used to create PDF loader adapters
- `protocols/protocols.py` - typed protocols used across the project
- `chroma/` - Chroma persistence folder (contains `chroma.sqlite3` in this repo)

## Environment variables

The app reads a few environment variables used to configure paths, models and Chroma settings. Defaults are provided in `dependencies.py` and `services/vector_db_service.py`.

- `TEMP_DIR` - temporary folder where uploaded files are saved (default `\temp` on Windows)
- `LLM_MODEL` - LLM model name passed to the RAG adapter (default `mistral`)
- `CHROMA_PATH` - directory used by Chroma to persist the DB (default `chroma`)
- `COLLECTION_NAME` - Chroma collection name (default `my-rag`)
- `TEXT_EMBEDDING_MODEL` - embedding model name used by Ollama embeddings (default `nomic-embed-text`)

## Requirements & Recommended packages

The project imports the following packages (used in the codebase). Install the latest compatible versions for your Python environment:

- fastapi
- uvicorn
- werkzeug
- langchain_ollama
- langchain_chroma
- langchain_community
- langchain_core

## Ollama (local LLM & embeddings)

This project uses Ollama-backed adapters for embeddings and LLM calls (via `langchain_ollama` and `langchain_chroma`). If you plan to run the embeddings/LLM locally you must install and run Ollama so the adapters can reach the models.

High-level guidance:

- Official docs / installation: follow the Ollama documentation at https://ollama.com/docs for the most up-to-date install instructions.


Example (after installing Ollama):

```bash
# list available models on your Ollama host
ollama ls

# pull the LLM and embedding models you want to use (replace names with valid Ollama model identifiers)
ollama pull mistral
ollama pull nomic-embed-text
```

## Virtual environment (Windows PowerShell)

Follow these steps to create and activate a virtual environment and install the (example) dependencies.

```powershell
# create a virtual environment in the project folder
python -m venv .venv

# activate the virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# install example dependencies (replace with pinned deps in requirements.txt)
pip install --upgrade pip
pip install fastapi uvicorn werkzeug langchain_ollama langchain_chroma langchain_community langchain_core
```

## How to run (development)

Start the FastAPI app with Uvicorn (from the repository root):

```powershell
# from project root
.\.venv\Scripts\Activate.ps1 ;
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://127.0.0.1:8000 and interactive docs at http://127.0.0.1:8000/docs

## Using Swagger / Interactive API docs

FastAPI provides interactive OpenAPI documentation out of the box. Once the app is running you can use these UIs to explore and test endpoints:

- Swagger UI (interactive, allows trying requests):
	- URL: http://127.0.0.1:8000/docs

From the Swagger UI you can select any endpoint, expand it to see the request schema, provide parameters or files, and execute the request directly from your browser. This is very handy for manual testing during development.

## API Endpoints

The main endpoints provided in `app.py` are:

- POST /embed-document
	- Description: Upload a PDF and add its embedded chunks to Chroma.
	- Request: multipart/form-data with `file` (PDF)
	- Response: JSON message with success/failure

- POST /rag-query
	- Description: Send a text query and get the RAG-produced response (delegates to the configured RAG adapter).
	- Request: JSON body `{ "query": "..." }`
	- Response: JSON with `message` containing the response text

- GET /chroma/collection-stats
	- Description: Returns stats about the Chroma collection (total chunks, chunks per document)

- POST /chroma/delete/{document_name}
	- Description: Delete all chunks associated with the specified `document_name`


## Data persistence

Chroma persistence is stored under the `chroma/` directory in this repo (there is a `chroma.sqlite3` file in the workspace). Keep backups if you need to preserve embedded data.
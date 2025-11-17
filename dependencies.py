import os
from fastapi import Depends
from adapters.ragquery.rag_query_adapters import OllamaRagQueryAdapter
from adapters.splitters.splitter_adapters import RecursiveCharacterSplitterAdapter
from services.embeddings_service import EmbeddingsService
from services.file_service import FileService
from services.rag_query_service import RagQueryService
from services.vector_db_service import VectorDbService
from factories.pdf_loader_factory import PDFLoaderFactory

TEMP_DIR = os.getenv('TEMP_DIR', '\\temp')
LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')

def get_file_service() -> FileService:
    return FileService()

def get_vector_db_service() -> VectorDbService:
    return VectorDbService()

def get_pdf_loader_factory() -> PDFLoaderFactory:
    return PDFLoaderFactory()

def get_text_splitter_adapter() -> RecursiveCharacterSplitterAdapter:
    return RecursiveCharacterSplitterAdapter()

def get_rag_query_adapter(
    vector_db_service: VectorDbService = Depends(get_vector_db_service),
) -> OllamaRagQueryAdapter:
    return OllamaRagQueryAdapter(
        vector_db_service = vector_db_service,
        llm_model = LLM_MODEL
    )

def get_embeddings_service(
    file_service: FileService = Depends(get_file_service),
    vector_db_service: VectorDbService = Depends(get_vector_db_service),
    document_loader_factory: PDFLoaderFactory = Depends(get_pdf_loader_factory),
    splitter: RecursiveCharacterSplitterAdapter = Depends(get_text_splitter_adapter),
) -> EmbeddingsService:
    return EmbeddingsService(
        file_service = file_service,
        vector_db_service = vector_db_service,
        document_loader_factory = document_loader_factory,
        splitter = splitter,
        temp_dir = TEMP_DIR
    )

def get_rag_query_service(rag_query_handler: OllamaRagQueryAdapter = Depends(get_rag_query_adapter)) -> RagQueryService:
    return RagQueryService(rag_query_handler)
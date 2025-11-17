from typing import Protocol, List
from langchain_core.documents import Document

from adapters.loaders.loader_adapters import PDFLoaderAdapter

class DocumentLoader(Protocol):
    def load(self) -> List[Document]: ...

class TextSplitter(Protocol):
    def split_documents(self, docs: List[Document]) -> List[Document]: ...

class VectorDb(Protocol):
    def get_retriever(self): ...
    def add_documents(self, docs: List) -> None: ...

class RagQueryHandler(Protocol):
    def handle_rag_query(self, user_input) -> str : ...

class DocumentLoaderFactory(Protocol):
    def create_pdf_loader(self, file_path: str) -> PDFLoaderAdapter : ...

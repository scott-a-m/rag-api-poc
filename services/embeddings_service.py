import os
from protocols.protocols import DocumentLoaderFactory, TextSplitter
from services.file_service import FileService
from services.vector_db_service import VectorDbService

class EmbeddingsService:

    def __init__(
            self, file_service: FileService, 
            vector_db_service: VectorDbService, 
            document_loader_factory: DocumentLoaderFactory, 
            splitter: TextSplitter, 
            temp_dir: str, 
            chunk_size: int = 800, 
            chunk_overlap: int = 50):
        
        self.file_service = file_service
        self.vector_db_service = vector_db_service
        self.document_loader_factory = document_loader_factory
        self.splitter = splitter
        self.temp_dir = temp_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_chunks(self, file_path):
        loader = self.document_loader_factory.create_pdf_loader(file_path)
        data = loader.load()
        chunks = self.splitter.split_documents(data)

        for chunk in chunks:
            chunk.metadata["document_name"] = os.path.basename(file_path)

        return chunks

    def create_embeddings(self, file):
        if file and self.file_service.validate_file(file.filename, 'pdf'):
            file_path = self.file_service.create_file_path(file.filename, self.temp_dir)
            self.file_service.save_file(file, file_path)
            chunks = self.get_chunks(file_path)
            self.vector_db_service.add_chunks_to_db(chunks)
            self.file_service.remove_file(file_path)

            return True
        
        return False
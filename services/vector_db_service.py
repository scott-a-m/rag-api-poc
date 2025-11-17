import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = os.getenv('CHROMA_PATH', 'chroma')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'my-rag')
TEXT_EMBEDDING_MODEL = os.getenv('TEXT_EMBEDDING_MODEL', 'nomic-embed-text')

class VectorDbService:

    def __init__(self):
        embedding_function = OllamaEmbeddings(model=TEXT_EMBEDDING_MODEL)
        self.db = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function
        )
    
    def get_retriever(self):
        return self.db.as_retriever()
    
    def add_chunks_to_db(self, chunks):
        self.db.add_documents(chunks)

    def get_collection_stats(self):
        collection = self.db._collection
        metadatas = collection.get()["metadatas"]

        total_chunks = len(metadatas)

        doc_counts = {}
        
        for meta in metadatas:
            name = meta.get("document_name", "unknown")
            doc_counts[name] = doc_counts.get(name, 0) + 1

        return {
            "total_chunks": total_chunks,
            "chunks_per_document": doc_counts
        }
    
    def delete_single_document_from_db(self, document_name):
        self.db._collection.delete(where={"document_name": document_name})



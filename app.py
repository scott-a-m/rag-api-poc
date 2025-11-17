from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel
from dependencies import get_embeddings_service, get_rag_query_service, get_vector_db_service
from services.embeddings_service import EmbeddingsService
from services.rag_query_service import RagQueryService
from services.vector_db_service import VectorDbService

app = FastAPI(title="RAG API", version="1.0.0")

class QueryRequest(BaseModel):
    query: str

@app.post("/embed-document")
async def embed_document(
    file: UploadFile = File(...),
    embeddings_service: EmbeddingsService = Depends(get_embeddings_service),
):
    """
    Embed document
    """
        
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file has been selected")

    embedded = embeddings_service.create_embeddings(file)

    if embedded:
        return {"message": "Document embedding has been successful"}
    
    raise HTTPException(status_code=500, detail="Document embedding error")


@app.post("/rag-query")
async def rag_route_query(
    request: QueryRequest,
    rag_query_service: RagQueryService = Depends(get_rag_query_service),
):
    """
    Query documents
    """
        
    response = rag_query_service.handle_query(request.query)

    if response:
        return {"message": response}
    
    raise HTTPException(status_code=500, detail="oops an error occurred")


@app.get("/chroma/collection-stats")
async def chroma_collection_stats(vector_db_service: VectorDbService = Depends(get_vector_db_service)):
    """
    Get stats about the Chroma vector database
    """

    return vector_db_service.get_collection_stats()


@app.post("/chroma/delete/{document_name}")
async def delete_document_from_db(document_name: str, vector_db_service: VectorDbService = Depends(get_vector_db_service)):
    """
    Delete chunks for a specific document
    """
    vector_db_service.delete_single_document_from_db(document_name)

    return {"deleted": True}
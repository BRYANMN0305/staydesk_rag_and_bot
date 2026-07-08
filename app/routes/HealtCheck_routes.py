import os
from fastapi import APIRouter
from app.config.config import settings
from app.schemas.Status_schema import StatusResponse

router = APIRouter(tags=["Basic Healt Check"])


@router.get("/")
async def root():
    return {
        "message": "RAG API está funcionando 🤖",
        "docs": "http://localhost:8000/docs"
    }


@router.get("/status", response_model=StatusResponse)
async def get_status():

    return StatusResponse(
        status="ok",
        vector_store_path=settings.CHROMA_DB_PATH,
        vector_store_exists=os.path.exists(settings.CHROMA_DB_PATH),
        llm_model=settings.LLM_MODEL,
        embedding_model=settings.EMBEDDING_MODEL,
        retriever_k=settings.RETRIEVER_K,
    )

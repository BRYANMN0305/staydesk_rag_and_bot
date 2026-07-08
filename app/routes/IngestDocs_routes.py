from http.client import HTTPException
from fastapi import APIRouter
from app.ingest import run_ingestion
from app.rag_chain import initialize_chain as reinit
global _rag_chain

router = APIRouter(tags=["Document Admin"])


@router.post("/ingest")
async def trigger_ingestion():

    try:
        run_ingestion()
        reinit()
        return {"message": "Ingesta completada. Vector store actualizado."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante la ingesta: {str(e)}"
        )

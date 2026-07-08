import time
from fastapi import APIRouter, HTTPException
from app.rag_chain import get_answer
from app.schemas.Question_schema import QuestionRequest
from app.schemas.Answer_schema import AnswerResponse
from app.schemas.SourceDocument_schema import SourceDocument

router = APIRouter(tags=["Rag Question"])


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):

    start_time = time.time()

    try:
        result = get_answer(request.question)
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Sistema RAG no inicializado: {str(e)}. Ejecuta primero la ingesta."
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Base de datos no encontrada: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la pregunta: {str(e)}"
        )

    processing_time = round(time.time() - start_time, 2)

    return AnswerResponse(
        question=request.question,
        answer=result["answer"],
        sources=[SourceDocument(**s) for s in result["sources"]],
        processing_time_seconds=processing_time,
    )

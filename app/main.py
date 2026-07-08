from app.config.Api import app

from app.routes.HealtCheck_routes import router as health_check_router
from app.routes.IngestDocs_routes import router as ingest_docs_router
from app.routes.RagQuestion_routes import router as rag_question_router

app.include_router(health_check_router)
app.include_router(ingest_docs_router)
app.include_router(rag_question_router)

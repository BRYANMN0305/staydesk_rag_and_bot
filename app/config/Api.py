from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.rag_chain import initialize_chain

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "=" * 60)
    print("INICIANDO SERVIDOR RAG API")
    print("=" * 60)

    try:
        initialize_chain()
        print("Servidor listo para recibir peticiones\n")
    except FileNotFoundError as e:
        print(f"\nADVERTENCIA: {e}")
        print("   El servidor arrancará pero /ask dará error hasta que indexes documentos.")
    except Exception as e:
        print(f"\nError al inicializar: {e}")
        raise

    yield

    print("\nCerrando servidor RAG API...")


app = FastAPI(
    title="RAG API",
    description="Sistema de Retrieval-Augmented Generation con HuggingFace y ChromaDB",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
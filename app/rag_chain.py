from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from app.config.config import settings
from app.utils.prompt_template import PROMPT_TEMPLATE
import os

os.environ["HF_TOKEN"] = settings.API_TOKEN_HUGGINFACEHUB


RAG_PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)


def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store(embeddings: HuggingFaceEmbeddings) -> Chroma:
    import os
    if not os.path.exists(settings.PATH_CHROMA_DB):
        raise FileNotFoundError(
            f"No se encontró la base de datos en '{settings.PATH_CHROMA_DB}'. "
            "Ejecuta primero: python -m app.ingest"
        )
    return Chroma(
        persist_directory=settings.PATH_CHROMA_DB,
        embedding_function=embeddings,
        collection_name=settings.CHROMA_COLLECTION_NAME,
    )


def get_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.LLM_MODEL,
        api_key=settings.API_KEY_GROQ,
        temperature=0.1,
        max_tokens=512,
    )


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


_retriever = None
_chain = None


def initialize_chain():
    global _retriever, _chain
    settings.validate()
    print("Inicializando pipeline RAG...")

    embeddings = get_embeddings()
    vector_store = get_vector_store(embeddings)
    llm = get_llm()

    _retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": settings.RETRIEVER_K, "fetch_k": 20}
    )

    _chain = (
            {"context": _retriever | format_docs, "question": RunnablePassthrough()}
            | RAG_PROMPT
            | llm
            | StrOutputParser()
    )

    print("Pipeline RAG listo")


def get_answer(question: str) -> dict:
    if _chain is None:
        raise RuntimeError("La cadena RAG no está inicializada.")

    source_documents = _retriever.invoke(question)
    answer = _chain.invoke(question)

    sources = []
    for doc in source_documents:
        sources.append({
            "source": doc.metadata.get("source", "Desconocido"),
            "page": doc.metadata.get("page", None),
            "content_preview": doc.page_content[:200] + "..."
        })

    return {
        "answer": answer.strip(),
        "sources": sources,
    }

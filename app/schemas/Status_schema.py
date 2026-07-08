from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str
    vector_store_path: str
    vector_store_exists: bool
    llm_model: str
    embedding_model: str
    retriever_k: int

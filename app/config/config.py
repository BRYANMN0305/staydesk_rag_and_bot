import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_KEY_GROQ: str = os.getenv("API_KEY_GROQ", "")
    API_TOKEN_HUGGINFACEHUB: str = os.getenv("API_TOKEN_HUGGINFACEHUB", "")
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    LLM_MODEL: str = os.getenv(
        "LLM_MODEL",
        "mistralai/Mistral-7B-Instruct-v0.2"
    )
    PATH_CHROMA_DB: str = os.getenv("PATH_CHROMA_DB", "./chroma_db")
    CHROMA_COLLECTION_NAME: str = os.getenv(
        "CHROMA_COLLECTION_NAME",
        "rag_documents"
    )

    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "2000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    RETRIEVER_K: int = int(os.getenv("RETRIEVER_K", "8"))

    DOCS_PATH: str = "./docs"

    def validate(self):
        if not self.API_TOKEN_HUGGINFACEHUB:
            raise ValueError(
                "API_TOKEN_HUGGINFACEHUB no está configurado en el archivo .env"
            )


settings = Settings()

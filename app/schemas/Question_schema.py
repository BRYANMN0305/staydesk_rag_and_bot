from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="La pregunta a realizar al sistema RAG",
        example="¿Cuáles son las políticas de vacaciones de la empresa?"
    )

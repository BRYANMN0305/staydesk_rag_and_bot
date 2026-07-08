from pydantic import BaseModel

from app.schemas.SourceDocument_schema import SourceDocument


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceDocument]
    processing_time_seconds: float

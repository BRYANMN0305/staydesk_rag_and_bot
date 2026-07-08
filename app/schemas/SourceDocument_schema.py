from pydantic import BaseModel


class SourceDocument(BaseModel):
    source: str
    page: int | None = None
    content_preview: str
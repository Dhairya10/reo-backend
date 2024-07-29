from pydantic import BaseModel, UUID4

class KeywordBase(BaseModel):
    word: str

class Keyword(KeywordBase):
    id: UUID4
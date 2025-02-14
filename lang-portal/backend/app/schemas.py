from pydantic import BaseModel, ConfigDict
from typing import List

# Word schemas
class WordBase(BaseModel):
    script: str
    transliteration: str | None = None
    meaning: str

class Word(WordBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedWords(BaseModel):
    total: int
    items: List[Word]
    page: int
    per_page: int

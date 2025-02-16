from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Word schemas
class WordBase(BaseModel):
    script: str
    transliteration: Optional[str] = None
    meaning: str
    language_code: str

class Word(WordBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedWords(BaseModel):
    total: int
    items: List[Word]
    page: int
    per_page: int

class LanguageBase(BaseModel):
    code: str
    name: str
    active: bool = True
    promo_text: str | None = None

class Language(LanguageBase):
    model_config = ConfigDict(from_attributes=True)

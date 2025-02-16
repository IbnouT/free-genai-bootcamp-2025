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
    correct_count: int = 0
    wrong_count: int = 0
    
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

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    words_count: int  # Computed field, not stored

    model_config = ConfigDict(from_attributes=True)

class PaginatedGroups(BaseModel):
    total: int
    items: List[Group]
    page: int
    per_page: int
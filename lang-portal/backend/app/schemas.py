from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Word schemas
class WordBase(BaseModel):
    script: str
    transliteration: Optional[str] = None
    meaning: str

class WordCreate(WordBase):
    language_code: str  # Keep language_code for creation/requests

class WordStats(BaseModel):
    correct_count: int = 0
    wrong_count: int = 0

    model_config = ConfigDict(from_attributes=True)
    
class Word(WordBase):
    id: int
    stats: WordStats
    
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
    promo_text: Optional[str] = None

class Language(LanguageBase):
    model_config = ConfigDict(from_attributes=True)

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    language_code: str  # Keep language_code for creation/requests

class Group(GroupBase):
    id: int
    words_count: int  # Computed field, not stored

    model_config = ConfigDict(from_attributes=True)

class PaginatedGroups(BaseModel):
    total: int
    items: List[Group]
    page: int
    per_page: int

class GroupInWord(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class WordDetail(WordBase):
    id: int
    groups: List[GroupInWord]
    stats: WordStats
    
    model_config = ConfigDict(from_attributes=True)

class WordInGroup(BaseModel):
    id: int
    script: str
    transliteration: Optional[str] = None
    meaning: str
    stats: WordStats
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedGroupWords(BaseModel):
    items: List[WordInGroup]
    page: int
    per_page: int

class GroupDetail(GroupBase):
    id: int
    words_count: int
    words: PaginatedGroupWords
    
    model_config = ConfigDict(from_attributes=True)
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

# Study Activity schemas
class StudyActivityBase(BaseModel):
    name: str
    url: str
    description: str
    image_url: str
    is_language_specific: bool = False

class StudyActivity(StudyActivityBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class GroupInSession(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class ActivityInSession(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

# Study Session schemas
class StudySessionBase(BaseModel):
    group_id: int
    study_activity_id: int

class StudySessionCreate(StudySessionBase):
    pass

class StudySession(BaseModel):
    id: int
    group: GroupInSession
    activity: ActivityInSession
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)

class StudySessionDetail(StudySession):
    last_review_at: str | None
    reviews_count: int
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedStudySessions(BaseModel):
    total: int
    items: List[StudySessionDetail]
    page: int
    per_page: int

# Study Activity with Sessions
class StudyActivityWithSessions(StudyActivity):
    sessions: PaginatedStudySessions
    
    model_config = ConfigDict(from_attributes=True)

# Word Review schemas
class WordReviewCreate(BaseModel):
    word_id: int
    correct: bool

class WordReview(BaseModel):
    id: int
    word_id: int
    study_session_id: int
    correct: bool
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)

# Dashboard schemas
class LastStudySessionStats(BaseModel):
    correct_count: int
    wrong_count: int
    
    model_config = ConfigDict(from_attributes=True)

class LastStudySession(BaseModel):
    activity_name: str
    date: str
    stats: LastStudySessionStats
    group: GroupInSession
    
    model_config = ConfigDict(from_attributes=True)

class StudyProgress(BaseModel):
    words_studied: int
    total_words: int
    progress_percentage: float
    
    model_config = ConfigDict(from_attributes=True)

class QuickStats(BaseModel):
    success_rate: float
    study_sessions: int
    active_groups: int
    study_streak: int
    
    model_config = ConfigDict(from_attributes=True)
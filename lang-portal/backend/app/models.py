from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Language(Base):
    __tablename__ = "languages"
    
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    promo_text = Column(String)
    
    # Relationship to words
    words = relationship("Word", back_populates="language")

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True)
    script = Column(String, nullable=False)
    transliteration = Column(String)
    meaning = Column(String, nullable=False)
    language_code = Column(String, ForeignKey("languages.code"), nullable=False)
    
    # Relationship to language
    language = relationship("Language", back_populates="words")
    
    groups = relationship("Group", secondary="word_groups", back_populates="words")
    review_items = relationship("WordReviewItem", back_populates="word")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    words_count = Column(Integer, default=0)
    
    words = relationship("Word", secondary="word_groups", back_populates="groups")

class WordGroup(Base):
    __tablename__ = "word_groups"
    word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)

class StudyActivity(Base):
    __tablename__ = "study_activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"))
    created_at = Column(DateTime, server_default=func.now())

class WordReviewItem(Base):
    __tablename__ = "word_review_items"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"))
    correct = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())
    
    word = relationship("Word", back_populates="review_items") 
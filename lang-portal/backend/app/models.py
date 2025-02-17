from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, and_, UniqueConstraint, ForeignKeyConstraint, CheckConstraint, event
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from app.database import Base

class Language(Base):
    __tablename__ = "languages"
    
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    promo_text = Column(String)
    
    # Relationships
    words = relationship("Word", back_populates="language")
    groups = relationship("Group", back_populates="language")
    supported_activities = relationship("StudyActivity", secondary="activity_language_support", back_populates="supported_languages")

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True)
    script = Column(String, nullable=False)
    transliteration = Column(String)
    meaning = Column(String, nullable=False)
    language_code = Column(String, ForeignKey("languages.code"), nullable=False)
    
    # Relationships
    language = relationship("Language", back_populates="words")
    groups = relationship("Group", secondary="word_groups", back_populates="words")
    review_items = relationship("WordReviewItem", back_populates="word")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    language_code = Column(String, ForeignKey("languages.code"), nullable=False)
    
    # Relationships
    language = relationship("Language", back_populates="groups")
    words = relationship("Word", secondary="word_groups", back_populates="groups")
    sessions = relationship("StudySession", back_populates="group")

class WordGroup(Base):
    __tablename__ = "word_groups"
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)

class StudyActivity(Base):
    __tablename__ = "study_activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    is_language_specific = Column(Boolean, default=False)

    # Relationships
    sessions = relationship("StudySession", back_populates="activity")
    supported_languages = relationship("Language", secondary="activity_language_support", back_populates="supported_activities")

class ActivityLanguageSupport(Base):
    __tablename__ = "activity_language_support"
    activity_id = Column(Integer, ForeignKey("study_activities.id"), primary_key=True)
    language_code = Column(String, ForeignKey("languages.code"), primary_key=True)

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    activity = relationship("StudyActivity", back_populates="sessions")
    group = relationship("Group", back_populates="sessions")
    review_items = relationship("WordReviewItem", back_populates="session")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    word = relationship("Word", back_populates="review_items")
    session = relationship("StudySession", back_populates="review_items") 
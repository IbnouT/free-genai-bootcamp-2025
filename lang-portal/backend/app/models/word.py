from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    script = Column(String, nullable=False)
    transliteration = Column(String, nullable=True)  # Optional
    meaning = Column(String, nullable=False)
    
    # Relationships
    groups = relationship("Group", secondary="word_groups", back_populates="words")
    review_items = relationship("WordReviewItem", back_populates="word") 
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WordGroup(Base):
    __tablename__ = "word_groups"
    word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True) 
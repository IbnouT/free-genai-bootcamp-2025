from sqlalchemy import text
from app.database import Base

def reset_database(engine):
    """Drop all tables and recreate them. Use only in development!"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
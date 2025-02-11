from sqlalchemy import text
from app.database import engine, Base

def reset_database():
    """Drop all tables and recreate them"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def seed_database():
    """Add initial test data"""
    # This will be expanded when we add models
    pass 
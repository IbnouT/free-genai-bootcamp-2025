import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get the absolute path to the backend directory
BASE_DIR = Path(__file__).resolve().parent

Base = declarative_base()

# Production database
def get_db_url():
    db_path = BASE_DIR / "app.db"
    return f"sqlite:///{db_path}"

def get_test_db_url():
    return "sqlite:///:memory:"

def setup_db(db_url: str):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        # echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

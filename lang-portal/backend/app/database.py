import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get the absolute path to the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent

def get_db_url():
    db_path = os.path.join(BASE_DIR, "sql_app.db")
    return f"sqlite:///{db_path}"

def get_test_db_url():
    return "sqlite:///:memory:"

# Make engine configurable
engine = None
SessionLocal = None

def setup_db(db_url: str):
    global engine, SessionLocal
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

# Use the new import location
Base = declarative_base()

# Dependency
def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call setup_db first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
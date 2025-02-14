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

# Use production database by default
SQLALCHEMY_DATABASE_URL = get_db_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the new import location
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
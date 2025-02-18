import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get the absolute path to the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent

Base = declarative_base()

# Production database
def get_db_url():
    # Special case for running tests on dev
    if os.getenv("RUNNING_TEST_ON_DEV") == "true":
        return "sqlite:///:memory:"
    # Normal case
    db_path = BASE_DIR / "app" / "app.db"
    return f"sqlite:///{db_path}"

def get_test_db_url():
    return "sqlite:///:memory:"

def setup_db(db_url: str):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        # echo=True
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, session_factory

# Initialize the database engine and SessionLocal for direct imports
engine, SessionLocal = setup_db(get_db_url())

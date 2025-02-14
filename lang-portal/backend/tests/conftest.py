import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_test_db_url

@pytest.fixture(scope="session")
def engine():
    # Use test database URL from database.py
    engine = create_engine(get_test_db_url())
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Cleanup after each test
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine) 
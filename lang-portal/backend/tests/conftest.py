import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_test_db_url, get_db, setup_db, get_db_url
from app.main import app
from sqlalchemy import create_engine

@pytest.fixture(scope="session", autouse=True)
def test_db():
    # Override with test DB before any tests run
    engine = setup_db(get_test_db_url())
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    # Create test database
    engine = create_engine(get_test_db_url())
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        # Always rollback and close, even if test passed
        session.rollback()
        session.close()
        # Drop all tables after each test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session  # Same session for all calls
        finally:
            db_session.close() 
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    print("Cleaning up test client...")
    app.dependency_overrides.clear()
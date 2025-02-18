import pytest
import os

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_test_db_url, setup_db
from app.main import app, get_db

@pytest.fixture(scope="function")
def db_session():
    engine,  _ = setup_db(get_test_db_url())
    Base.metadata.create_all(bind=engine)

    # Create a single connection and bind it to the session
    connection = engine.connect()
    TestingSessionLocal = sessionmaker(bind=connection)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        connection.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    with TestClient(app) as c:
        app.dependency_overrides[get_db] = override_get_db
        yield c
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def development_env(monkeypatch):
    """Set up development environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("TESTING", "false")
    monkeypatch.setenv("RUNNING_TEST_ON_DEV", "true")
    

@pytest.fixture(scope="function")
def production_env(monkeypatch):
    """Set up production environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("TESTING", "false")

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up global test environment variables."""
    os.environ["TESTING"] = "true"
    os.environ["RUNNING_TEST_ON_DEV"] = "false"
    yield
    # Clean up after all tests
    os.environ.pop("TESTING", None)
    os.environ.pop("RUNNING_TEST_ON_DEV", None)
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import setup_db, Base, get_db_url
from app.models import Language
from app.seed import seed_all
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Load environment variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Import routers here to avoid circular imports
    from app.routers import admin, groups, languages, words, activities, sessions, dashboard
    app.include_router(admin.router)
    app.include_router(groups.router)
    app.include_router(languages.router)
    app.include_router(words.router)
    app.include_router(activities.router)
    app.include_router(sessions.router)
    app.include_router(dashboard.router)

    if os.getenv("TESTING") == "true":
        yield  # Skip lifespan for tests
        return
    
    engine, SessionLocal = setup_db(get_db_url())
    # print("Using DB URL:", engine.url)

    app.state.engine = engine
    app.state.SessionLocal = SessionLocal
    Base.metadata.create_all(bind=engine)

    if settings.ENVIRONMENT == "development":
        with Session(engine) as db:
            if not db.query(Language).first():
                print("No data found. Seeding database with test data...")
                seed_all(db, include_test_data=True)
                print("Database seeding completed!")
    yield
    engine.dispose()

def get_db():
    session_factory = app.state.SessionLocal
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="Language Learning Portal",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
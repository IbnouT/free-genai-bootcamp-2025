from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import setup_db, engine, Base, get_db_url
from app.models import Word, Group, WordGroup, Language
from app.routers import words, languages, admin
from app.seed import seed_all
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup production database on app startup
engine = setup_db(get_db_url())

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    # Auto-seed in development environment
    if os.getenv("ENVIRONMENT") == "development":
        with Session(engine) as db:
            if not db.query(Language).first():  # Only seed if empty
                seed_all(db)
    
    yield

app = FastAPI(
    title="Language Learning Portal",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(words.router)
app.include_router(languages.router)
app.include_router(admin.router) 
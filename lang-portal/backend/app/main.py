from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import setup_db, engine, Base, get_db_url
from app.models import Word, Group, WordGroup
from app.routers import words

# Setup production database on app startup
setup_db(get_db_url())

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app = FastAPI(
    title="Language Learning Portal",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(words.router) 
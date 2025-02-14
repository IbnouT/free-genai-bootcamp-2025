from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI(title="Language Learning Portal")

# Create tables at startup
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
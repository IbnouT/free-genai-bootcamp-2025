from fastapi import FastAPI

app = FastAPI(title="Language Learning Portal")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
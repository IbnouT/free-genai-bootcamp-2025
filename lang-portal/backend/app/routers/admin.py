from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import admin_only
from app.seed import seed_all

router = APIRouter()

@router.post("/admin/seed", dependencies=[Depends(admin_only)])
def seed_database(db: Session = Depends(get_db)):
    """Protected endpoint for manual seeding"""
    data = seed_all(db)
    return {"message": "Database seeded successfully"} 
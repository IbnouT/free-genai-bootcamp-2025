from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.main import get_db
from app.models import Language
from app.schemas import Language as LanguageSchema

router = APIRouter()

@router.get("/languages", response_model=List[LanguageSchema])
def get_languages(
    active: bool | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Language)
    if active is not None:
        query = query.filter(Language.active == active)
    return query.all() 
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Word
from app.schemas import PaginatedWords

router = APIRouter()

@router.get("/words", response_model=PaginatedWords)
def get_words(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc"
):
    query = db.query(Word)

    # Apply sorting
    if sort_by:
        column = getattr(Word, sort_by)
        if order == "desc":
            column = column.desc()
        query = query.order_by(column)

    # Get total count
    total = query.count()
    
    # Apply pagination
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "total": total,
        "items": items,
        "page": page,
        "per_page": per_page
    } 
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.main import get_db
from app.models import Word, WordReviewItem
from app.schemas import PaginatedWords
from sqlalchemy import func, case, text

router = APIRouter()

@router.get("/words", response_model=PaginatedWords)
def get_words(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
    language_code: str = Query(..., description="ISO 639-1 code of the language"),
):
    query = db.query(Word, 
        func.count(case((WordReviewItem.correct == True, 1))).label("correct_count"),
        func.count(case((WordReviewItem.correct == False, 1))).label("wrong_count")
    )

    # Filter by language (required)
    query = query.filter(Word.language_code == language_code)
    
    # Add correct/wrong counts
    query = query.outerjoin(WordReviewItem).group_by(Word.id)

    # Apply sorting
    if sort_by:
        if sort_by in ["correct_count", "wrong_count"]:
            column = text(sort_by)
        else:
            column = getattr(Word, sort_by)
        if order == "desc":
            column = column.desc()
        query = query.order_by(column)

    # Get total count
    total = query.count()
    
    # Apply pagination
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # Convert results to Word objects with counts
    items = []
    for word, correct, wrong in results:
        word.correct_count = correct
        word.wrong_count = wrong
        items.append(word)
    
    return {
        "total": total,
        "items": items,
        "page": page,
        "per_page": per_page
    } 
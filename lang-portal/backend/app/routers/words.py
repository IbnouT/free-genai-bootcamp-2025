from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.main import get_db
from app.models import Word, WordReviewItem
from app.schemas import PaginatedWords, WordDetail
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
    
    # Convert results to Word objects with stats
    items = []
    for word, correct, wrong in results:
        word_dict = {
            "id": word.id,
            "script": word.script,
            "transliteration": word.transliteration,
            "meaning": word.meaning,
            "stats": {
                "correct_count": correct,
                "wrong_count": wrong
            }
        }
        items.append(word_dict)
    
    return {
        "total": total,
        "items": items,
        "page": page,
        "per_page": per_page
    }

@router.get("/words/{word_id}", response_model=WordDetail)
def get_word(
    word_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves detailed information about a specific word, including its groups and review statistics.
    """
    # Query word with stats and groups
    result = (
        db.query(
            Word,
            func.count(case((WordReviewItem.correct == True, 1))).label("correct_count"),
            func.count(case((WordReviewItem.correct == False, 1))).label("wrong_count")
        )
        .outerjoin(WordReviewItem)
        .options(joinedload(Word.groups))  # Eager load groups
        .filter(Word.id == word_id)
        .group_by(Word.id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"Word with id {word_id} not found")

    word, correct_count, wrong_count = result
    # Format response according to spec
    return {
        "id": word.id,
        "script": word.script,
        "transliteration": word.transliteration,
        "meaning": word.meaning,
        "stats": {
            "correct_count": correct_count,
            "wrong_count": wrong_count
        },
        "groups": [{"id": g.id, "name": g.name} for g in word.groups]
    } 
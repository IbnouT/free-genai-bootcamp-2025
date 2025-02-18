from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.main import get_db
from app.models import Group, Word, WordGroup, WordReviewItem
from sqlalchemy import func, and_, case, text, desc
from app.schemas import PaginatedGroups, GroupDetail

router = APIRouter()

@router.get("/groups", response_model=PaginatedGroups)
def get_groups(
    db: Session = Depends(get_db),
    language_code: str = Query(..., description="ISO 639-1 code of the language"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
):
    """
    Returns a paginated list of groups for the specified language, including their word counts.
    """
    # Base query for groups filtered by language
    base_query = db.query(Group).filter(Group.language_code == language_code)
    
    # Get total count of groups for this language
    total = base_query.count()

    # Build query for groups with word counts
    query = (
        db.query(
            Group, 
            func.count(Word.id).label("words_count")
        )
        .select_from(Group)
        .filter(Group.language_code == language_code)
        .outerjoin(WordGroup, WordGroup.group_id == Group.id)
        .outerjoin(Word, and_(Word.id == WordGroup.word_id, Word.language_code == language_code))
        .group_by(Group.id)
    )

    # Sorting logic
    if sort_by:
        if sort_by == "words_count":
            column = func.count(Word.id)
        else:
            column = getattr(Group, sort_by)
        if order == "desc":
            column = column.desc()
        query = query.order_by(column)

    # Pagination
    results = query.offset((page - 1) * per_page).limit(per_page).all()

    # Build items list
    items = []
    for group, words_count in results:
        group.words_count = words_count
        items.append(group)

    return {
        "total": total,
        "items": items,
        "page": page,
        "per_page": per_page
    }

@router.get("/groups/{group_id}", response_model=GroupDetail)
def get_group(
    group_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    sort_by: Optional[str] = Query(None, description="Field to sort words by"),
    order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db)
):
    """
    Retrieves detailed information about a specific group and its words.
    The language context is derived from the group itself.
    """
    # First check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group with id {group_id} not found")

    # Get words count for this group's language
    words_count = (
        db.query(func.count(Word.id))
        .join(WordGroup, WordGroup.word_id == Word.id)
        .filter(
            WordGroup.group_id == group_id,
            Word.language_code == group.language_code
        )
        .scalar()
    )

    # Query words with their stats
    query = (
        db.query(
            Word,
            func.count(case((WordReviewItem.correct == True, 1))).label("correct_count"),
            func.count(case((WordReviewItem.correct == False, 1))).label("wrong_count")
        )
        .join(WordGroup, WordGroup.word_id == Word.id)
        .filter(
            WordGroup.group_id == group_id,
            Word.language_code == group.language_code
        )
        .outerjoin(WordReviewItem, WordReviewItem.word_id == Word.id)
        .group_by(Word.id)
    )

    # Apply sorting
    if sort_by:
        if sort_by in ["correct_count", "wrong_count"]:
            column = text(sort_by)
            if order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)
        else:
            column = getattr(Word, sort_by)
            if order == "desc":
                column = column.desc()
            query = query.order_by(column)

    # Apply pagination
    results = query.offset((page - 1) * per_page).limit(per_page).all()

    # Build items list
    items = []
    for word, correct_count, wrong_count in results:
        word_dict = {
            "id": word.id,
            "script": word.script,
            "transliteration": word.transliteration,
            "meaning": word.meaning,
            "stats": {
                "correct_count": correct_count,
                "wrong_count": wrong_count
            }
        }
        items.append(word_dict)

    return {
        "id": group.id,
        "name": group.name,
        "words_count": words_count,
        "words": {
            "items": items,
            "page": page,
            "per_page": per_page
        }
    }
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.main import get_db
from app.models import Group, Word, WordGroup, WordReviewItem
from sqlalchemy import func, and_, case, text
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
    Returns a paginated list of all groups (unfiltered), but each group includes 
    the count of words that match the given language_code.
    """

    # 1) Count how many total groups exist (unfiltered).
    total = db.query(Group).count()

    # 2) Build a query that includes count of words *filtered by language_code*.
    #    Use an outer join so groups with zero matching words still appear (count=0).
    query = (
        db.query(
            Group, 
            func.count(Word.id).label("words_count")
        )
        .select_from(Group)
        # Join Group -> WordGroup
        .outerjoin(WordGroup, WordGroup.group_id == Group.id)
        # Join WordGroup -> Word with a condition on language_code
        .outerjoin(
            Word, 
            and_(
                Word.id == WordGroup.word_id, 
                Word.language_code == language_code
            )
        )
        .group_by(Group.id)
    )

    # Sorting logic (e.g., by words_count or a Group column)
    if sort_by:
        if sort_by == "words_count":
            column = func.count(Word.id)
        else:
            # e.g. "name" or "id" on Group
            column = getattr(Group, sort_by)
        if order == "desc":
            column = column.desc()
        query = query.order_by(column)

    # Pagination
    results = query.offset((page - 1) * per_page).limit(per_page).all()

    # Build items list
    items = []
    for group, words_count in results:
        # Attach the words_count attribute for convenience
        group.words_count = words_count
        items.append(group)

    return {
        "total": total,       # total # of groups (unfiltered)
        "items": items,       # each group + filtered word count
        "page": page,
        "per_page": per_page
    }

@router.get("/groups/{group_id}", response_model=GroupDetail)
def get_group(
    group_id: int,
    language_code: str = Query(..., description="ISO 639-1 code of the language"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    sort_by: Optional[str] = Query(None, description="Field to sort words by"),
    order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db)
):
    """
    Retrieves detailed information about a specific group and its words in the specified language.
    """
    # First check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group with id {group_id} not found")

    # Get words count for this language
    words_count = (
        db.query(func.count(Word.id))
        .join(WordGroup, WordGroup.word_id == Word.id)
        .filter(
            WordGroup.group_id == group_id,
            Word.language_code == language_code
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
            Word.language_code == language_code
        )
        .outerjoin(WordReviewItem, WordReviewItem.word_id == Word.id)
        .group_by(Word.id)
    )

    # Apply sorting
    if sort_by:
        if sort_by in ["correct_count", "wrong_count"]:
            column = text(sort_by)
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
            "language_code": word.language_code,
            "correct_count": correct_count,
            "wrong_count": wrong_count
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
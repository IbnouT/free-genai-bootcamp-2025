from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.main import get_db
from app.models import Group, Word, WordGroup
from sqlalchemy import func, and_
from app.schemas import PaginatedGroups
from sqlalchemy import func, case, text

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
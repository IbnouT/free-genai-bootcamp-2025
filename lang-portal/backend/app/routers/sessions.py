from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from app.main import get_db
from app.models import StudySession as StudySessionModel, WordReviewItem as WordReviewModel, Group, Word
from app.schemas import (
    StudySessionCreate, StudySession, StudySessionDetail,
    PaginatedStudySessions, WordReviewCreate, WordReview
)

router = APIRouter()

@router.post("/study-sessions", response_model=StudySession)
def create_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new study session."""
    # Verify that the group exists
    group = db.query(Group).filter(Group.id == session.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group with id {session.group_id} not found")
    
    # Create the session
    db_session = StudySessionModel(
        group_id=session.group_id,
        study_activity_id=session.study_activity_id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    # Convert to response format with ISO formatted datetime
    return {
        "id": db_session.id,
        "group": db_session.group,
        "activity": db_session.activity,
        "created_at": db_session.created_at.isoformat()
    }

@router.post("/study-sessions/{session_id}/reviews", response_model=WordReview)
def create_word_review(
    session_id: int,
    review: WordReviewCreate,
    db: Session = Depends(get_db)
):
    """Record a word review result for the given study session."""
    # Verify that the session exists
    session = db.query(StudySessionModel).filter(StudySessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Study session with id {session_id} not found")
    
    # Verify that the word exists and belongs to the session's group
    word = db.query(Word).join(
        Word.groups
    ).filter(
        Word.id == review.word_id,
        Group.id == session.group_id
    ).first()
    if not word:
        raise HTTPException(
            status_code=404,
            detail=f"Word with id {review.word_id} not found or does not belong to the session's group"
        )
    
    # Create the review
    db_review = WordReviewModel(
        word_id=review.word_id,
        study_session_id=session_id,
        correct=review.correct
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Get all needed data while session is active
    review_data = {
        "id": db_review.id,
        "word_id": db_review.word_id,
        "study_session_id": db_review.study_session_id,
        "correct": db_review.correct,
        "created_at": db_review.created_at.isoformat()
    }
    
    return review_data

@router.get("/study-sessions", response_model=PaginatedStudySessions)
def get_study_sessions(
    language_code: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(created_at|last_review_at|reviews_count)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """Get a paginated list of study sessions for the specified language."""
    # Build base query
    sessions_query = db.query(
        StudySessionModel,
        func.max(WordReviewModel.created_at).label("last_review_at"),
        func.count(WordReviewModel.id).label("reviews_count")
    ).join(
        StudySessionModel.group
    ).outerjoin(
        WordReviewModel,
        WordReviewModel.study_session_id == StudySessionModel.id
    ).filter(
        StudySessionModel.group.has(language_code=language_code)
    ).group_by(
        StudySessionModel.id
    )
    
    # Apply sorting
    if sort_by == "created_at":
        sort_column = StudySessionModel.created_at
    elif sort_by == "last_review_at":
        sort_column = func.max(WordReviewModel.created_at)
    else:  # reviews_count
        sort_column = func.count(WordReviewModel.id)
    
    if order == "desc":
        sessions_query = sessions_query.order_by(desc(sort_column))
    else:
        sessions_query = sessions_query.order_by(sort_column)
    
    # Get total count
    total = sessions_query.count()
    
    # Apply pagination
    sessions = sessions_query.offset((page - 1) * per_page).limit(per_page).all()
    
    # Convert to response format
    session_items = []
    for session, last_review_at, reviews_count in sessions:
        session_detail = StudySessionDetail(
            id=session.id,
            group=session.group,
            activity=session.activity,
            created_at=session.created_at.isoformat(),
            last_review_at=last_review_at.isoformat() if last_review_at else None,
            reviews_count=reviews_count
        )
        session_items.append(session_detail)
    
    return PaginatedStudySessions(
        total=total,
        items=session_items,
        page=page,
        per_page=per_page
    )

@router.get("/study-sessions/{session_id}", response_model=StudySessionDetail)
def get_study_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific study session."""
    # Get session with review statistics
    session_data = db.query(
        StudySessionModel,
        func.max(WordReviewModel.created_at).label("last_review_at"),
        func.count(WordReviewModel.id).label("reviews_count")
    ).outerjoin(
        WordReviewModel,
        WordReviewModel.study_session_id == StudySessionModel.id
    ).filter(
        StudySessionModel.id == session_id
    ).group_by(
        StudySessionModel.id
    ).first()
    
    if not session_data:
        raise HTTPException(status_code=404, detail=f"Study session with id {session_id} not found")
    
    session, last_review_at, reviews_count = session_data
    
    return StudySessionDetail(
        id=session.id,
        group=session.group,
        activity=session.activity,
        created_at=session.created_at.isoformat(),
        last_review_at=last_review_at.isoformat() if last_review_at else None,
        reviews_count=reviews_count
    ) 
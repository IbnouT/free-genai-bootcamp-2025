from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List
from app.main import get_db
from app.models import StudyActivity, ActivityLanguageSupport, StudySession, WordReviewItem
from app.schemas import StudyActivity as StudyActivitySchema
from app.schemas import StudyActivityWithSessions, PaginatedStudySessions, StudySessionDetail

router = APIRouter()

@router.get("/study-activities", response_model=List[StudyActivitySchema])
def get_study_activities(
    language_code: str,
    db: Session = Depends(get_db)
):
    """
    Get all study activities available for a specific language.
    This includes both universal activities and language-specific ones that support the given language.
    """
    # Get all universal activities (is_language_specific = False)
    # and language-specific activities that support the given language
    activities = db.query(StudyActivity).filter(
        (StudyActivity.is_language_specific == False) |  # Universal activities
        and_(
            StudyActivity.is_language_specific == True,  # Language-specific activities
            StudyActivity.id.in_(
                db.query(ActivityLanguageSupport.activity_id)
                .filter(ActivityLanguageSupport.language_code == language_code)
            )
        )
    ).all()
    
    return activities

@router.get("/study-activities/{activity_id}", response_model=StudyActivityWithSessions)
def get_study_activity(
    activity_id: int,
    language_code: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(created_at|last_review_at|reviews_count)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific study activity, including its sessions history
    for the specified language.
    """
    # Get the activity
    activity = db.query(StudyActivity).filter(StudyActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail=f"Study activity with id {activity_id} not found")
    
    # Get sessions with their review statistics
    sessions_query = db.query(
        StudySession,
        func.max(WordReviewItem.created_at).label("last_review_at"),
        func.count(WordReviewItem.id).label("reviews_count")
    ).join(
        StudySession.group
    ).outerjoin(
        WordReviewItem,
        WordReviewItem.study_session_id == StudySession.id
    ).filter(
        StudySession.study_activity_id == activity_id,
        StudySession.group.has(language_code=language_code)
    ).group_by(
        StudySession.id
    )
    
    # Apply sorting
    if sort_by == "created_at":
        sort_column = StudySession.created_at
    elif sort_by == "last_review_at":
        sort_column = func.max(WordReviewItem.created_at)
    else:  # reviews_count
        sort_column = func.count(WordReviewItem.id)
    
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
    
    # Create paginated sessions response
    paginated_sessions = PaginatedStudySessions(
        total=total,
        items=session_items,
        page=page,
        per_page=per_page
    )
    
    # Add sessions to activity response
    activity_response = StudyActivityWithSessions(
        id=activity.id,
        name=activity.name,
        url=activity.url,
        description=activity.description,
        image_url=activity.image_url,
        is_language_specific=activity.is_language_specific,
        sessions=paginated_sessions
    )
    
    return activity_response 
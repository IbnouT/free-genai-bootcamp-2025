from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, case
from datetime import datetime, timedelta
from typing import Optional
from app.main import get_db
from app.models import StudySession, WordReviewItem, Word, Group
from app.schemas import LastStudySession, LastStudySessionStats, StudyProgress, QuickStats

router = APIRouter()

@router.get("/dashboard/last-session", response_model=Optional[LastStudySession])
def get_last_study_session(
    language_code: str,
    db: Session = Depends(get_db)
):
    """Get information about the user's last study session for a specific language."""
    # Get the last session with its review statistics
    last_session = db.query(
        StudySession,
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == True).label("correct_count"),
        func.count(WordReviewItem.id).filter(WordReviewItem.correct == False).label("wrong_count")
    ).join(
        StudySession.group
    ).outerjoin(
        WordReviewItem,
        WordReviewItem.study_session_id == StudySession.id
    ).filter(
        StudySession.group.has(language_code=language_code)
    ).group_by(
        StudySession.id
    ).order_by(
        desc(StudySession.created_at)
    ).first()
    
    if not last_session:
        return None
    
    session, correct_count, wrong_count = last_session
    
    return LastStudySession(
        activity_name=session.activity.name,
        date=session.created_at.isoformat(),
        stats=LastStudySessionStats(
            correct_count=correct_count,
            wrong_count=wrong_count
        ),
        group=session.group
    )

@router.get("/dashboard/progress", response_model=StudyProgress)
def get_study_progress(
    language_code: str,
    db: Session = Depends(get_db)
):
    """Get the user's study progress over the last month."""
    # Calculate last month's date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)  # Last month
    
    # Get total words count from groups used in study sessions
    total_words = db.query(
        func.count(Word.id.distinct())
    ).join(
        Word.groups
    ).join(
        StudySession,
        StudySession.group_id == Group.id
    ).filter(
        Group.language_code == language_code,
        StudySession.created_at >= start_date
    ).scalar()
    
    # Get words studied count
    words_studied = db.query(
        func.count(Word.id.distinct())
    ).join(
        WordReviewItem,
        WordReviewItem.word_id == Word.id
    ).join(
        StudySession,
        StudySession.id == WordReviewItem.study_session_id
    ).join(
        Group,
        Group.id == StudySession.group_id
    ).filter(
        Group.language_code == language_code,
        WordReviewItem.created_at >= start_date
    ).scalar()
    
    # Calculate progress percentage
    total_words = total_words or 0
    words_studied = words_studied or 0
    progress_percentage = (words_studied / total_words * 100) if total_words > 0 else 0.0
    
    return StudyProgress(
        total_words=total_words,
        words_studied=words_studied,
        progress_percentage=round(progress_percentage, 1)  # Round to 1 decimal place
    )

@router.get("/dashboard/quick-stats", response_model=QuickStats)
def get_quick_stats(
    language_code: str,
    db: Session = Depends(get_db)
):
    """Get aggregated statistics about the user's study performance."""
    # Get success rate and session count
    stats = db.query(
        (func.sum(case((WordReviewItem.correct == True, 1), else_=0)) * 100.0 / 
         func.count(WordReviewItem.id)).label("success_rate"),
        func.count(func.distinct(StudySession.id)).label("study_sessions")
    ).join(
        StudySession,
        StudySession.id == WordReviewItem.study_session_id
    ).join(
        Group,
        Group.id == StudySession.group_id
    ).filter(
        Group.language_code == language_code
    ).first()
    
    # Get active groups count
    active_groups = db.query(
        func.count(func.distinct(Group.id))
    ).join(
        StudySession,
        StudySession.group_id == Group.id
    ).filter(
        Group.language_code == language_code
    ).scalar()
    
    # Calculate study streak
    study_dates = db.query(
        func.date(StudySession.created_at).label("date")
    ).join(
        Group,
        Group.id == StudySession.group_id
    ).filter(
        Group.language_code == language_code
    ).order_by(
        desc("date")
    ).distinct().all()
    
    # Convert to list of dates and ensure they are datetime.date objects
    study_dates = [datetime.strptime(str(date[0]), "%Y-%m-%d").date() for date in study_dates]
    
    # Calculate streak
    streak = 0
    if study_dates:
        current_date = datetime.utcnow().date()
        for i, date in enumerate(study_dates):
            if i == 0:
                # First date must be today or yesterday
                days_diff = (current_date - date).days
                if days_diff > 1:
                    break
            if i > 0:
                # Check gap between consecutive dates
                days_diff = (study_dates[i-1] - date).days
                if days_diff > 1:
                    break
            streak += 1
    
    return QuickStats(
        success_rate=round(stats.success_rate or 0.0, 1),
        study_sessions=stats.study_sessions or 0,
        active_groups=active_groups or 0,
        study_streak=streak
    ) 
from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session
from app.models import StudyActivity, Group, Word, StudySession, WordReviewItem, Language

def test_get_last_study_session_no_sessions(client, db_session: Session):
    """Test getting last study session when there are no sessions."""
    response = client.get("/dashboard/last-session?language_code=es")
    assert response.status_code == 200
    assert response.json() is None

def test_get_last_study_session(client, db_session: Session):
    """Test getting last study session with review statistics."""
    # Create test data
    activity = StudyActivity(
        name="Test Activity",
        url="/test-url",
        description="Test Description",
        image_url="/test.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    group = Group(name="Test Group", language_code="es")
    db_session.add(group)
    db_session.commit()
    
    word = Word(script="test", meaning="prueba", language_code="es")
    db_session.add(word)
    db_session.commit()
    
    word.groups.append(group)
    db_session.commit()
    
    session = StudySession(group_id=group.id, study_activity_id=activity.id)
    db_session.add(session)
    db_session.commit()
    
    # Add some reviews
    reviews = [
        WordReviewItem(word_id=word.id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=word.id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=word.id, study_session_id=session.id, correct=False)
    ]
    db_session.add_all(reviews)
    db_session.commit()
    
    response = client.get("/dashboard/last-session?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["activity_name"] == "Test Activity"
    assert "date" in data
    assert data["stats"]["correct_count"] == 2
    assert data["stats"]["wrong_count"] == 1
    assert data["group"]["name"] == "Test Group"
    assert data["group"]["id"] == group.id

def test_get_study_progress_no_data(client, db_session: Session):
    """Test getting study progress when there is no data."""
    response = client.get("/dashboard/progress?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_words"] == 0
    assert data["words_studied"] == 0
    assert data["progress_percentage"] == 0.0

def test_get_study_progress(client, db_session: Session):
    """Test getting study progress with actual data."""
    # Create test data
    activity = StudyActivity(
        name="Test Activity",
        url="/test-url",
        description="Test Description",
        image_url="/test.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    group = Group(name="Test Group", language_code="es")
    db_session.add(group)
    db_session.commit()
    
    # Add some words and link to group
    words = [
        Word(script=f"test{i}", meaning=f"prueba{i}", language_code="es")
        for i in range(5)
    ]
    for word in words:
        db_session.add(word)
    db_session.commit()
    
    for word in words:
        word.groups.append(group)
    db_session.commit()
    
    # Create a session within the last month
    session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=datetime.utcnow() - timedelta(days=15)
    )
    db_session.add(session)
    db_session.commit()
    
    # Add reviews for first 3 words
    reviews = []
    for word in words[:3]:
        review = WordReviewItem(
            word_id=word.id,
            study_session_id=session.id,
            correct=True,
            created_at=datetime.utcnow() - timedelta(days=15)
        )
        reviews.append(review)
    db_session.add_all(reviews)
    db_session.commit()
    
    response = client.get("/dashboard/progress?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_words"] == 5  # All words in the group
    assert data["words_studied"] == 3  # Only 3 words were reviewed
    assert data["progress_percentage"] == 60.0  # (3/5) * 100

def test_get_study_progress_old_session(client, db_session: Session):
    """Test that old sessions (>1 month) are not included."""
    # Create test data
    activity = StudyActivity(
        name="Test Activity",
        url="/test-url",
        description="Test Description",
        image_url="/test.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    group = Group(name="Test Group", language_code="es")
    db_session.add(group)
    db_session.commit()
    
    word = Word(script="test", meaning="prueba", language_code="es")
    db_session.add(word)
    db_session.commit()
    
    word.groups.append(group)
    db_session.commit()
    
    # Create an old session (more than a month ago)
    old_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=datetime.utcnow() - timedelta(days=35)
    )
    db_session.add(old_session)
    db_session.commit()
    
    # Add review for the word
    review = WordReviewItem(
        word_id=word.id,
        study_session_id=old_session.id,
        correct=True,
        created_at=datetime.utcnow() - timedelta(days=35)
    )
    db_session.add(review)
    db_session.commit()
    
    response = client.get("/dashboard/progress?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_words"] == 0  # Old session not counted
    assert data["words_studied"] == 0
    assert data["progress_percentage"] == 0.0

def test_get_quick_stats_no_data(client, db_session: Session):
    """Test getting quick stats when there is no data."""
    response = client.get("/dashboard/quick-stats?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["success_rate"] == 0.0
    assert data["study_sessions"] == 0
    assert data["active_groups"] == 0
    assert data["study_streak"] == 0

def test_get_quick_stats(client, db_session: Session):
    """Test getting quick stats with actual data."""
    # Create test data
    activity = StudyActivity(
        name="Test Activity",
        url="/test-url",
        description="Test Description",
        image_url="/test.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Create two groups
    groups = [
        Group(name=f"Test Group {i}", language_code="es")
        for i in range(2)
    ]
    for group in groups:
        db_session.add(group)
    db_session.commit()
    
    word = Word(script="test", meaning="prueba", language_code="es")
    db_session.add(word)
    db_session.commit()
    
    word.groups.append(groups[0])
    db_session.commit()
    
    # Create sessions over three consecutive days
    base_date = datetime.utcnow().date()
    for days_ago in range(3):
        session_date = base_date - timedelta(days=days_ago)
        session = StudySession(
            group_id=groups[0].id if days_ago < 2 else groups[1].id,  # Use both groups
            study_activity_id=activity.id,
            created_at=datetime.combine(session_date, datetime.min.time())
        )
        db_session.add(session)
        db_session.commit()
        
        # Add reviews with 75% success rate (3 correct, 1 wrong)
        reviews = []
        for i in range(4):
            review = WordReviewItem(
                word_id=word.id,
                study_session_id=session.id,
                correct=(i < 3),  # First 3 are correct, last one wrong
                created_at=datetime.combine(session_date, datetime.min.time())
            )
            reviews.append(review)
        db_session.add_all(reviews)
        db_session.commit()
    
    response = client.get("/dashboard/quick-stats?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["success_rate"] == 75.0  # (9 correct / 12 total) * 100
    assert data["study_sessions"] == 3  # Three sessions
    assert data["active_groups"] == 2  # Both groups used
    assert data["study_streak"] == 3  # Three consecutive days

def test_get_quick_stats_broken_streak(client, db_session: Session):
    """Test that streak breaks correctly when there's a gap in study days."""
    # Create test data
    activity = StudyActivity(
        name="Test Activity",
        url="/test-url",
        description="Test Description",
        image_url="/test.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    group = Group(name="Test Group", language_code="es")
    db_session.add(group)
    db_session.commit()
    
    word = Word(script="test", meaning="prueba", language_code="es")
    db_session.add(word)
    db_session.commit()
    
    word.groups.append(group)
    db_session.commit()
    
    # Create sessions with a gap
    base_date = datetime.utcnow().date()
    session_dates = [base_date - timedelta(days=d) for d in [0, 1, 3]]  # Note the gap at day 2
    
    for session_date in session_dates:
        session = StudySession(
            group_id=group.id,
            study_activity_id=activity.id,
            created_at=datetime.combine(session_date, datetime.min.time())
        )
        db_session.add(session)
        db_session.commit()
        
        review = WordReviewItem(
            word_id=word.id,
            study_session_id=session.id,
            correct=True,
            created_at=datetime.combine(session_date, datetime.min.time())
        )
        db_session.add(review)
        db_session.commit()
    
    response = client.get("/dashboard/quick-stats?language_code=es")
    assert response.status_code == 200
    data = response.json()
    
    assert data["study_streak"] == 2  # Only counts the last two consecutive days 

def test_study_progress_broken_streak(client, db_session):
    """Test study progress with a broken streak (gap > 1 day)."""
    # Create test data
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()
    
    activity = StudyActivity(
        name="Flashcards",
        url="/study/flashcards",
        description="Practice with flashcards",
        image_url="/images/flashcards.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Create sessions with a gap to break the streak
    # Today's session
    today_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=datetime.utcnow()
    )
    db_session.add(today_session)
    
    # Session from 3 days ago (creates a gap)
    old_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=datetime.utcnow() - timedelta(days=3)
    )
    db_session.add(old_session)
    db_session.commit()
    
    # Add some reviews to make the sessions valid
    review = WordReviewItem(
        word_id=1,  # Dummy word ID
        study_session_id=today_session.id,
        correct=True
    )
    db_session.add(review)
    db_session.commit()
    
    # Test the quick-stats endpoint
    response = client.get("/dashboard/quick-stats?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    # The streak should be 1 (only today) because of the gap
    assert data["study_streak"] == 1 

def test_study_streak_consecutive_gap(client, db_session):
    """Test streak calculation when there's a gap between consecutive study dates."""
    # Create test data
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()
    
    activity = StudyActivity(
        name="Flashcards",
        url="/study/flashcards",
        description="Practice with flashcards",
        image_url="/images/flashcards.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Create sessions with specific dates to test gap detection
    base_date = datetime.utcnow().date()
    
    # Yesterday's session (to pass the first condition)
    yesterday = base_date - timedelta(days=1)
    yesterday_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=yesterday
    )
    db_session.add(yesterday_session)
    
    # Session from 4 days ago
    four_days_ago = base_date - timedelta(days=4)
    four_days_ago_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=four_days_ago
    )
    db_session.add(four_days_ago_session)
    
    # Session from 5 days ago
    five_days_ago = base_date - timedelta(days=5)
    five_days_ago_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=five_days_ago
    )
    db_session.add(five_days_ago_session)
    db_session.commit()
    
    # Add reviews for each session
    for session in [yesterday_session, four_days_ago_session, five_days_ago_session]:
        review = WordReviewItem(
            word_id=1,  # Dummy word ID
            study_session_id=session.id,
            correct=True,
            created_at=session.created_at
        )
        db_session.add(review)
    db_session.commit()
    
    # Test the quick-stats endpoint
    response = client.get("/dashboard/quick-stats?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    # The streak should be 1 (only yesterday)
    # When sorted in descending order:
    # 1. yesterday (passes first condition)
    # 2. comparing yesterday with 4 days ago (gap > 1, breaks at line 157)
    assert data["study_streak"] == 1

def test_study_streak_old_first_date(client, db_session):
    """Test streak calculation when the most recent study date is more than 1 day old."""
    # Create test data
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()
    
    activity = StudyActivity(
        name="Flashcards",
        url="/study/flashcards",
        description="Practice with flashcards",
        image_url="/images/flashcards.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Create sessions with specific dates to test first date check
    base_date = datetime.utcnow().date()
    
    # Most recent session is 3 days ago
    three_days_ago = base_date - timedelta(days=3)
    three_days_ago_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=three_days_ago
    )
    db_session.add(three_days_ago_session)
    
    # Session from 4 days ago
    four_days_ago = base_date - timedelta(days=4)
    four_days_ago_session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=four_days_ago
    )
    db_session.add(four_days_ago_session)
    db_session.commit()
    
    # Add reviews for each session
    for session in [three_days_ago_session, four_days_ago_session]:
        review = WordReviewItem(
            word_id=1,  # Dummy word ID
            study_session_id=session.id,
            correct=True,
            created_at=session.created_at
        )
        db_session.add(review)
    db_session.commit()
    
    # Test the quick-stats endpoint
    response = client.get("/dashboard/quick-stats?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    # The streak should be 0 because the most recent session is more than 1 day old
    assert data["study_streak"] == 0 
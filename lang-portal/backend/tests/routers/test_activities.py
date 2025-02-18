from app.models import StudyActivity, ActivityLanguageSupport, StudySession, WordReviewItem, Group, Language
from datetime import datetime, timedelta

def test_get_study_activities(client, db_session):
    # Create test activities
    activities = [
        StudyActivity(
            name="Flashcards",
            url="/study/flashcards",
            description="Practice with flashcards",
            image_url="/images/flashcards.png",
            is_language_specific=False  # Universal activity
        ),
        StudyActivity(
            name="Typing Practice",
            url="/study/typing",
            description="Practice typing",
            image_url="/images/typing.png",
            is_language_specific=True  # Language-specific activity
        ),
        StudyActivity(
            name="Writing Practice",
            url="/study/writing",
            description="Practice writing",
            image_url="/images/writing.png",
            is_language_specific=True  # Language-specific activity
        )
    ]
    db_session.add_all(activities)
    db_session.commit()
    
    # Create language support for typing practice
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    support = ActivityLanguageSupport(
        activity_id=activities[1].id,  # Typing Practice
        language_code="ja"
    )
    db_session.add(support)
    db_session.commit()
    
    # Test getting activities for Japanese
    response = client.get("/study-activities?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    # Should get Flashcards (universal) and Typing Practice (supported)
    assert len(data) == 2
    activity_names = {item["name"] for item in data}
    assert "Flashcards" in activity_names
    assert "Typing Practice" in activity_names
    assert "Writing Practice" not in activity_names  # Not supported for Japanese

def test_get_study_activity_details(client, db_session):
    # Create test activity
    activity = StudyActivity(
        name="Flashcards",
        url="/study/flashcards",
        description="Practice with flashcards",
        image_url="/images/flashcards.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Create language and group
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()
    
    # Create sessions with reviews
    sessions = []
    for i in range(3):  # Create 3 sessions
        session = StudySession(
            group_id=group.id,
            study_activity_id=activity.id,
            created_at=datetime.now() - timedelta(days=i)
        )
        db_session.add(session)
        db_session.commit()
        sessions.append(session)
        
        # Add some reviews
        for _ in range(i + 1):  # Different number of reviews per session
            review = WordReviewItem(
                word_id=1,  # Dummy word ID
                study_session_id=session.id,
                correct=True,
                created_at=datetime.now() - timedelta(hours=i)
            )
            db_session.add(review)
        db_session.commit()
    
    # Test getting activity details
    response = client.get(f"/study-activities/{activity.id}?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    # Check activity details
    assert data["id"] == activity.id
    assert data["name"] == activity.name
    assert data["url"] == activity.url
    assert data["description"] == activity.description
    assert data["image_url"] == activity.image_url
    
    # Check sessions
    assert data["sessions"]["total"] == 3
    assert len(data["sessions"]["items"]) == 3
    
    # Check session details and sorting (default: created_at desc)
    items = data["sessions"]["items"]
    assert items[0]["reviews_count"] == 1  # Newest session
    assert items[1]["reviews_count"] == 2  # Middle session
    assert items[2]["reviews_count"] == 3  # Oldest session
    
    # Test sorting by reviews_count
    response = client.get(
        f"/study-activities/{activity.id}?language_code=ja&sort_by=reviews_count&order=desc"
    )
    assert response.status_code == 200
    data = response.json()
    items = data["sessions"]["items"]
    assert items[0]["reviews_count"] == 3  # Most reviews
    assert items[1]["reviews_count"] == 2
    assert items[2]["reviews_count"] == 1  # Least reviews

def test_get_nonexistent_activity(client):
    response = client.get("/study-activities/999?language_code=ja")
    assert response.status_code == 404
    assert response.json()["detail"] == "Study activity with id 999 not found"

def test_get_study_activity_details_with_sorting(client, db_session):
    """Test different sorting options for study activity sessions."""
    # Create test activity
    activity = StudyActivity(
        name="Flashcards",
        url="/study/flashcards",
        description="Practice with flashcards",
        image_url="/images/flashcards.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Create language and group
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()
    
    # Create sessions with reviews at different times
    sessions = []
    base_time = datetime.now()
    
    for i in range(3):
        session = StudySession(
            group_id=group.id,
            study_activity_id=activity.id,
            created_at=base_time - timedelta(days=i)  # Different creation times
        )
        db_session.add(session)
        db_session.commit()
        sessions.append(session)
        
        # Add reviews with different last review times
        review_time = base_time - timedelta(hours=i*2)  # Different review times
        review = WordReviewItem(
            word_id=1,  # Dummy word ID
            study_session_id=session.id,
            correct=True,
            created_at=review_time
        )
        db_session.add(review)
        db_session.commit()
    
    # Test sorting by last_review_at in descending order
    response = client.get(
        f"/study-activities/{activity.id}?language_code=ja&sort_by=last_review_at&order=desc"
    )
    assert response.status_code == 200
    data = response.json()
    items = data["sessions"]["items"]
    
    # Most recent review should be first
    assert items[0]["id"] == sessions[0].id
    assert items[1]["id"] == sessions[1].id
    assert items[2]["id"] == sessions[2].id
    
    # Test sorting by last_review_at in ascending order
    response = client.get(
        f"/study-activities/{activity.id}?language_code=ja&sort_by=last_review_at&order=asc"
    )
    assert response.status_code == 200
    data = response.json()
    items = data["sessions"]["items"]
    
    # Oldest review should be first
    assert items[0]["id"] == sessions[2].id
    assert items[1]["id"] == sessions[1].id
    assert items[2]["id"] == sessions[0].id 
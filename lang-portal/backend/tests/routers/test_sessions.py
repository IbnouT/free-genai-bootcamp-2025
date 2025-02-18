from app.models import StudyActivity, StudySession, WordReviewItem, Group, Language, Word, WordGroup
from datetime import datetime, timedelta

def test_create_study_session(client, db_session):
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
    
    # Test creating a session
    response = client.post("/study-sessions", json={
        "group_id": group.id,
        "study_activity_id": activity.id
    })
    assert response.status_code == 200
    data = response.json()
    
    # Check response
    assert data["id"] is not None
    assert data["group"]["id"] == group.id
    assert data["group"]["name"] == group.name
    assert data["activity"]["id"] == activity.id
    assert data["activity"]["name"] == activity.name
    assert "created_at" in data

def test_create_word_review(client, db_session):
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
    
    word = Word(script="食べる", meaning="to eat", language_code="ja")
    db_session.add(word)
    db_session.commit()
    word_id = word.id  # Store the ID before closing session
    
    word_group = WordGroup(word_id=word.id, group_id=group.id)
    db_session.add(word_group)
    db_session.commit()
    
    session = StudySession(group_id=group.id, study_activity_id=activity.id)
    db_session.add(session)
    db_session.commit()
    session_id = session.id  # Store the ID before closing session
    
    # Test creating a review
    response = client.post(f"/study-sessions/{session_id}/reviews", json={
        "word_id": word_id,
        "correct": True
    })
    assert response.status_code == 200
    data = response.json()
    
    # Check response
    assert data["id"] is not None
    assert data["word_id"] == word_id
    assert data["study_session_id"] == session_id
    assert data["correct"] is True
    assert "created_at" in data

def test_get_study_sessions(client, db_session):
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
    
    # Test getting sessions
    response = client.get("/study-sessions?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    # Check response
    assert data["total"] == 3
    assert len(data["items"]) == 3
    
    # Check session details and sorting (default: created_at desc)
    items = data["items"]
    assert items[0]["reviews_count"] == 1  # Newest session
    assert items[1]["reviews_count"] == 2  # Middle session
    assert items[2]["reviews_count"] == 3  # Oldest session
    
    # Test sorting by reviews_count
    response = client.get("/study-sessions?language_code=ja&sort_by=reviews_count&order=desc")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    assert items[0]["reviews_count"] == 3  # Most reviews
    assert items[1]["reviews_count"] == 2
    assert items[2]["reviews_count"] == 1  # Least reviews

def test_get_study_session(client, db_session):
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
    
    # Create session with reviews
    session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id,
        created_at=datetime.now() - timedelta(days=1)
    )
    db_session.add(session)
    db_session.commit()
    
    # Add reviews
    for i in range(3):
        review = WordReviewItem(
            word_id=1,  # Dummy word ID
            study_session_id=session.id,
            correct=True,
            created_at=datetime.now() - timedelta(hours=i)
        )
        db_session.add(review)
    db_session.commit()
    
    # Test getting session details
    response = client.get(f"/study-sessions/{session.id}")
    assert response.status_code == 200
    data = response.json()
    
    # Check response
    assert data["id"] == session.id
    assert data["group"]["id"] == group.id
    assert data["group"]["name"] == group.name
    assert data["activity"]["id"] == activity.id
    assert data["activity"]["name"] == activity.name
    assert data["reviews_count"] == 3
    assert "created_at" in data
    assert "last_review_at" in data

def test_get_nonexistent_session(client):
    response = client.get("/study-sessions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Study session with id 999 not found"

def test_create_review_for_nonexistent_session(client):
    response = client.post("/study-sessions/999/reviews", json={
        "word_id": 1,
        "correct": True
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Study session with id 999 not found"

def test_create_review_for_word_not_in_group(client, db_session):
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
    
    session = StudySession(group_id=group.id, study_activity_id=activity.id)
    db_session.add(session)
    db_session.commit()
    
    # Try to create a review for a word that doesn't exist
    response = client.post(f"/study-sessions/{session.id}/reviews", json={
        "word_id": 999,
        "correct": True
    })
    assert response.status_code == 404
    assert "not found or does not belong to the session's group" in response.json()["detail"]

def test_create_study_session_group_not_found(client, db_session):
    """Test creating a session with a non-existent group."""
    # Create an activity
    activity = StudyActivity(
        name="Flashcards",
        url="/study/flashcards",
        description="Practice with flashcards",
        image_url="/images/flashcards.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()
    
    # Try to create a session with a non-existent group
    session_data = {
        "group_id": 999,  # Non-existent group ID
        "study_activity_id": activity.id
    }
    response = client.post("/study-sessions", json=session_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Group with id 999 not found"

def test_get_study_sessions_sorting(client, db_session):
    """Test different sorting options for study sessions."""
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
    response = client.get("/study-sessions?language_code=ja&sort_by=last_review_at&order=desc")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    
    # Most recent review should be first
    assert items[0]["id"] == sessions[0].id
    assert items[1]["id"] == sessions[1].id
    assert items[2]["id"] == sessions[2].id
    
    # Test sorting by last_review_at in ascending order
    response = client.get("/study-sessions?language_code=ja&sort_by=last_review_at&order=asc")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    
    # Oldest review should be first
    assert items[0]["id"] == sessions[2].id
    assert items[1]["id"] == sessions[1].id
    assert items[2]["id"] == sessions[0].id 
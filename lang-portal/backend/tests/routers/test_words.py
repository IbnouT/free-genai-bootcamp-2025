from app.models import Word, WordReviewItem, StudySession, StudyActivity, Group, WordGroup, Language

def test_get_words_empty(client, db_session):
    response = client.get("/words?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "total": 0,
        "items": [],
        "page": 1,
        "per_page": 10  # Default page size
    }

def test_get_words_pagination(client, db_session):
    # Create test words
    words = [
        Word(script="食べる", transliteration="taberu", meaning="to eat", language_code="ja"),
        Word(script="飲む", transliteration="nomu", meaning="to drink", language_code="ja"),
        Word(script="読む", transliteration="yomu", meaning="to read", language_code="ja"),
    ]
    db_session.add_all(words)
    db_session.commit()

    # Create a group first
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()

    # Create a study activity
    study_activity = StudyActivity(
        name="Flashcards",
        url="/activities/flashcards",
        description="Practice vocabulary with interactive flashcards",
        image_url="/static/images/activities/flashcards.svg",
        is_language_specific=False
    )
    db_session.add(study_activity)
    db_session.commit()

    # Create a study session
    study_session = StudySession(
        study_activity_id=study_activity.id,
        group_id=group.id
    )
    db_session.add(study_session)
    db_session.commit()

    # Add some review items
    review_items = [
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=False),
    ]
    db_session.add_all(review_items)
    db_session.commit()

    # Test first page
    response = client.get("/words?language_code=ja&page=1&per_page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["per_page"] == 2
    assert len(data["items"]) == 2
    # Verify word fields
    assert data["items"][0]["id"] is not None
    assert data["items"][0]["script"] == "食べる"
    assert data["items"][0]["transliteration"] == "taberu"
    assert data["items"][0]["meaning"] == "to eat"
    assert data["items"][0]["stats"]["correct_count"] == 2
    assert data["items"][0]["stats"]["wrong_count"] == 1

    # Test second page
    response = client.get("/words?language_code=ja&page=2&per_page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["per_page"] == 2
    assert len(data["items"]) == 1

def test_get_words_sorting(client, db_session):
    # Create test words
    words = [
        Word(script="citron", meaning="lemon", language_code="fr"),
        Word(script="pomme", meaning="apple", language_code="fr"),
        Word(script="banane", meaning="banana", language_code="fr"),
    ]
    db_session.add_all(words)
    db_session.commit()

    # Create a group
    group = Group(name="Fruits", language_code="fr")
    db_session.add(group)
    db_session.commit()

    # Create a study activity
    study_activity = StudyActivity(
        name="Flashcards",
        url="/activities/flashcards",
        description="Practice vocabulary with interactive flashcards",
        image_url="/static/images/activities/flashcards.svg",
        is_language_specific=False
    )
    db_session.add(study_activity)
    db_session.commit()

    # Create a study session
    study_session = StudySession(
        study_activity_id=study_activity.id,
        group_id=group.id
    )
    db_session.add(study_session)
    db_session.commit()

    # Add review items with different counts to test sorting
    review_items = [
        # pomme: 2 correct, 1 wrong
        WordReviewItem(word_id=words[1].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[1].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[1].id, study_session_id=study_session.id, correct=False),
        # citron: 1 correct, 1 wrong
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=False),
    ]
    db_session.add_all(review_items)
    db_session.commit()

    # Test sorting by script in descending order
    response = client.get("/words?language_code=fr&sort_by=script&order=desc")
    assert response.status_code == 200
    data = response.json()
    # With desc order, the order should be pomme, citron, banane
    assert data["items"][0]["script"] == "pomme"
    assert data["items"][1]["script"] == "citron"
    assert data["items"][2]["script"] == "banane"
    assert data["page"] == 1
    assert data["per_page"] == 10
    assert data["total"] == 3
    assert data["items"][0]["stats"]["correct_count"] == 2
    assert data["items"][0]["stats"]["wrong_count"] == 1
    assert data["items"][1]["stats"]["correct_count"] == 1
    assert data["items"][1]["stats"]["wrong_count"] == 1
    assert data["items"][2]["stats"]["correct_count"] == 0
    assert data["items"][2]["stats"]["wrong_count"] == 0

def test_get_word_details(client, db_session):
    # Create a word
    word = Word(
        script="食べる",
        transliteration="taberu",
        meaning="to eat",
        language_code="ja"
    )
    db_session.add(word)
    db_session.commit()

    # Create groups and link them to the word
    groups = [
        Group(name="Core Verbs", language_code="ja"),
        Group(name="Food & Drink", language_code="ja")
    ]
    db_session.add_all(groups)
    db_session.commit()

    # Link word to both groups
    word_groups = [
        WordGroup(word_id=word.id, group_id=groups[0].id),
        WordGroup(word_id=word.id, group_id=groups[1].id)
    ]
    db_session.add_all(word_groups)
    db_session.commit()

    # Create some review items
    study_activity = StudyActivity(
        name="Flashcards",
        url="/activities/flashcards",
        description="Practice vocabulary with interactive flashcards",
        image_url="/static/images/activities/flashcards.svg",
        is_language_specific=False
    )
    db_session.add(study_activity)
    db_session.commit()

    study_session = StudySession(
        study_activity_id=study_activity.id,
        group_id=groups[0].id
    )
    db_session.add(study_session)
    db_session.commit()

    # Add review items (2 correct, 1 wrong)
    review_items = [
        WordReviewItem(word_id=word.id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=word.id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=word.id, study_session_id=study_session.id, correct=False),
    ]
    db_session.add_all(review_items)
    db_session.commit()

    # Test the endpoint
    response = client.get(f"/words/{word.id}")
    assert response.status_code == 200
    data = response.json()

    # Verify the response matches spec exactly
    assert data == {
        "id": word.id,
        "script": "食べる",
        "transliteration": "taberu",
        "meaning": "to eat",
        "stats": {
            "correct_count": 2,
            "wrong_count": 1
        },
        "groups": [
            {
                "id": groups[0].id,
                "name": "Core Verbs"
            },
            {
                "id": groups[1].id,
                "name": "Food & Drink"
            }
        ]
    }

def test_get_word_not_found(client, db_session):
    response = client.get("/words/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Word with id 999 not found"

def test_get_word_no_reviews(client, db_session):
    # Create a word without any reviews
    word = Word(
        script="新しい",
        transliteration="atarashii",
        meaning="new",
        language_code="ja"
    )
    db_session.add(word)
    db_session.commit()

    response = client.get(f"/words/{word.id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == word.id
    assert data["script"] == "新しい"
    assert data["stats"]["correct_count"] == 0
    assert data["stats"]["wrong_count"] == 0
    assert data["groups"] == []  # No groups

def test_get_words_with_review_count_sorting(client, db_session):
    """Test sorting words by correct_count and wrong_count."""
    # Create test data
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    # Create words
    words = [
        Word(script="食べる", meaning="to eat", language_code="ja"),
        Word(script="飲む", meaning="to drink", language_code="ja"),
        Word(script="話す", meaning="to speak", language_code="ja")
    ]
    db_session.add_all(words)
    db_session.commit()
    
    # Create a group and session for reviews
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
    
    # Add reviews with different correct/wrong counts
    # Word 1: 3 correct, 1 wrong
    # Word 2: 2 correct, 2 wrong
    # Word 3: 1 correct, 3 wrong
    for i, word in enumerate(words):
        correct_reviews = 3 - i
        wrong_reviews = i + 1
        
        # Add correct reviews
        for _ in range(correct_reviews):
            review = WordReviewItem(
                word_id=word.id,
                study_session_id=session.id,
                correct=True
            )
            db_session.add(review)
            
        # Add wrong reviews
        for _ in range(wrong_reviews):
            review = WordReviewItem(
                word_id=word.id,
                study_session_id=session.id,
                correct=False
            )
            db_session.add(review)
    
    db_session.commit()
    
    # Test sorting by correct_count desc
    response = client.get("/words?language_code=ja&sort_by=correct_count&order=desc")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    
    assert items[0]["id"] == words[0].id  # Most correct (3)
    assert items[1]["id"] == words[1].id  # Medium correct (2)
    assert items[2]["id"] == words[2].id  # Least correct (1)
    
    # Test sorting by wrong_count desc
    response = client.get("/words?language_code=ja&sort_by=wrong_count&order=desc")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    
    assert items[0]["id"] == words[2].id  # Most wrong (3)
    assert items[1]["id"] == words[1].id  # Medium wrong (2)
    assert items[2]["id"] == words[0].id  # Least wrong (1)
from app.models import Group, Word, WordGroup, StudyActivity, StudySession, WordReviewItem

def test_get_groups_empty(client, db_session):
    response = client.get("/groups?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "total": 0,
        "items": [],
        "page": 1,
        "per_page": 10  # Default page size
    }

def test_get_groups(client, db_session):
    # Create test groups
    groups = [
        Group(
            name="Core Verbs",
        ),
        Group(
            name="Food & Drink",
        )
    ]
    db_session.add_all(groups)
    db_session.commit()

    # Add some words to groups
    words = [
        Word(script="食べる", meaning="to eat", language_code="ja"),
        Word(script="飲む", meaning="to drink", language_code="ja"),
        Word(script="manger", meaning="to eat", language_code="fr")
    ]
    db_session.add_all(words)
    db_session.commit()

    # Link words to groups
    db_session.add(WordGroup(word_id=words[0].id, group_id=groups[0].id))
    db_session.add(WordGroup(word_id=words[1].id, group_id=groups[0].id))
    db_session.add(WordGroup(word_id=words[1].id, group_id=groups[1].id))
    db_session.add(WordGroup(word_id=words[2].id, group_id=groups[0].id))
    db_session.add(WordGroup(word_id=words[2].id, group_id=groups[1].id))
    db_session.commit()

    response = client.get("/groups?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "Core Verbs"
    assert data["items"][0]["words_count"] == 2  # Two Japanese words
    assert data["items"][1]["name"] == "Food & Drink"
    assert data["items"][1]["words_count"] == 1  # One Japanese word

def test_get_group_details(client, db_session):
    # Create a group
    group = Group(name="Core Verbs")
    db_session.add(group)
    db_session.commit()

    # Create words in different languages
    words = [
        Word(script="食べる", transliteration="taberu", meaning="to eat", language_code="ja"),
        Word(script="飲む", transliteration="nomu", meaning="to drink", language_code="ja"),
        Word(script="manger", transliteration=None, meaning="to eat", language_code="fr")
    ]
    db_session.add_all(words)
    db_session.commit()

    # Link words to group
    word_groups = [
        WordGroup(word_id=word.id, group_id=group.id)
        for word in words
    ]
    db_session.add_all(word_groups)
    db_session.commit()

    # Add some review items
    study_activity = StudyActivity(name="Flashcards", url="/activities/flashcards")
    db_session.add(study_activity)
    db_session.commit()

    study_session = StudySession(
        study_activity_id=study_activity.id,
        group_id=group.id
    )
    db_session.add(study_session)
    db_session.commit()

    # Add reviews for first word
    review_items = [
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=study_session.id, correct=False),
    ]
    db_session.add_all(review_items)
    db_session.commit()

    # Test Japanese words
    response = client.get(f"/groups/{group.id}?language_code=ja")
    assert response.status_code == 200
    data = response.json()

    assert data == {
        "id": group.id,
        "name": "Core Verbs",
        "words_count": 2,  # Only Japanese words
        "words": {
            "items": [
                {
                    "id": words[0].id,
                    "script": "食べる",
                    "transliteration": "taberu",
                    "meaning": "to eat",
                    "language_code": "ja",
                    "correct_count": 2,
                    "wrong_count": 1
                },
                {
                    "id": words[1].id,
                    "script": "飲む",
                    "transliteration": "nomu",
                    "meaning": "to drink",
                    "language_code": "ja",
                    "correct_count": 0,
                    "wrong_count": 0
                }
            ],
            "page": 1,
            "per_page": 10
        }
    }

def test_get_group_not_found(client, db_session):
    response = client.get("/groups/999?language_code=ja")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group with id 999 not found"

def test_get_group_empty_words(client, db_session):
    # Create a group without any words
    group = Group(name="Empty Group")
    db_session.add(group)
    db_session.commit()

    response = client.get(f"/groups/{group.id}?language_code=ja")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == group.id
    assert data["name"] == "Empty Group"
    assert data["words_count"] == 0
    assert data["words"]["items"] == []
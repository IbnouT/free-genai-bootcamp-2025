from app.models import Group, Word, WordGroup, StudyActivity, StudySession, WordReviewItem, Language

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
            language_code="ja"
        ),
        Group(
            name="Food & Drink",
            language_code="ja"
        ),
        Group(  # Add a French group
            name="Verbes",
            language_code="fr"
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

    # Link words to groups (only matching languages)
    db_session.add(WordGroup(word_id=words[0].id, group_id=groups[0].id))  # Japanese word to Japanese group
    db_session.add(WordGroup(word_id=words[1].id, group_id=groups[0].id))  # Japanese word to Japanese group
    db_session.add(WordGroup(word_id=words[1].id, group_id=groups[1].id))  # Japanese word to Japanese group
    db_session.add(WordGroup(word_id=words[2].id, group_id=groups[2].id))  # French word to French group
    db_session.commit()

    # Test Japanese groups
    response = client.get("/groups?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 2  # Only Japanese groups
    assert data["items"][0]["name"] == "Core Verbs"
    assert data["items"][0]["words_count"] == 2  # Two Japanese words
    assert data["items"][1]["name"] == "Food & Drink"
    assert data["items"][1]["words_count"] == 1  # One Japanese word

    # Test French groups
    response = client.get("/groups?language_code=fr")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 1  # Only French group
    assert data["items"][0]["name"] == "Verbes"
    assert data["items"][0]["words_count"] == 1  # One French word

def test_get_group_details(client, db_session):
    # Create a group
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()

    # Create words in different languages
    words = [
        Word(script="食べる", transliteration="taberu", meaning="to eat", language_code="ja"),
        Word(script="飲む", transliteration="nomu", meaning="to drink", language_code="ja"),
        Word(script="manger", transliteration=None, meaning="to eat", language_code="fr")  # French word
    ]
    db_session.add_all(words)
    db_session.commit()

    # Link only Japanese words to Japanese group
    word_groups = [
        WordGroup(word_id=words[0].id, group_id=group.id),  # Japanese word
        WordGroup(word_id=words[1].id, group_id=group.id)   # Japanese word
        # Intentionally NOT linking the French word
    ]
    db_session.add_all(word_groups)
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
    response = client.get(f"/groups/{group.id}")
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
                    "stats": {
                        "correct_count": 2,
                        "wrong_count": 1
                    }
                },
                {
                    "id": words[1].id,
                    "script": "飲む",
                    "transliteration": "nomu",
                    "meaning": "to drink",
                    "stats": {
                        "correct_count": 0,
                        "wrong_count": 0
                    }
                }
            ],
            "page": 1,
            "per_page": 10
        }
    }

    # Verify French word is not included
    french_words = [item for item in data["words"]["items"] if item["script"] == "manger"]
    assert len(french_words) == 0

def test_get_group_not_found(client, db_session):
    response = client.get("/groups/999?language_code=ja")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group with id 999 not found"

def test_get_group_empty_words(client, db_session):
    # Create a group without any words
    group = Group(name="Empty Group", language_code="ja")
    db_session.add(group)
    db_session.commit()

    response = client.get(f"/groups/{group.id}?language_code=ja")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == group.id
    assert data["name"] == "Empty Group"
    assert data["words_count"] == 0
    assert data["words"]["items"] == []

def test_get_groups_sorting(client, db_session):
    """Test sorting functionality for groups endpoint."""
    # Create test groups with different word counts
    groups = [
        Group(name="Group A", language_code="ja"),
        Group(name="Group B", language_code="ja"),
        Group(name="Group C", language_code="ja")
    ]
    db_session.add_all(groups)
    db_session.commit()

    # Add different numbers of words to each group
    words = []
    for i in range(5):  # Group A: 5 words
        word = Word(script=f"word{i}", meaning=f"meaning{i}", language_code="ja")
        words.append(word)
        db_session.add(word)
    db_session.commit()
    for word in words:
        db_session.add(WordGroup(word_id=word.id, group_id=groups[0].id))
    
    words = []
    for i in range(3):  # Group B: 3 words
        word = Word(script=f"wordB{i}", meaning=f"meaningB{i}", language_code="ja")
        words.append(word)
        db_session.add(word)
    db_session.commit()
    for word in words:
        db_session.add(WordGroup(word_id=word.id, group_id=groups[1].id))
    
    words = []
    for i in range(4):  # Group C: 4 words
        word = Word(script=f"wordC{i}", meaning=f"meaningC{i}", language_code="ja")
        words.append(word)
        db_session.add(word)
    db_session.commit()
    for word in words:
        db_session.add(WordGroup(word_id=word.id, group_id=groups[2].id))
    
    db_session.commit()

    # Test sorting by name ascending
    response = client.get("/groups?language_code=ja&sort_by=name&order=asc")
    assert response.status_code == 200
    data = response.json()
    names = [item["name"] for item in data["items"]]
    assert names == ["Group A", "Group B", "Group C"]

    # Test sorting by name descending
    response = client.get("/groups?language_code=ja&sort_by=name&order=desc")
    assert response.status_code == 200
    data = response.json()
    names = [item["name"] for item in data["items"]]
    assert names == ["Group C", "Group B", "Group A"]

    # Test sorting by words_count ascending
    response = client.get("/groups?language_code=ja&sort_by=words_count&order=asc")
    assert response.status_code == 200
    data = response.json()
    word_counts = [item["words_count"] for item in data["items"]]
    assert word_counts == [3, 4, 5]

    # Test sorting by words_count descending
    response = client.get("/groups?language_code=ja&sort_by=words_count&order=desc")
    assert response.status_code == 200
    data = response.json()
    word_counts = [item["words_count"] for item in data["items"]]
    assert word_counts == [5, 4, 3]

def test_get_groups_pagination(client, db_session):
    """Test pagination functionality for groups endpoint."""
    # Create 15 test groups
    groups = [
        Group(name=f"Group {i}", language_code="ja")
        for i in range(15)
    ]
    db_session.add_all(groups)
    db_session.commit()

    # Test first page (default 10 per page)
    response = client.get("/groups?language_code=ja")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["per_page"] == 10

    # Test second page
    response = client.get("/groups?language_code=ja&page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 5
    assert data["page"] == 2

    # Test custom page size
    response = client.get("/groups?language_code=ja&per_page=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 5
    assert data["per_page"] == 5

    # Test empty page
    response = client.get("/groups?language_code=ja&page=4")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 0

def test_get_group_sorting(client, db_session):
    """Test sorting functionality for specific group endpoint."""
    # Create a test group
    group = Group(name="Test Group", language_code="ja")
    db_session.add(group)
    db_session.commit()

    # Create test words with different review stats
    words = []
    for i in range(5):
        word = Word(
            script=f"word{i}",
            transliteration=f"trans{i}",
            meaning=f"meaning{i}",
            language_code="ja"
        )
        words.append(word)
        db_session.add(word)
    db_session.commit()

    # Link words to group
    for word in words:
        db_session.add(WordGroup(word_id=word.id, group_id=group.id))
    db_session.commit()

    # Create a study session
    activity = StudyActivity(
        name="Test Activity",
        url="/test",
        description="Test Description",
        image_url="/test.png",
        is_language_specific=False
    )
    db_session.add(activity)
    db_session.commit()

    session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id
    )
    db_session.add(session)
    db_session.commit()

    # Add different review counts for each word
    reviews = [
        # word[0]: 3 correct, 1 wrong
        WordReviewItem(word_id=words[0].id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=words[0].id, study_session_id=session.id, correct=False),
        
        # word[1]: 1 correct, 2 wrong
        WordReviewItem(word_id=words[1].id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=words[1].id, study_session_id=session.id, correct=False),
        WordReviewItem(word_id=words[1].id, study_session_id=session.id, correct=False),
        
        # word[2]: 2 correct, 0 wrong
        WordReviewItem(word_id=words[2].id, study_session_id=session.id, correct=True),
        WordReviewItem(word_id=words[2].id, study_session_id=session.id, correct=True),
    ]
    db_session.add_all(reviews)
    db_session.commit()

    # Test sorting by correct_count ascending
    response = client.get(f"/groups/{group.id}?sort_by=correct_count&order=asc")
    assert response.status_code == 200
    data = response.json()
    correct_counts = [item["stats"]["correct_count"] for item in data["words"]["items"]]
    assert correct_counts[:3] == [0, 0, 1]  # First three items

    # Test sorting by correct_count descending
    response = client.get(f"/groups/{group.id}?sort_by=correct_count&order=desc")
    assert response.status_code == 200
    data = response.json()
    correct_counts = [item["stats"]["correct_count"] for item in data["words"]["items"]]
    assert correct_counts[:3] == [3, 2, 1]  # First three items

    # Test sorting by script
    response = client.get(f"/groups/{group.id}?sort_by=script&order=asc")
    assert response.status_code == 200
    data = response.json()
    scripts = [item["script"] for item in data["words"]["items"]]
    assert scripts == sorted(scripts)

    # Test sorting by wrong_count
    response = client.get(f"/groups/{group.id}?sort_by=wrong_count&order=desc")
    assert response.status_code == 200
    data = response.json()
    wrong_counts = [item["stats"]["wrong_count"] for item in data["words"]["items"]]
    assert wrong_counts[:3] == [2, 1, 0]  # First three items

def test_get_group_words_sorting(client, db_session):
    """Test sorting words in group details by word attributes."""
    # Create test data
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    group = Group(name="Core Verbs", language_code="ja")
    db_session.add(group)
    db_session.commit()
    
    # Create words with different scripts to test sorting
    words = [
        Word(script="食べる", meaning="to eat", language_code="ja"),
        Word(script="飲む", meaning="to drink", language_code="ja"),
        Word(script="話す", meaning="to speak", language_code="ja")
    ]
    db_session.add_all(words)
    db_session.commit()
    
    # Add words to group
    for word in words:
        word_group = WordGroup(word_id=word.id, group_id=group.id)
        db_session.add(word_group)
    db_session.commit()
    
    # Test sorting by script in descending order
    response = client.get(f"/groups/{group.id}?sort_by=script&order=desc")
    assert response.status_code == 200
    data = response.json()
    
    # Check that words are sorted by script in descending order
    items = data["words"]["items"]
    # In descending order by Unicode values:
    # 飲 (U+98F2) comes first (highest)
    # 食 (U+98DF) comes second
    # 話 (U+8A71) comes last (lowest)
    assert items[0]["script"] == "飲む"
    assert items[1]["script"] == "食べる"
    assert items[2]["script"] == "話す"
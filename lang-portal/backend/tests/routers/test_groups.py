from app.models import Group, Word, WordGroup

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
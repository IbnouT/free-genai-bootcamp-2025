from app.main import app
from app.models import Word

def test_get_words_empty(client, db_session):
    response = client.get("/words")
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

    # Test first page
    response = client.get("/words?page=1&per_page=2")
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

    # Test second page
    response = client.get("/words?page=2&per_page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["per_page"] == 2
    assert len(data["items"]) == 1

def test_get_words_sorting(client, db_session):
    words = [
        Word(script="citron", meaning="lemon", language_code="fr"),
        Word(script="pomme", meaning="apple", language_code="fr"),
        Word(script="banane", meaning="banana", language_code="fr"),
    ]
    db_session.add_all(words)
    db_session.commit()

    # Test sorting by script in descending order
    response = client.get("/words?sort_by=script&order=desc")
    assert response.status_code == 200
    data = response.json()
    # With desc order, the order should be pomme, citron, banane
    assert data["items"][0]["script"] == "pomme"
    assert data["items"][1]["script"] == "citron"
    assert data["items"][2]["script"] == "banane"
    assert data["page"] == 1
    assert data["per_page"] == 10
    assert data["total"] == 3
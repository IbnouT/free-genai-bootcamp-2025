from app.models import Language

def test_get_languages(client, db_session):
    # Create test languages
    languages = [
        Language(code="ja", name="Japanese", promo_text="Test promo"),
        Language(code="fr", name="French", active=False, promo_text="Test promo 2"),
    ]
    db_session.add_all(languages)
    db_session.commit()
    
    # Test getting all languages
    response = client.get("/languages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["code"] == "ja"
    assert data[0]["promo_text"] == "Test promo"
    
    # Test filtering active languages
    response = client.get("/languages?active=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "ja" 
import pytest
from sqlalchemy.exc import IntegrityError
from app.models.word import Word

def test_word_creation(db_session):
    word = Word(
        original="hello",
        translation="bonjour",
        context="Greeting someone",
        notes="Common greeting"
    )
    db_session.add(word)
    db_session.commit()
    
    assert word.id is not None
    assert word.original == "hello"
    assert word.translation == "bonjour"

def test_word_requires_original_and_translation(db_session):
    word = Word(original="hello")  # Missing translation
    db_session.add(word)
    with pytest.raises(IntegrityError):
        db_session.commit() 
import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Word, Group, WordGroup, StudyActivity, StudySession, WordReviewItem, Language

def create_test_language(db_session, code="ja"):
    language = Language(code=code, name=f"{code} language")
    db_session.add(language)
    db_session.commit()
    return language

def test_word_creation(db_session):
    language = create_test_language(db_session)
    word = Word(
        script="食べる",
        transliteration="taberu",
        meaning="to eat",
        language_code=language.code
    )
    db_session.add(word)
    db_session.commit()
    
    assert word.id is not None
    assert word.script == "食べる"
    assert word.transliteration == "taberu"
    assert word.meaning == "to eat"

def test_word_requires_script_and_meaning(db_session):
    language = create_test_language(db_session, code="fr")
    
    # Test missing script
    word1 = Word(meaning="to eat", language_code=language.code)
    db_session.add(word1)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    
    # Test missing meaning
    language = create_test_language(db_session, code="es")
    word2 = Word(script="食べる", language_code=language.code)
    db_session.add(word2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    
    # Test missing language_code
    word3 = Word(script="食べる", meaning="to eat")
    db_session.add(word3)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_transliteration_is_optional(db_session):
    language = create_test_language(db_session)
    word = Word(
        script="食べる",
        meaning="to eat",
        language_code=language.code
    )
    db_session.add(word)
    db_session.commit()
    
    assert word.id is not None
    assert word.transliteration is None

def test_word_group_relationship(db_session):
    language = create_test_language(db_session)
    word = Word(script="食べる", meaning="to eat", language_code=language.code)
    group = Group(name="Verbs")
    
    db_session.add(word)
    db_session.add(group)
    db_session.commit()
    
    word.groups.append(group)
    db_session.commit()
    
    assert len(word.groups) == 1
    assert word.groups[0].name == "Verbs"
    assert len(group.words) == 1
    assert group.words[0].script == "食べる"

def test_word_group_join_table(db_session):
    language = create_test_language(db_session)
    word = Word(script="食べる", meaning="to eat", language_code=language.code)
    group = Group(name="Verbs")
    
    db_session.add(word)
    db_session.add(group)
    db_session.commit()
    
    word.groups.append(group)
    db_session.commit()
    
    # Query the join table directly
    word_group = db_session.query(WordGroup).filter_by(
        word_id=word.id,
        group_id=group.id
    ).first()
    
    assert word_group is not None
    assert word_group.word_id == word.id
    assert word_group.group_id == group.id

def test_group_creation(db_session):
    group = Group(name="Verbs")
    db_session.add(group)
    db_session.commit()
    
    assert group.id is not None
    assert group.name == "Verbs"

def test_study_activity_creation(db_session):
    activity = StudyActivity(
        name="Flashcards",
        url="/activities/flashcards"
    )
    db_session.add(activity)
    db_session.commit()
    
    assert activity.id is not None
    assert activity.name == "Flashcards"

def test_study_session_creation(db_session):
    group = Group(name="Verbs")
    activity = StudyActivity(name="Flashcards", url="/activities/flashcards")
    db_session.add_all([group, activity])
    db_session.commit()
    
    session = StudySession(
        group_id=group.id,
        study_activity_id=activity.id
    )
    db_session.add(session)
    db_session.commit()
    
    assert session.id is not None
    assert session.created_at is not None

def test_word_review_creation(db_session):
    language = create_test_language(db_session)
    word = Word(script="食べる", meaning="to eat", language_code=language.code)
    group = Group(name="Verbs")
    activity = StudyActivity(name="Flashcards", url="/activities/flashcards")
    db_session.add_all([word, group, activity])
    db_session.commit()
    
    session = StudySession(group_id=group.id, study_activity_id=activity.id)
    db_session.add(session)
    db_session.commit()
    
    review = WordReviewItem(
        word_id=word.id,
        study_session_id=session.id,
        correct=True
    )
    db_session.add(review)
    db_session.commit()
    
    assert review.id is not None
    assert review.correct is True
    assert review.created_at is not None

def test_language_creation(db_session):
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    assert language.code == "ja"
    assert language.name == "Japanese"
    assert language.active == True  # default value

def test_word_with_language(db_session):
    # Create language first
    language = Language(code="ja", name="Japanese")
    db_session.add(language)
    db_session.commit()
    
    # Create word with language
    word = Word(
        script="食べる",
        transliteration="taberu",
        meaning="to eat",
        language_code="ja"
    )
    db_session.add(word)
    db_session.commit()
    
    # Test relationships
    assert word.language.code == "ja"
    assert word.language.name == "Japanese"
    assert language.words[0].script == "食べる" 
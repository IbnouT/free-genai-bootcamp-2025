from app.seed import seed_all
import pytest
from app.models import Language, Group, Word
import subprocess
import sys
import os

def test_seed_all(db_session):
    data = seed_all(db_session, include_test_data=True)
    
    # Verify the number of seeded items
    assert len(data["languages"]) == 8  # 4 active (ja, fr, ar, es) + 4 inactive (zh, ko, ru, de)
    assert len(data["groups"]) == 28  # 7 groups per active language (4 languages)
    assert len(data["activities"]) == 5  # Flashcards, Typing, Quiz, Writing, Pronunciation
    assert len(data["words"]) > 0  # At least some words were seeded
    
    # Check languages
    assert any(l.code == "ja" for l in data["languages"])
    
    # Check active/inactive status
    active_langs = [l for l in data["languages"] if l.active]
    inactive_langs = [l for l in data["languages"] if not l.active]
    assert len(active_langs) == 4  # ja, fr, ar, es
    assert len(inactive_langs) == 4  # zh, ko, ru, de
    
    # Check words
    assert len(data["words"]) >= 48  # 12 words per language, 4 languages
    
    # Check group templates (without language suffixes)
    expected_group_templates = {
        "Core Verbs",
        "Common Phrases",
        "Objects",
        "Places",
        "Adjectives",
        "Numbers & Time",
        "Food & Drink"
    }
    
    # Extract base group names by removing language suffixes
    actual_group_templates = {g.name.split(" (")[0] for g in data["groups"]}
    assert actual_group_templates == expected_group_templates
    
    # Verify each active language has all group templates
    for lang in active_langs:
        lang_groups = {g.name.split(" (")[0] for g in data["groups"] if g.language_code == lang.code}
        assert lang_groups == expected_group_templates, f"Missing group templates for language {lang.code}"
    
    # Check activities
    assert len(data["activities"]) == 5
    
    # Check word-group relationships
    ja_food_group = next(g for g in data["groups"] if "Food & Drink" in g.name and g.language_code == "ja")
    assert len(ja_food_group.words) > 0  # Food group has words
    
    # Check multiple group assignments
    ja_food_words = [w for w in data["words"] if "eat" in w.meaning or "drink" in w.meaning and w.language_code == "ja"]
    for word in ja_food_words:
        # Should be in both "Core Verbs" and "Food & Drink"
        group_templates = {g.name.split(" (")[0] for g in word.groups}
        assert "Core Verbs" in group_templates
        assert "Food & Drink" in group_templates
        
    # Check test data
    ja_core_verbs = next(g for g in data["groups"] if "Core Verbs" in g.name and g.language_code == "ja")
    taberu = next(w for w in ja_core_verbs.words if w.meaning == "to eat")
    nomu = next(w for w in ja_core_verbs.words if w.meaning == "to drink")
    hanasu = next(w for w in ja_core_verbs.words if w.meaning == "to speak")
    
    # Check review counts
    assert len([r for r in taberu.review_items if r.correct]) == 7  # 7 correct
    assert len([r for r in taberu.review_items if not r.correct]) == 2  # 2 wrong
    assert len([r for r in nomu.review_items if r.correct]) == 5  # 5 correct
    assert len([r for r in nomu.review_items if not r.correct]) == 3  # 3 wrong
    assert len([r for r in hanasu.review_items if r.correct]) == 2  # 2 correct
    assert len([r for r in hanasu.review_items if not r.correct]) == 6  # 6 wrong

def test_seed_all_without_test_data(db_session):
    """Test seeding without test data to cover the if __name__ == '__main__' block."""
    data = seed_all(db_session, include_test_data=False)
    assert data["sessions"] is None
    
def test_seed_word_groups_with_inactive_language(db_session):
    """Test the continue statement in seed_word_groups for inactive languages."""
    from app.seed import seed_word_groups
    
    # Create an inactive language
    inactive_lang = Language(
        code="test_lang",
        name="Test Language",
        active=False
    )
    db_session.add(inactive_lang)
    
    # Create a word for the inactive language
    word = Word(
        language_code=inactive_lang.code,
        script="test",
        meaning="to test",  # This would normally put it in Core Verbs
        transliteration="test"
    )
    db_session.add(word)
    db_session.commit()
    
    seed_word_groups(db_session, [word], [])
    
    # Verify the word has no groups (because it's for an inactive language)
    db_session.refresh(word)
    assert word.groups == []

def test_command_line_seeding(monkeypatch):
    """Test the command-line interface of the seed script."""
    # Set up test environment
    monkeypatch.setenv("RUNNING_TEST_ON_DEV", "true")
    
    # Get the path to seed.py
    seed_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "seed.py")
    
    # Test without test data
    result = subprocess.run([sys.executable, seed_script_path], 
                          capture_output=True, 
                          text=True,
                          env={**os.environ, "RUNNING_TEST_ON_DEV": "true"})
    assert result.returncode == 0
    assert "Database seeding completed successfully!" in result.stdout
    assert "Test data" not in result.stdout

    # Test with test data
    result = subprocess.run([sys.executable, seed_script_path, "--include-test-data"], 
                          capture_output=True, 
                          text=True,
                          env={**os.environ, "RUNNING_TEST_ON_DEV": "true"})
    assert result.returncode == 0
    assert "Database seeding completed successfully!" in result.stdout
    assert "Test data (study sessions and reviews) was included." in result.stdout 

def test_command_line_seeding_error():
    """Test error handling in the command line interface."""
    # Get the path to seed.py
    seed_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "seed.py")
    
    # Run with --test-error flag to trigger the error handling
    result = subprocess.run([sys.executable, seed_script_path, "--test-error"], 
                          capture_output=True, 
                          text=True)
    
    assert result.returncode != 0
    assert "Error seeding database: Test error for error handling" in result.stdout

def test_seed_all_error(db_session):
    """Test error handling in seed_all function."""
    from app.seed import seed_all
    from sqlalchemy.exc import IntegrityError
    
    # Create a duplicate language to cause an integrity error
    lang1 = Language(code="test", name="Test")
    lang2 = Language(code="test", name="Test")  # Same code will cause unique constraint violation
    db_session.add(lang1)
    db_session.add(lang2)
    
    with pytest.raises(Exception) as exc_info:
        seed_all(db_session, include_test_data=False)
    
    assert "Error seeding database" in str(exc_info.value) 
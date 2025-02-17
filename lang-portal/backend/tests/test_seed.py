from app.seed import seed_all

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
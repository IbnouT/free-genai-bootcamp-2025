from app.seed import seed_all

def test_seed_all(db_session):
    data = seed_all(db_session)
    
    # Check languages
    assert len(data["languages"]) == 8
    assert any(l.code == "ja" for l in data["languages"])
    
    # Check active/inactive status
    active_langs = [l for l in data["languages"] if l.active]
    inactive_langs = [l for l in data["languages"] if not l.active]
    assert len(active_langs) == 4  # ja, fr, ar, es
    assert len(inactive_langs) == 4  # zh, ko, ru, de
    
    # Check words
    assert len(data["words"]) >= 48  # 12 words per language, 4 languages
    
    # Check groups
    assert len(data["groups"]) == 6
    expected_groups = {"Core Verbs", "Common Phrases", "Food & Drink", 
                      "Movement", "Communication", "Daily Activities"}
    actual_groups = {g.name for g in data["groups"]}
    assert actual_groups == expected_groups
    
    # Check activities
    assert len(data["activities"]) == 3
    
    # Check word-group relationships
    food_group = data["groups"][2]
    assert len(food_group.words) > 0  # Food group has words 
    
    # Check multiple group assignments
    food_words = [w for w in data["words"] if "eat" in w.meaning or "drink" in w.meaning]
    for word in food_words:
        # Should be in both "Core Verbs" and "Food & Drink"
        assert len(word.groups) >= 2
        group_names = {g.name for g in word.groups}
        assert "Core Verbs" in group_names
        assert "Food & Drink" in group_names 
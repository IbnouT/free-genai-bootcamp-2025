from sqlalchemy.orm import Session
from app.models import Language, Word, Group, StudyActivity, WordGroup, StudySession, WordReviewItem, ActivityLanguageSupport
from app.utils.db_utils import reset_database
import random

def seed_languages(db: Session):
    languages = [
        Language(
            code="ja", 
            name="Japanese",
            promo_text="Explore the rich culture and language of Japan, from its ancient traditions to modern innovations."
        ),
        Language(
            code="fr", 
            name="French",
            promo_text="Delve into the elegant language of France, known for its influence in art, cuisine, and diplomacy."
        ),
        Language(
            code="ar", 
            name="Arabic",
            promo_text="Immerse yourself in the rich and diverse language of the Arab world, spoken by millions across continents."
        ),
        Language(
            code="es", 
            name="Spanish",
            promo_text="Join the vibrant world of Spanish, a language of passion and history spoken by over 460 million people worldwide."
        ),
        # Inactive languages
        Language(
            code="zh", 
            name="Chinese", 
            active=False,
            promo_text="Master the most spoken language in the world, with its unique characters and tonal system."
        ),
        Language(
            code="ko", 
            name="Korean", 
            active=False,
            promo_text="Learn the language of K-pop and Korean dramas, with its logical writing system and rich cultural heritage."
        ),
        Language(
            code="ru", 
            name="Russian", 
            active=False,
            promo_text="Discover the language of Tolstoy and Dostoevsky, spoken across the largest country in the world."
        ),
        Language(
            code="de", 
            name="German", 
            active=False,
            promo_text="Learn the language of philosophers and scientists, known for its precision and compound words."
        ),
    ]
    db.add_all(languages)
    db.commit()
    return languages

def seed_words(db: Session):
    words = [
        # Japanese words
        # Core Verbs (kept essential ones)
        Word(script="食べる", transliteration="taberu", meaning="to eat", language_code="ja"),
        Word(script="飲む", transliteration="nomu", meaning="to drink", language_code="ja"),
        Word(script="話す", transliteration="hanasu", meaning="to speak", language_code="ja"),
        
        # Nouns - Objects
        Word(script="本", transliteration="hon", meaning="book", language_code="ja"),
        Word(script="電話", transliteration="denwa", meaning="telephone", language_code="ja"),
        Word(script="鞄", transliteration="kaban", meaning="bag", language_code="ja"),
        
        # Nouns - Places
        Word(script="学校", transliteration="gakkou", meaning="school", language_code="ja"),
        Word(script="駅", transliteration="eki", meaning="station", language_code="ja"),
        Word(script="公園", transliteration="kouen", meaning="park", language_code="ja"),
        
        # Adjectives
        Word(script="大きい", transliteration="ookii", meaning="big", language_code="ja"),
        Word(script="小さい", transliteration="chiisai", meaning="small", language_code="ja"),
        Word(script="赤い", transliteration="akai", meaning="red", language_code="ja"),
        Word(script="青い", transliteration="aoi", meaning="blue", language_code="ja"),
        
        # Numbers & Time
        Word(script="一", transliteration="ichi", meaning="one", language_code="ja"),
        Word(script="二", transliteration="ni", meaning="two", language_code="ja"),
        Word(script="今日", transliteration="kyou", meaning="today", language_code="ja"),
        Word(script="明日", transliteration="ashita", meaning="tomorrow", language_code="ja"),

        # French words
        # Core Verbs (kept essential ones)
        Word(script="manger", meaning="to eat", language_code="fr"),
        Word(script="boire", meaning="to drink", language_code="fr"),
        Word(script="parler", meaning="to speak", language_code="fr"),
        
        # Nouns - Objects
        Word(script="livre", meaning="book", language_code="fr"),
        Word(script="téléphone", meaning="telephone", language_code="fr"),
        Word(script="sac", meaning="bag", language_code="fr"),
        
        # Nouns - Places
        Word(script="école", meaning="school", language_code="fr"),
        Word(script="gare", meaning="station", language_code="fr"),
        Word(script="parc", meaning="park", language_code="fr"),
        
        # Adjectives
        Word(script="grand", meaning="big", language_code="fr"),
        Word(script="petit", meaning="small", language_code="fr"),
        Word(script="rouge", meaning="red", language_code="fr"),
        Word(script="bleu", meaning="blue", language_code="fr"),
        
        # Numbers & Time
        Word(script="un", meaning="one", language_code="fr"),
        Word(script="deux", meaning="two", language_code="fr"),
        Word(script="aujourd'hui", meaning="today", language_code="fr"),
        Word(script="demain", meaning="tomorrow", language_code="fr"),

        # Arabic words
        # Core Verbs (kept essential ones)
        Word(script="يأكل", transliteration="ya'kul", meaning="to eat", language_code="ar"),
        Word(script="يشرب", transliteration="yashrab", meaning="to drink", language_code="ar"),
        Word(script="يتكلم", transliteration="yatakallam", meaning="to speak", language_code="ar"),
        
        # Nouns - Objects
        Word(script="كتاب", transliteration="kitaab", meaning="book", language_code="ar"),
        Word(script="هاتف", transliteration="haatif", meaning="telephone", language_code="ar"),
        Word(script="حقيبة", transliteration="haqiba", meaning="bag", language_code="ar"),
        
        # Nouns - Places
        Word(script="مدرسة", transliteration="madrasa", meaning="school", language_code="ar"),
        Word(script="محطة", transliteration="mahatta", meaning="station", language_code="ar"),
        Word(script="حديقة", transliteration="hadiqa", meaning="park", language_code="ar"),
        
        # Adjectives
        Word(script="كبير", transliteration="kabir", meaning="big", language_code="ar"),
        Word(script="صغير", transliteration="saghir", meaning="small", language_code="ar"),
        Word(script="أحمر", transliteration="ahmar", meaning="red", language_code="ar"),
        Word(script="أزرق", transliteration="azraq", meaning="blue", language_code="ar"),
        
        # Numbers & Time
        Word(script="واحد", transliteration="wahid", meaning="one", language_code="ar"),
        Word(script="اثنان", transliteration="ithnan", meaning="two", language_code="ar"),
        Word(script="اليوم", transliteration="al-yawm", meaning="today", language_code="ar"),
        Word(script="غدا", transliteration="ghadan", meaning="tomorrow", language_code="ar"),

        # Spanish words
        # Core Verbs (kept essential ones)
        Word(script="comer", meaning="to eat", language_code="es"),
        Word(script="beber", meaning="to drink", language_code="es"),
        Word(script="hablar", meaning="to speak", language_code="es"),
        
        # Nouns - Objects
        Word(script="libro", meaning="book", language_code="es"),
        Word(script="teléfono", meaning="telephone", language_code="es"),
        Word(script="bolso", meaning="bag", language_code="es"),
        
        # Nouns - Places
        Word(script="escuela", meaning="school", language_code="es"),
        Word(script="estación", meaning="station", language_code="es"),
        Word(script="parque", meaning="park", language_code="es"),
        
        # Adjectives
        Word(script="grande", meaning="big", language_code="es"),
        Word(script="pequeño", meaning="small", language_code="es"),
        Word(script="rojo", meaning="red", language_code="es"),
        Word(script="azul", meaning="blue", language_code="es"),
        
        # Numbers & Time
        Word(script="uno", meaning="one", language_code="es"),
        Word(script="dos", meaning="two", language_code="es"),
        Word(script="hoy", meaning="today", language_code="es"),
        Word(script="mañana", meaning="tomorrow", language_code="es"),
        
        # Common Phrases (kept essential ones)
        Word(script="おはよう", transliteration="ohayou", meaning="good morning", language_code="ja"),
        Word(script="bonjour", meaning="good morning/hello", language_code="fr"),
        Word(script="صباح الخير", transliteration="sabah al-khayr", meaning="good morning", language_code="ar"),
        Word(script="buenos días", meaning="good morning", language_code="es"),
    ]
    db.add_all(words)
    db.commit()
    return words

def seed_activities(db: Session):
    activities = [
        StudyActivity(
            name="Flashcards",
            url="/study/flashcards",
            description="Practice vocabulary with interactive flashcards. Test your memory and track your progress.",
            image_url="/static/images/activities/flashcards.svg",
            is_language_specific=False  # Universal activity
        ),
        StudyActivity(
            name="Typing Practice",
            url="/study/typing",
            description="Improve your typing skills in your target language. Practice with real sentences and words.",
            image_url="/static/images/activities/typing.svg",
            is_language_specific=True  # Language-specific (needs special character support)
        ),
        StudyActivity(
            name="Multiple Choice",
            url="/study/quiz",
            description="Test your knowledge with multiple choice questions. A fun way to reinforce your learning.",
            image_url="/static/images/activities/quiz.svg",
            is_language_specific=False  # Universal activity
        ),
        StudyActivity(
            name="Character Writing",
            url="/study/writing",
            description="Practice writing characters and get instant feedback on your strokes.",
            image_url="/static/images/activities/writing.svg",
            is_language_specific=True  # Only for languages with special writing systems
        ),
        StudyActivity(
            name="Pronunciation",
            url="/study/pronunciation",
            description="Practice pronunciation with voice recognition technology.",
            image_url="/static/images/activities/pronunciation.svg",
            is_language_specific=True  # Language-specific audio features
        )
    ]
    db.add_all(activities)
    db.commit()
    return activities

def seed_activity_language_support(db: Session, activities: list, languages: list):
    """Set up which activities support which languages"""
    supports = []
    
    for activity in activities:
        if activity.is_language_specific:
            # Typing Practice: Support for Japanese, Chinese, Korean, Arabic
            if activity.name == "Typing Practice":
                for lang in languages:
                    if lang.code in ["ja", "zh", "ko", "ar"]:
                        supports.append(ActivityLanguageSupport(
                            activity_id=activity.id,
                            language_code=lang.code
                        ))
            
            # Character Writing: Only for Japanese, Chinese
            elif activity.name == "Character Writing":
                for lang in languages:
                    if lang.code in ["ja", "zh"]:
                        supports.append(ActivityLanguageSupport(
                            activity_id=activity.id,
                            language_code=lang.code
                        ))
            
            # Pronunciation: All active languages
            elif activity.name == "Pronunciation":
                for lang in languages:
                    if lang.active:
                        supports.append(ActivityLanguageSupport(
                            activity_id=activity.id,
                            language_code=lang.code
                        ))
    
    db.add_all(supports)
    db.commit()
    return supports

def seed_groups(db: Session, languages: list):
    """Create groups for each language"""
    groups = []
    
    # Updated group templates to match new word types
    group_templates = [
        "Core Verbs",
        "Common Phrases",
        "Objects",
        "Places",
        "Adjectives",
        "Numbers & Time",
        "Food & Drink"
    ]
    
    # Create each template group for each active language
    for lang in languages:
        if lang.active:  # Only create groups for active languages
            for template in group_templates:
                groups.append(Group(
                    name=f"{template} ({lang.name})",
                    language_code=lang.code
                ))
    
    db.add_all(groups)
    db.commit()
    return groups

def seed_word_groups(db: Session, words: list, groups: list):
    """Assign words to their appropriate language-specific groups"""
    
    # Group words by language
    words_by_lang = {}
    for word in words:
        if word.language_code not in words_by_lang:
            words_by_lang[word.language_code] = []
        words_by_lang[word.language_code].append(word)
    
    # Create a map of groups by language and template
    groups_map = {}
    for group in groups:
        lang_code = group.language_code
        if lang_code not in groups_map:
            groups_map[lang_code] = {}
        
        # Extract template name from group name (e.g., "Core Verbs (Japanese)" -> "Core Verbs")
        template = group.name.split(" (")[0]
        groups_map[lang_code][template] = group
    
    # Assign words to groups based on their characteristics
    for lang_code, lang_words in words_by_lang.items():
        if lang_code not in groups_map:
            continue  # Skip inactive languages
            
        lang_groups = groups_map[lang_code]
        
        for word in lang_words:
            word_groups = set()  # Use set to avoid duplicates
            
            # Core Verbs
            if word.meaning.startswith("to "):
                word_groups.add(lang_groups["Core Verbs"])
            
            # Common Phrases
            if any(phrase in word.meaning.lower() for phrase in ["morning", "hello", "thank", "please", "excuse", "goodbye", "sorry"]):
                word_groups.add(lang_groups["Common Phrases"])
            
            # Objects
            if any(term in word.meaning.lower() for term in ["book", "telephone", "phone", "bag", "pen", "computer"]):
                word_groups.add(lang_groups["Objects"])
            
            # Places
            if any(term in word.meaning.lower() for term in ["school", "station", "park", "hospital", "store", "restaurant", "house"]):
                word_groups.add(lang_groups["Places"])
            
            # Adjectives
            if any(term in word.meaning.lower() for term in ["big", "small", "red", "blue", "hot", "cold", "new", "old"]):
                word_groups.add(lang_groups["Adjectives"])
            
            # Numbers & Time
            if any(term in word.meaning.lower() for term in ["one", "two", "three", "today", "tomorrow", "morning", "night", "hour"]):
                word_groups.add(lang_groups["Numbers & Time"])
            
            # Food & Drink
            if any(term in word.meaning.lower() for term in ["eat", "drink", "water", "coffee", "bread", "tea", "rice", "meal", "food", "beverage"]):
                word_groups.add(lang_groups["Food & Drink"])
            
            # Add all groups to the word
            word.groups.extend(word_groups)
    
    db.commit()

def seed_test_activity_data(db: Session, words: list, groups: list, activities: list):
    """Create specific test scenarios for word reviews.
    
    Test Scenarios:
    1. Japanese Core Verbs Group:
       - "食べる" (to eat): High success (7 correct, 2 wrong)
       - "飲む" (to drink): Medium success (5 correct, 3 wrong)
       - "話す" (to speak): Low success (2 correct, 6 wrong)
    
    2. Japanese Common Phrases Group:
       - "おはよう" (good morning): Perfect score (5 correct, 0 wrong)
    
    3. French Core Verbs Group:
       - "manger" (to eat): High success (6 correct, 1 wrong)
       - "boire" (to drink): Medium success (4 correct, 4 wrong)
       - "parler" (to speak): Low success (1 correct, 5 wrong)
    """
    from datetime import datetime, timedelta
    
    # Create one study session for each active language
    sessions = {}
    flashcards_activity = next(a for a in activities if a.name == "Flashcards")
    
    # Get groups by name and language
    def get_group(name: str, lang_code: str):
        return next(g for g in groups if g.name == f"{name} ({db.query(Language).filter_by(code=lang_code).first().name})")
    
    # Japanese test scenarios
    ja_core_verbs = get_group("Core Verbs", "ja")
    ja_common_phrases = get_group("Common Phrases", "ja")
    
    # Create sessions
    sessions["ja_core"] = StudySession(
        group_id=ja_core_verbs.id,
        study_activity_id=flashcards_activity.id,
        created_at=datetime.now() - timedelta(days=1)
    )
    sessions["ja_phrases"] = StudySession(
        group_id=ja_common_phrases.id,
        study_activity_id=flashcards_activity.id,
        created_at=datetime.now() - timedelta(days=2)
    )
    
    # French test scenarios
    fr_core_verbs = get_group("Core Verbs", "fr")
    sessions["fr_core"] = StudySession(
        group_id=fr_core_verbs.id,
        study_activity_id=flashcards_activity.id,
        created_at=datetime.now() - timedelta(days=1)
    )
    
    db.add_all(sessions.values())
    db.flush()
    
    # Helper function to create reviews
    def create_reviews(word_id: int, session_id: int, correct_count: int, wrong_count: int):
        reviews = []
        # Add correct reviews
        for _ in range(correct_count):
            reviews.append(WordReviewItem(
                word_id=word_id,
                study_session_id=session_id,
                correct=True,
                created_at=datetime.now() - timedelta(hours=random.randint(1, 24))
            ))
        # Add wrong reviews
        for _ in range(wrong_count):
            reviews.append(WordReviewItem(
                word_id=word_id,
                study_session_id=session_id,
                correct=False,
                created_at=datetime.now() - timedelta(hours=random.randint(1, 24))
            ))
        return reviews
    
    # Create reviews for Japanese words
    reviews = []
    
    # Japanese Core Verbs
    taberu = next(w for w in words if w.script == "食べる")
    nomu = next(w for w in words if w.script == "飲む")
    hanasu = next(w for w in words if w.script == "話す")
    
    reviews.extend(create_reviews(taberu.id, sessions["ja_core"].id, 7, 2))  # High success
    reviews.extend(create_reviews(nomu.id, sessions["ja_core"].id, 5, 3))    # Medium success
    reviews.extend(create_reviews(hanasu.id, sessions["ja_core"].id, 2, 6))  # Low success
    
    # Japanese Common Phrases
    ohayou = next(w for w in words if w.script == "おはよう")
    reviews.extend(create_reviews(ohayou.id, sessions["ja_phrases"].id, 5, 0))  # Perfect score
    
    # French Core Verbs
    manger = next(w for w in words if w.script == "manger")
    boire = next(w for w in words if w.script == "boire")
    parler = next(w for w in words if w.script == "parler")
    
    reviews.extend(create_reviews(manger.id, sessions["fr_core"].id, 6, 1))  # High success
    reviews.extend(create_reviews(boire.id, sessions["fr_core"].id, 4, 4))   # Medium success
    reviews.extend(create_reviews(parler.id, sessions["fr_core"].id, 1, 5))  # Low success
    
    db.add_all(reviews)
    db.commit()
    
    return list(sessions.values())

def seed_all(db: Session, include_test_data: bool = False):
    """Seed all tables with initial data"""
    try:
        reset_database(db.get_bind())  # Pass the engine from session
        
        # Seed in correct order (due to foreign keys)
        languages = seed_languages(db)
        words = seed_words(db)
        activities = seed_activities(db)
        activity_support = seed_activity_language_support(db, activities, languages)
        groups = seed_groups(db, languages)
        seed_word_groups(db, words, groups)
        
        # Optionally add test activity data
        sessions = None
        if include_test_data:
            sessions = seed_test_activity_data(db, words, groups, activities)
        
        db.commit()
        return {
            "languages": languages,
            "words": words,
            "groups": groups,
            "activities": activities,
            "activity_support": activity_support,
            "sessions": sessions if include_test_data else None
        }
    except Exception as e:
        db.rollback()
        raise Exception(f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    import argparse
    from app.database import SessionLocal

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Seed the database with initial data')
    parser.add_argument('--include-test-data', action='store_true',
                       help='Include test study sessions and review data')
    
    args = parser.parse_args()
    
    # Create database session
    db = SessionLocal()
    
    try:
        print("Starting database seeding...")
        seed_all(db, include_test_data=args.include_test_data)
        print("Database seeding completed successfully!")
        if args.include_test_data:
            print("Test data (study sessions and reviews) was included.")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        raise
    finally:
        db.close() 
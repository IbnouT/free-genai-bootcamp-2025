from sqlalchemy.orm import Session
from app.models import Language, Word, Group, StudyActivity, WordGroup
from app.utils.db_utils import reset_database

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
        # Core Verbs
        Word(script="食べる", transliteration="taberu", meaning="to eat", language_code="ja"),
        Word(script="飲む", transliteration="nomu", meaning="to drink", language_code="ja"),
        Word(script="話す", transliteration="hanasu", meaning="to speak", language_code="ja"),
        
        # Common Phrases
        Word(script="おはよう", transliteration="ohayou", meaning="good morning", language_code="ja"),
        Word(script="ありがとう", transliteration="arigatou", meaning="thank you", language_code="ja"),
        Word(script="すみません", transliteration="sumimasen", meaning="excuse me/sorry", language_code="ja"),
        
        # Food & Drink
        Word(script="水", transliteration="mizu", meaning="water", language_code="ja"),
        Word(script="お茶", transliteration="ocha", meaning="tea", language_code="ja"),
        Word(script="ご飯", transliteration="gohan", meaning="rice/meal", language_code="ja"),
        
        # Daily Activities
        Word(script="起きる", transliteration="okiru", meaning="to wake up", language_code="ja"),
        Word(script="寝る", transliteration="neru", meaning="to sleep", language_code="ja"),
        Word(script="勉強する", transliteration="benkyou suru", meaning="to study", language_code="ja"),

        # French words
        # Core Verbs
        Word(script="manger", meaning="to eat", language_code="fr"),
        Word(script="boire", meaning="to drink", language_code="fr"),
        Word(script="parler", meaning="to speak", language_code="fr"),
        
        # Common Phrases
        Word(script="bonjour", meaning="good morning/hello", language_code="fr"),
        Word(script="merci", meaning="thank you", language_code="fr"),
        Word(script="s'il vous plaît", meaning="please", language_code="fr"),
        
        # Food & Drink
        Word(script="eau", meaning="water", language_code="fr"),
        Word(script="café", meaning="coffee", language_code="fr"),
        Word(script="pain", meaning="bread", language_code="fr"),
        
        # Daily Activities
        Word(script="se réveiller", meaning="to wake up", language_code="fr"),
        Word(script="dormir", meaning="to sleep", language_code="fr"),
        Word(script="étudier", meaning="to study", language_code="fr"),

        # Arabic words
        # Core Verbs
        Word(script="يأكل", transliteration="ya'kul", meaning="to eat", language_code="ar"),
        Word(script="يشرب", transliteration="yashrab", meaning="to drink", language_code="ar"),
        Word(script="يتكلم", transliteration="yatakallam", meaning="to speak", language_code="ar"),
        
        # Common Phrases
        Word(script="صباح الخير", transliteration="sabah al-khayr", meaning="good morning", language_code="ar"),
        Word(script="شكرا", transliteration="shukran", meaning="thank you", language_code="ar"),
        Word(script="من فضلك", transliteration="min fadlik", meaning="please", language_code="ar"),
        
        # Food & Drink
        Word(script="ماء", transliteration="maa'", meaning="water", language_code="ar"),
        Word(script="قهوة", transliteration="qahwa", meaning="coffee", language_code="ar"),
        Word(script="خبز", transliteration="khubz", meaning="bread", language_code="ar"),
        
        # Daily Activities
        Word(script="يستيقظ", transliteration="yastayqiz", meaning="to wake up", language_code="ar"),
        Word(script="ينام", transliteration="yanam", meaning="to sleep", language_code="ar"),
        Word(script="يدرس", transliteration="yadrus", meaning="to study", language_code="ar"),

        # Spanish words
        # Core Verbs
        Word(script="comer", meaning="to eat", language_code="es"),
        Word(script="beber", meaning="to drink", language_code="es"),
        Word(script="hablar", meaning="to speak", language_code="es"),
        
        # Common Phrases
        Word(script="buenos días", meaning="good morning", language_code="es"),
        Word(script="gracias", meaning="thank you", language_code="es"),
        Word(script="por favor", meaning="please", language_code="es"),
        
        # Food & Drink
        Word(script="agua", meaning="water", language_code="es"),
        Word(script="café", meaning="coffee", language_code="es"),
        Word(script="pan", meaning="bread", language_code="es"),
        
        # Daily Activities
        Word(script="despertar", meaning="to wake up", language_code="es"),
        Word(script="dormir", meaning="to sleep", language_code="es"),
        Word(script="estudiar", meaning="to study", language_code="es"),
    ]
    db.add_all(words)
    db.commit()
    return words

def seed_groups(db: Session):
    groups = [
        Group(name="Core Verbs"),
        Group(name="Common Phrases"),
        Group(name="Food & Drink"),
        Group(name="Movement"),
        Group(name="Communication"),
        Group(name="Daily Activities"),
    ]
    db.add_all(groups)
    db.commit()
    return groups

def seed_activities(db: Session):
    activities = [
        StudyActivity(name="Flashcards", url="/study/flashcards"),
        StudyActivity(name="Typing Practice", url="/study/typing"),
        StudyActivity(name="Multiple Choice", url="/study/quiz"),
    ]
    db.add_all(activities)
    db.commit()
    return activities

def seed_word_groups(db: Session, words: list, groups: list):
    # Get groups by name for easier reference
    core_verbs = groups[0]      # "Core Verbs"
    phrases = groups[1]         # "Common Phrases"
    food_drink = groups[2]      # "Food & Drink"
    movement = groups[3]        # "Movement"
    communication = groups[4]   # "Communication"
    daily = groups[5]          # "Daily Activities"
    
    for word in words:
        word_groups = set()  # Use set to avoid duplicates
        
        # Core Verbs
        if word.meaning.startswith("to "):
            word_groups.add(core_verbs)
        
        # Common Phrases
        if any(phrase in word.meaning for phrase in ["morning", "thank", "please", "excuse"]):
            word_groups.add(phrases)
        
        # Food & Drink
        if any(term in word.meaning for term in ["eat", "drink", "water", "coffee", "bread", "tea", "rice", "meal"]):
            word_groups.add(food_drink)
        
        # Communication
        if any(term in word.meaning for term in ["speak", "say", "tell", "ask"]):
            word_groups.add(communication)
        
        # Daily Activities
        if any(term in word.meaning for term in ["wake", "sleep", "study"]):
            word_groups.add(daily)
        
        # Add all groups to the word
        word.groups.extend(word_groups)
    
    db.commit()

def seed_all(db: Session):
    """Seed all tables with initial data"""
    try:
        reset_database(db.get_bind())  # Pass the engine from session
        
        # Seed in correct order (due to foreign keys)
        languages = seed_languages(db)
        words = seed_words(db)
        groups = seed_groups(db)
        activities = seed_activities(db)
        seed_word_groups(db, words, groups)
        
        db.commit()
        return {
            "languages": languages,
            "words": words,
            "groups": groups,
            "activities": activities
        }
    except Exception as e:
        db.rollback()
        raise Exception(f"Error seeding database: {str(e)}") 
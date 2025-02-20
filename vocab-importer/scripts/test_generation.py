"""Simple script to test vocabulary generation workflow."""
import os
import sys
from pathlib import Path
import json
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.vocab_generator import VocabGenerator
from utils.validators import validate_vocabulary_file

def print_word_details(entry: dict):
    """Print detailed information about a vocabulary entry."""
    print(f"\n- Word: {entry['script']}")
    print(f"  Transliteration: {entry['transliteration']}")
    print(f"  Meaning: {entry['meaning']}")
    print(f"  Part of Speech: {entry['part_of_speech']}")
    
    print("  Pronunciation Aid:")
    for unit in entry['pronunciation_aid']:
        readings = ", ".join(unit['readings'])
        print(f"    {unit['unit']}: {readings}")
    
    print("  Usage Examples:")
    for example in entry['usage_examples']:
        print(f"    • {example['script']}")
        print(f"      {example['meaning']}")
    
    print(f"  Notes: {entry['notes']}")

def print_summary(lang_name: str, category: str, results: dict):
    """Print a summary of the generated vocabulary."""
    print(f"\n✅ Generated {lang_name} {category}:")
    for entry in results["vocab_examples"][0]["vocab"]:
        print(f"- {entry['script']} ({entry['transliteration']}): {entry['meaning']}")

def run_automatic_tests(generator: VocabGenerator, show_details: bool = False):
    """Run automatic tests for predefined scenarios."""
    test_scenarios = [
        ("ja", "Verbs"),      # First set of Japanese verbs
        ("ar", "Nouns"),      # First set of Arabic nouns
        ("fr", "Adjectives"), # First set of French adjectives
        ("ja", "Verbs"),      # Second set of Japanese verbs (should merge)
        ("ar", "Nouns"),      # Second set of Arabic nouns (should merge)
        ("es", "Verbs"),      # Spanish verbs
        ("ja", "Verbs"),      # Third set of Japanese verbs (should merge)
        ("fr", "Adjectives")  # Second set of French adjectives (should merge)
    ]
    
    languages = {
        "ja": "Japanese",
        "fr": "French",
        "ar": "Arabic",
        "es": "Spanish"
    }
    
    print("\n🔄 Running automatic tests for multiple scenarios...")
    print("Note: Some scenarios are repeated to test merging functionality")
    
    for i, (lang_code, category) in enumerate(test_scenarios, 1):
        print(f"\n=== Test {i}: {languages[lang_code]} {category} ===")
        try:
            # Get previously used words
            used_words = generator.prompt_manager.get_used_words(
                language=lang_code,
                category=category,
                data_dir=str(generator.file_manager.data_dir)
            )
            
            # Get the prompt
            prompt = generator.prompt_manager.get_prompt(
                language=lang_code,
                category=category,
                num_words=3,
                used_words=used_words
            )
            
            if show_details:
                print("\n=== Prompt being sent to LLM ===")
                print(prompt)
                print("\n=== End of prompt ===")
            
            # Generate vocabulary
            print(f"Generating {languages[lang_code]} {category}...")
            results = generator.generate_vocabulary(
                language=lang_code,
                category=category,
                num_words=3,
                save_to_file=True
            )
            
            if show_details:
                print("\n=== Raw response from LLM ===")
                print(json.dumps(results, ensure_ascii=False, indent=2))
                print("\n=== End of response ===")
            
            # Show summary
            print_summary(languages[lang_code], category, results)
            
            # Show total words after potential merge
            file_path = generator.file_manager.get_category_file(lang_code, category)
            if file_path:
                stats = generator.file_manager.get_file_info(file_path)
                print(f"\nTotal words in {languages[lang_code]} {category}: {stats['word_count']}")
            
        except Exception as e:
            print(f"❌ Error in {languages[lang_code]} {category}: {str(e)}")
            continue

def main():
    """Run vocabulary generation tests."""
    # Load environment variables
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in .env file")
        return

    # Initialize generator
    templates_dir = project_root / "prompt_templates"
    data_dir = project_root / "data"
    generator = VocabGenerator(
        templates_dir=str(templates_dir),
        data_dir=str(data_dir)
    )

    # Ask for mode
    print("\nSelect mode:")
    print("1. Manual (single test)")
    print("2. Automatic (multiple scenarios)")
    mode = input("\nSelect mode (1-2): ").strip()

    if mode == "2":
        show_details = input("\nShow full prompts and responses? (y/N): ").strip().lower() == 'y'
        run_automatic_tests(generator, show_details)
        return

    # Manual mode
    # Available languages
    languages = {
        "1": ("ja", "Japanese"),
        "2": ("fr", "French"),
        "3": ("ar", "Arabic"),
        "4": ("es", "Spanish")
    }

    # Show language options
    print("\nAvailable languages:")
    for key, (code, name) in languages.items():
        print(f"{key}. {name}")
    
    # Get language choice
    choice = input("\nSelect language (1-4): ").strip()
    if choice not in languages:
        print("❌ Invalid choice")
        return
    
    lang_code, lang_name = languages[choice]
    
    # Get category
    category = input("\nEnter category (e.g., Adjectives, Verbs, Nouns): ").strip()
    if not category:
        print("❌ Category cannot be empty")
        return

    # Ask about showing prompt/response
    show_details = input("\nShow full prompt and response? (y/N): ").strip().lower() == 'y'

    print(f"\nGenerating {lang_name} vocabulary for category: {category}")
    
    try:
        # Get previously used words
        used_words = generator.prompt_manager.get_used_words(
            language=lang_code,
            category=category,
            data_dir=str(data_dir)
        )
        
        # Get the prompt first
        prompt = generator.prompt_manager.get_prompt(
            language=lang_code,
            category=category,
            num_words=3,
            used_words=used_words
        )
        
        if show_details:
            print("\n=== Prompt being sent to LLM ===")
            print(prompt)
            print("\n=== End of prompt ===")
        
        # Generate vocabulary
        print("\nSending request to LLM...")
        results = generator.generate_vocabulary(
            language=lang_code,
            category=category,
            num_words=3,
            save_to_file=True
        )
        
        if show_details:
            print("\n=== Raw response from LLM ===")
            print(json.dumps(results, ensure_ascii=False, indent=2))
            print("\n=== End of response ===")
        
        # Show results
        print("\n✅ Generation successful!")
        file_path = generator.file_manager.get_category_file(lang_code, category)
        print(f"Results saved to: {file_path}")
        print("\nGenerated words (detailed view):")
        
        for entry in results["vocab_examples"][0]["vocab"]:
            print_word_details(entry)
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 
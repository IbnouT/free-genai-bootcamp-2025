"""Prompt management utilities for vocabulary generation."""
from typing import List, Dict, Optional
from pathlib import Path
import json
from datetime import datetime

class PromptManager:
    """Manages prompt templates and word variety for vocabulary generation."""
    
    LANGUAGE_NAMES = {
        "ja": "Japanese",
        "fr": "French",
        "ar": "Arabic",
        "es": "Spanish"
    }
    
    TEMPLATE_FILES = {
        "ja": "japanese_template.md",
        "fr": "french_template.md",
        "ar": "arabic_template.md",
        "es": "spanish_template.md"
    }
    
    def __init__(self, templates_dir: str = "prompt_templates"):
        """
        Initialize the prompt manager.
        
        Args:
            templates_dir: Directory containing prompt templates
        """
        self.templates_dir = Path(templates_dir)
        self._load_templates()
    
    def _load_templates(self):
        """Load all template files."""
        self.base_template = self._read_template("base_template.md")
        self.language_templates = {
            lang: self._read_template(self.TEMPLATE_FILES[lang])
            for lang in self.LANGUAGE_NAMES.keys()
        }
    
    def _read_template(self, filename: str) -> str:
        """Read a template file."""
        with open(self.templates_dir / filename, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_used_words(self, language: str, category: str, data_dir: str = "data") -> List[str]:
        """
        Get list of words already used for a language and category.
        
        Args:
            language: Language code
            category: Word category
            data_dir: Directory containing vocabulary files
            
        Returns:
            List[str]: List of words already used
        """
        data_path = Path(data_dir) / f"{language}_{category.lower()}.json"
        if not data_path.exists():
            return []
            
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            words = []
            for group in data.get("vocab_examples", []):
                if group.get("language") == language and group.get("group").lower() == category.lower():
                    words.extend(entry.get("script", "") for entry in group.get("vocab", []))
            return [w for w in words if w]  # Filter out empty strings
            
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return []
    
    def format_previously_used_section(self, used_words: List[str]) -> str:
        """
        Format the section listing previously used words.
        
        Args:
            used_words: List of words to exclude
            
        Returns:
            str: Formatted section for the prompt
        """
        if not used_words:
            return ""
            
        return f"""
**Previously Used Words:**
The following words have already been used and should NOT be generated again:
{', '.join(f'`{word}`' for word in used_words)}

"""
    
    def get_prompt(
        self,
        language: str,
        category: str,
        num_words: int = 10,
        used_words: Optional[List[str]] = None
    ) -> str:
        """
        Generate a complete prompt for vocabulary generation.
        
        Args:
            language: Language code (ja, fr, ar, es)
            category: Word category (e.g., "Adjectives")
            num_words: Number of words to generate
            used_words: Optional list of words to exclude
            
        Returns:
            str: Complete prompt for the LLM
            
        Raises:
            ValueError: If language is not supported
        """
        if language not in self.LANGUAGE_NAMES:
            raise ValueError(f"Unsupported language: {language}")
            
        # Get language-specific template
        language_specific = self.language_templates.get(language, "")
        
        # Format the previously used words section
        previously_used_section = self.format_previously_used_section(used_words or [])
        
        # Replace template variables
        prompt = self.base_template.replace(
            "${language_name}", self.LANGUAGE_NAMES[language]
        ).replace(
            "${language_code}", language
        ).replace(
            "${category}", category
        ).replace(
            "${num_words}", str(num_words)
        ).replace(
            "${previously_used_words_section}", previously_used_section
        ).replace(
            "${language_specific_instructions}", language_specific
        )
        
        return prompt
    
    def get_semantic_categories(self, category: str) -> List[str]:
        """
        Get semantic sub-categories for a word category to encourage diversity.
        
        Args:
            category: Main word category
            
        Returns:
            List[str]: List of semantic sub-categories
        """
        # This could be expanded based on the category
        categories = {
            "Adjectives": [
                "Physical Qualities",
                "Personality Traits",
                "Emotions",
                "Size and Dimensions",
                "Colors and Appearances",
                "Time and Age",
                "Difficulty Levels",
                "Temperature",
                "Weather Related",
                "Taste and Smell",
                "Sound Related",
                "Value and Worth",
                "Speed and Pace",
                "Distance and Space",
                "Quantity and Amount"
            ]
        }
        return categories.get(category, []) 
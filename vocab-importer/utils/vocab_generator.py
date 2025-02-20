"""Vocabulary generation using LLM and prompt management."""
from typing import Dict, List, Optional
import os
from datetime import datetime

from .prompt_manager import PromptManager
from .llm_client import create_llm_client, LLMError
from .validators import validate_vocabulary_file
from .file_manager import VocabFileManager

class VocabGeneratorError(Exception):
    """Base exception for vocabulary generation errors."""
    pass

class VocabGenerator:
    """Manages vocabulary generation using LLM and prompt templates."""
    
    def __init__(
        self,
        llm_provider: Optional[str] = None,
        templates_dir: str = "prompt_templates",
        data_dir: str = "data"
    ):
        """
        Initialize the vocabulary generator.
        
        Args:
            llm_provider: Optional LLM provider to use (groq, openai, gemini)
            templates_dir: Directory containing prompt templates
            data_dir: Directory for storing vocabulary files
        """
        try:
            self.prompt_manager = PromptManager(templates_dir)
            self.llm_client = create_llm_client(llm_provider)
            self.file_manager = VocabFileManager(data_dir)
        except Exception as e:
            raise VocabGeneratorError(f"Failed to initialize generator: {str(e)}")
    
    def generate_vocabulary(
        self,
        language: str,
        category: str,
        num_words: int = 5,
        save_to_file: bool = True
    ) -> Dict:
        """
        Generate vocabulary entries using LLM.
        
        Args:
            language: Language code (ja, fr, ar, es)
            category: Word category (e.g., "Adjectives")
            num_words: Number of words to generate
            save_to_file: Whether to save the generated words
            
        Returns:
            Dict: The generated vocabulary data
            
        Raises:
            VocabGeneratorError: If generation fails
        """
        try:
            # Get previously used words
            used_words = self.prompt_manager.get_used_words(
                language=language,
                category=category,
                data_dir=self.file_manager.data_dir
            )
            
            # Generate prompt with used words excluded
            prompt = self.prompt_manager.get_prompt(
                language=language,
                category=category,
                num_words=num_words,
                used_words=used_words
            )
            
            # Generate vocabulary using LLM
            response = self.llm_client.generate_vocabulary(prompt)
            
            # Validate response
            validate_vocabulary_file(response)
            
            # Save to file if requested
            if save_to_file:
                self.file_manager.save_vocab_data(
                    language=language,
                    category=category,
                    data=response
                )
            
            return response
            
        except Exception as e:
            raise VocabGeneratorError(f"Vocabulary generation failed: {str(e)}")
    
    def get_generation_stats(self, language: str, category: str) -> Dict:
        """
        Get statistics about generated vocabulary.
        
        Args:
            language: Language code
            category: Word category
            
        Returns:
            Dict: Statistics about the vocabulary
        """
        try:
            file_path = self.file_manager.get_category_file(language, category)
            if not file_path:
                return {
                    "total_words": 0,
                    "last_generated": None,
                    "file_exists": False
                }
            
            file_info = self.file_manager.get_file_info(file_path)
            return {
                "total_words": file_info["word_count"],
                "last_generated": file_info["modified"],
                "file_exists": True,
                "file_size": file_info["size"]
            }
            
        except Exception as e:
            raise VocabGeneratorError(f"Failed to get generation stats: {str(e)}")
    
    def get_available_categories(self, language: str) -> List[str]:
        """
        Get list of available categories for a language.
        
        Args:
            language: Language code
            
        Returns:
            List[str]: List of available categories
        """
        try:
            return self.file_manager.list_categories(language)
        except Exception as e:
            raise VocabGeneratorError(f"Failed to get categories: {str(e)}")
    
    def backup_vocabulary(self, language: str, category: str) -> Optional[str]:
        """
        Create a backup of vocabulary data.
        
        Args:
            language: Language code
            category: Word category
            
        Returns:
            Optional[str]: Path to backup file if created
        """
        try:
            backup_path = self.file_manager.backup_file(language, category)
            return str(backup_path) if backup_path else None
        except Exception as e:
            raise VocabGeneratorError(f"Failed to create backup: {str(e)}") 
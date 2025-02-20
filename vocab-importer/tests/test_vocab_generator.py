"""Tests for vocabulary generation functionality."""
import json
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
from pathlib import Path

from utils.vocab_generator import VocabGenerator, VocabGeneratorError

# Sample test data
SAMPLE_VOCAB_DATA = {
    "vocab_examples": [
        {
            "language": "ja",
            "group": "Adjectives",
            "generated_at": "2025-02-18T12:00:00Z",
            "vocab": [
                {
                    "script": "新しい",
                    "transliteration": "atarashii",
                    "pronunciation_aid": [
                        {
                            "unit": "新",
                            "readings": ["a", "ta", "ra"]
                        },
                        {
                            "unit": "しい",
                            "readings": ["shi", "i"]
                        }
                    ],
                    "meaning": "new",
                    "part_of_speech": "adjective",
                    "usage_examples": [
                        {
                            "script": "新しい本を買った。",
                            "meaning": "I bought a new book."
                        }
                    ],
                    "notes": "Common adjective"
                }
            ]
        }
    ]
}

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("GROQ_API_KEY", "mock-groq-key")
    monkeypatch.setenv("LLM_PROVIDER", "groq")

@pytest.fixture
def mock_prompt_manager():
    """Create a mock PromptManager."""
    with patch("utils.vocab_generator.PromptManager") as mock_cls:
        instance = mock_cls.return_value
        instance.get_prompt.return_value = "Test prompt"
        instance.get_used_words.return_value = []
        yield instance

@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client."""
    with patch("utils.vocab_generator.create_llm_client") as mock:
        instance = mock.return_value
        instance.generate_vocabulary.return_value = SAMPLE_VOCAB_DATA
        yield instance

@pytest.fixture
def mock_file_manager():
    """Create a mock FileManager."""
    with patch("utils.vocab_generator.VocabFileManager") as mock_cls:
        instance = mock_cls.return_value
        instance.data_dir = "mock_data_dir"
        instance.get_category_file.return_value = None
        instance.get_file_info.return_value = {
            "word_count": 5,
            "modified": datetime.now(),
            "size": 1024,
            "filename": "mock_file.json"
        }
        instance.list_categories.return_value = ["adjectives", "verbs"]
        instance.backup_file.return_value = Path("mock_backup.json")
        yield instance

@pytest.fixture
def generator(mock_prompt_manager, mock_llm_client, mock_file_manager):
    """Create a VocabGenerator instance with mocked dependencies."""
    return VocabGenerator(
        templates_dir="mock_templates_dir",
        data_dir="mock_data_dir"
    )

def test_generate_vocabulary(generator, mock_llm_client, mock_prompt_manager):
    """Test vocabulary generation."""
    result = generator.generate_vocabulary(
        language="ja",
        category="Adjectives",
        num_words=5
    )
    
    assert result == SAMPLE_VOCAB_DATA
    mock_prompt_manager.get_prompt.assert_called_once()
    mock_llm_client.generate_vocabulary.assert_called_once_with("Test prompt")

def test_generate_vocabulary_no_save(generator, mock_llm_client, mock_file_manager):
    """Test vocabulary generation without saving."""
    result = generator.generate_vocabulary(
        language="ja",
        category="Adjectives",
        num_words=5,
        save_to_file=False
    )
    
    assert result == SAMPLE_VOCAB_DATA
    mock_file_manager.save_vocab_data.assert_not_called()

def test_generate_vocabulary_with_used_words(generator, mock_prompt_manager, mock_llm_client):
    """Test vocabulary generation with used words exclusion."""
    mock_prompt_manager.get_used_words.return_value = ["古い", "新しい"]
    
    generator.generate_vocabulary("ja", "Adjectives")
    
    mock_prompt_manager.get_used_words.assert_called_once()
    mock_prompt_manager.get_prompt.assert_called_once()
    mock_llm_client.generate_vocabulary.assert_called_once()

def test_get_generation_stats_no_file(generator, mock_file_manager):
    """Test getting stats when no file exists."""
    mock_file_manager.get_category_file.return_value = None
    
    stats = generator.get_generation_stats("ja", "Adjectives")
    assert stats["total_words"] == 0
    assert stats["last_generated"] is None
    assert not stats["file_exists"]

def test_get_generation_stats_with_file(generator, mock_file_manager):
    """Test getting stats when file exists."""
    mock_file_info = {
        "word_count": 5,
        "modified": datetime.now(),
        "size": 1024,
        "filename": "ja_adjectives.json"
    }
    mock_file_manager.get_category_file.return_value = Path("mock_file.json")
    mock_file_manager.get_file_info.return_value = mock_file_info
    
    stats = generator.get_generation_stats("ja", "Adjectives")
    assert stats["total_words"] == 5
    assert stats["last_generated"] is not None
    assert stats["file_exists"]
    assert stats["file_size"] == 1024

def test_get_available_categories(generator, mock_file_manager):
    """Test getting available categories."""
    categories = generator.get_available_categories("ja")
    assert set(categories) == {"adjectives", "verbs"}
    mock_file_manager.list_categories.assert_called_once_with("ja")

def test_get_available_categories_error(generator, mock_file_manager):
    """Test error handling in category retrieval."""
    mock_file_manager.list_categories.side_effect = Exception("Test error")
    
    with pytest.raises(VocabGeneratorError, match="Failed to get categories"):
        generator.get_available_categories("ja")

def test_backup_vocabulary(generator, mock_file_manager):
    """Test creating vocabulary backup."""
    backup_path = generator.backup_vocabulary("ja", "Adjectives")
    assert backup_path == str(Path("mock_backup.json"))
    mock_file_manager.backup_file.assert_called_once_with("ja", "Adjectives")

def test_backup_vocabulary_no_file(generator, mock_file_manager):
    """Test backup when file doesn't exist."""
    mock_file_manager.backup_file.return_value = None
    
    backup_path = generator.backup_vocabulary("ja", "NonexistentCategory")
    assert backup_path is None
    mock_file_manager.backup_file.assert_called_once_with("ja", "NonexistentCategory")

def test_initialization_error():
    """Test error handling during initialization."""
    with patch("utils.vocab_generator.PromptManager", side_effect=Exception("Test error")):
        with pytest.raises(VocabGeneratorError, match="Failed to initialize generator"):
            VocabGenerator(templates_dir="mock_dir")

def test_generate_vocabulary_validation_error(generator, mock_prompt_manager, mock_llm_client):
    """Test error handling for invalid LLM response."""
    mock_llm_client.generate_vocabulary.return_value = {"invalid": "response"}
    
    with pytest.raises(VocabGeneratorError, match="Vocabulary generation failed"):
        generator.generate_vocabulary("ja", "Adjectives")

def test_get_generation_stats_error(generator, mock_file_manager):
    """Test error handling in stats retrieval."""
    mock_file_manager.get_file_info.side_effect = Exception("Test error")
    mock_file_manager.get_category_file.return_value = Path("mock_file.json")
    
    with pytest.raises(VocabGeneratorError, match="Failed to get generation stats"):
        generator.get_generation_stats("ja", "Adjectives") 
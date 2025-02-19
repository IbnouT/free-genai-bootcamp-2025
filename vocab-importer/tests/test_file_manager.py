"""Tests for file management utilities."""
import pytest
import shutil
from datetime import datetime
from pathlib import Path
from utils.file_manager import (
    create_vocab_filename,
    VocabFileManager,
    FileManagerError
)

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
                    "notes": "Describes something that is new or recent."
                }
            ]
        }
    ]
}

# Additional test data with different word
ADDITIONAL_VOCAB_DATA = {
    "vocab_examples": [
        {
            "language": "ja",
            "group": "Adjectives",
            "generated_at": "2025-02-18T12:00:00Z",
            "vocab": [
                {
                    "script": "古い",
                    "transliteration": "furui",
                    "pronunciation_aid": [
                        {
                            "unit": "古",
                            "readings": ["fu", "ru"]
                        },
                        {
                            "unit": "い",
                            "readings": ["i"]
                        }
                    ],
                    "meaning": "old",
                    "part_of_speech": "adjective",
                    "usage_examples": [
                        {
                            "script": "この家は古い。",
                            "meaning": "This house is old."
                        }
                    ],
                    "notes": "Describes something aged."
                }
            ]
        }
    ]
}

@pytest.fixture
def file_manager(tmp_path):
    """Create a file manager instance with a temporary directory."""
    return VocabFileManager(data_dir=str(tmp_path))

def test_create_vocab_filename():
    """Test vocabulary filename creation."""
    filename = create_vocab_filename(
        language="ja",
        category="Adjectives"
    )
    assert filename == "ja_adjectives.json"
    
    # Test category name sanitization
    filename = create_vocab_filename(
        language="fr",
        category="Common Phrases"
    )
    assert filename == "fr_common_phrases.json"

def test_file_manager_initialization(tmp_path):
    """Test file manager initialization."""
    manager = VocabFileManager(data_dir=str(tmp_path))
    assert manager.data_dir.exists()
    assert manager.data_dir.is_dir()

def test_save_and_get_vocab_data(file_manager):
    """Test saving and retrieving vocabulary data."""
    # Save initial data
    file_path = file_manager.save_vocab_data(
        language="ja",
        category="Adjectives",
        data=SAMPLE_VOCAB_DATA
    )
    
    assert file_path.exists()
    assert file_path.suffix == ".json"
    assert file_path.stem == "ja_adjectives"
    
    # Get the file
    retrieved_path = file_manager.get_category_file("ja", "Adjectives")
    assert retrieved_path == file_path

def test_merge_vocab_data(file_manager):
    """Test merging vocabulary data."""
    # Save initial data
    file_manager.save_vocab_data(
        "ja", "Adjectives", SAMPLE_VOCAB_DATA
    )
    
    # Save additional data (should merge)
    file_manager.save_vocab_data(
        "ja", "Adjectives", ADDITIONAL_VOCAB_DATA
    )
    
    # Verify merged data
    file_path = file_manager.get_category_file("ja", "Adjectives")
    from utils.vocab_file import load_vocab_file
    merged_data = load_vocab_file(str(file_path))
    
    # Should have one group with two words
    assert len(merged_data["vocab_examples"]) == 1
    assert len(merged_data["vocab_examples"][0]["vocab"]) == 2

def test_list_categories(file_manager):
    """Test listing available categories."""
    # Create files for different categories
    file_manager.save_vocab_data(
        "ja", "Adjectives", SAMPLE_VOCAB_DATA
    )
    file_manager.save_vocab_data(
        "ja", "Verbs", SAMPLE_VOCAB_DATA
    )
    file_manager.save_vocab_data(
        "fr", "Adjectives", SAMPLE_VOCAB_DATA
    )
    
    # Test listing all categories
    all_categories = file_manager.list_categories()
    assert set(all_categories) == {"adjectives", "verbs"}
    
    # Test listing categories for a specific language
    ja_categories = file_manager.list_categories(language="ja")
    assert set(ja_categories) == {"adjectives", "verbs"}
    
    fr_categories = file_manager.list_categories(language="fr")
    assert set(fr_categories) == {"adjectives"}

def test_get_file_info(file_manager):
    """Test getting file information."""
    file_path = file_manager.save_vocab_data(
        "ja", "Adjectives", SAMPLE_VOCAB_DATA
    )
    
    info = file_manager.get_file_info(file_path)
    assert "filename" in info
    assert "modified" in info
    assert "size" in info
    assert "word_count" in info
    assert info["word_count"] == 1  # One word in our sample data

def test_backup_file(file_manager):
    """Test creating backup of a vocabulary file."""
    # Create original file
    file_manager.save_vocab_data(
        "ja", "Adjectives", SAMPLE_VOCAB_DATA
    )
    
    # Create backup
    backup_path = file_manager.backup_file("ja", "Adjectives")
    
    assert backup_path.exists()
    assert backup_path.parent.name == "backups"
    assert "backup" in backup_path.name
    assert backup_path.suffix == ".json"
    
    # Verify backup contents
    from utils.vocab_file import load_vocab_file
    original_path = file_manager.get_category_file("ja", "Adjectives")
    original_data = load_vocab_file(str(original_path))
    backup_data = load_vocab_file(str(backup_path))
    assert original_data == backup_data

def test_backup_nonexistent_file(file_manager):
    """Test attempting to backup a nonexistent file."""
    backup_path = file_manager.backup_file("ja", "NonexistentCategory")
    assert backup_path is None 
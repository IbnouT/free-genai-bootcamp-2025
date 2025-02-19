"""Tests for vocabulary file utilities."""
import pytest
import json
import os
from datetime import datetime
from utils.vocab_file import (
    load_vocab_file,
    save_vocab_file,
    create_vocab_group,
    merge_vocab_files,
    VocabFileError
)

# Sample test data
SAMPLE_VOCAB_ENTRY = {
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

@pytest.fixture
def temp_vocab_file(tmp_path):
    """Create a temporary vocabulary file for testing."""
    file_path = tmp_path / "test_vocab.json"
    vocab_data = {
        "vocab_examples": [
            {
                "language": "ja",
                "group": "Adjectives",
                "generated_at": "2025-02-18T12:00:00Z",
                "vocab": [SAMPLE_VOCAB_ENTRY]
            }
        ]
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False)
    return file_path

def test_load_vocab_file(temp_vocab_file):
    """Test loading a vocabulary file."""
    data = load_vocab_file(temp_vocab_file)
    assert "vocab_examples" in data
    assert len(data["vocab_examples"]) == 1
    assert data["vocab_examples"][0]["language"] == "ja"

def test_load_vocab_file_invalid_json(tmp_path):
    """Test loading an invalid JSON file."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w') as f:
        f.write("invalid json")
    
    with pytest.raises(VocabFileError):
        load_vocab_file(file_path)

def test_save_vocab_file(tmp_path):
    """Test saving a vocabulary file."""
    file_path = tmp_path / "output.json"
    vocab_data = {
        "vocab_examples": [
            {
                "language": "ja",
                "group": "Adjectives",
                "generated_at": "2025-02-18T12:00:00Z",
                "vocab": [SAMPLE_VOCAB_ENTRY]
            }
        ]
    }
    
    save_vocab_file(vocab_data, file_path)
    assert os.path.exists(file_path)
    
    # Verify the saved data
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data == vocab_data

def test_create_vocab_group():
    """Test creating a vocabulary group."""
    group = create_vocab_group(
        language="ja",
        group="Adjectives",
        vocab=[SAMPLE_VOCAB_ENTRY]
    )
    
    assert group["language"] == "ja"
    assert group["group"] == "Adjectives"
    assert len(group["vocab"]) == 1
    assert "generated_at" in group

def test_create_vocab_group_invalid():
    """Test creating an invalid vocabulary group."""
    with pytest.raises(VocabFileError):
        create_vocab_group(
            language="invalid",  # Invalid language code
            group="Adjectives",
            vocab=[SAMPLE_VOCAB_ENTRY]
        )

def test_merge_vocab_files():
    """Test merging vocabulary files."""
    file1_data = {
        "vocab_examples": [
            {
                "language": "ja",
                "group": "Adjectives",
                "generated_at": "2025-02-18T12:00:00Z",
                "vocab": [SAMPLE_VOCAB_ENTRY]
            }
        ]
    }
    
    file2_data = {
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
    
    merged = merge_vocab_files(file1_data, file2_data)
    assert len(merged["vocab_examples"]) == 1
    assert len(merged["vocab_examples"][0]["vocab"]) == 2 
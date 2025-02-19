"""Tests for JSON schema validation utilities."""
import pytest
import json
from datetime import datetime
from jsonschema.exceptions import ValidationError
from utils.validators import (
    validate_vocabulary_file,
    validate_vocabulary_entry,
    validate_vocabulary_group
)

# Sample valid data for testing
VALID_ENTRY = {
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

VALID_GROUP = {
    "language": "ja",
    "group": "Adjectives",
    "generated_at": "2025-02-18T12:00:00Z",
    "vocab": [VALID_ENTRY]
}

VALID_FILE = {
    "vocab_examples": [VALID_GROUP]
}

def test_validate_vocabulary_entry():
    """Test validation of a single vocabulary entry."""
    assert validate_vocabulary_entry(VALID_ENTRY) is True

    # Test invalid entry (missing required field)
    invalid_entry = VALID_ENTRY.copy()
    del invalid_entry["script"]
    with pytest.raises(ValidationError):
        validate_vocabulary_entry(invalid_entry)

def test_validate_vocabulary_group():
    """Test validation of a vocabulary group."""
    assert validate_vocabulary_group(VALID_GROUP) is True

    # Test invalid group (invalid language)
    invalid_group = VALID_GROUP.copy()
    invalid_group["language"] = "invalid"
    with pytest.raises(ValidationError):
        validate_vocabulary_group(invalid_group)

def test_validate_vocabulary_file():
    """Test validation of a complete vocabulary file."""
    assert validate_vocabulary_file(VALID_FILE) is True

    # Test invalid file (empty vocab_examples)
    invalid_file = VALID_FILE.copy()
    invalid_file["vocab_examples"] = []
    with pytest.raises(ValidationError):
        validate_vocabulary_file(invalid_file)

def test_pronunciation_aid_validation():
    """Test validation of pronunciation aid structure."""
    entry = VALID_ENTRY.copy()
    entry["pronunciation_aid"] = [{"unit": "新", "readings": []}]  # Empty readings
    with pytest.raises(ValidationError):
        validate_vocabulary_entry(entry)

def test_usage_examples_validation():
    """Test validation of usage examples structure."""
    entry = VALID_ENTRY.copy()
    entry["usage_examples"] = []  # Empty usage examples
    with pytest.raises(ValidationError):
        validate_vocabulary_entry(entry)

def test_notes_validation():
    """Test validation of notes field."""
    entry = VALID_ENTRY.copy()
    entry["notes"] = ""  # Empty notes
    with pytest.raises(ValidationError):
        validate_vocabulary_entry(entry) 
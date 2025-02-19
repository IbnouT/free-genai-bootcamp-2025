"""JSON schema validation utilities for vocabulary data."""
from typing import Dict, List, Union
import jsonschema
from jsonschema import validate

# JSON Schema for pronunciation aid
PRONUNCIATION_AID_SCHEMA = {
    "type": "object",
    "required": ["unit", "readings"],
    "properties": {
        "unit": {"type": "string"},
        "readings": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        }
    }
}

# JSON Schema for usage examples
USAGE_EXAMPLE_SCHEMA = {
    "type": "object",
    "required": ["script", "meaning"],
    "properties": {
        "script": {"type": "string"},
        "meaning": {"type": "string"}
    }
}

# JSON Schema for individual vocabulary entries
VOCABULARY_ENTRY_SCHEMA = {
    "type": "object",
    "required": [
        "script",
        "transliteration",
        "pronunciation_aid",
        "meaning",
        "part_of_speech",
        "usage_examples",
        "notes"
    ],
    "properties": {
        "script": {"type": "string"},
        "transliteration": {"type": "string"},
        "pronunciation_aid": {
            "type": "array",
            "items": PRONUNCIATION_AID_SCHEMA,
            "minItems": 1
        },
        "meaning": {"type": "string"},
        "part_of_speech": {"type": "string"},
        "usage_examples": {
            "type": "array",
            "items": USAGE_EXAMPLE_SCHEMA,
            "minItems": 1
        },
        "notes": {
            "type": "string",
            "minLength": 1
        }
    }
}

# JSON Schema for vocabulary group
VOCABULARY_GROUP_SCHEMA = {
    "type": "object",
    "required": ["language", "group", "generated_at", "vocab"],
    "properties": {
        "language": {
            "type": "string",
            "enum": ["ja", "fr", "ar", "es"]
        },
        "group": {"type": "string"},
        "generated_at": {
            "type": "string",
            "format": "date-time"
        },
        "vocab": {
            "type": "array",
            "items": VOCABULARY_ENTRY_SCHEMA,
            "minItems": 1
        }
    }
}

# Complete schema for vocabulary file
VOCAB_FILE_SCHEMA = {
    "type": "object",
    "required": ["vocab_examples"],
    "properties": {
        "vocab_examples": {
            "type": "array",
            "items": VOCABULARY_GROUP_SCHEMA,
            "minItems": 1
        }
    }
}

def validate_vocabulary_file(data: Dict) -> bool:
    """
    Validate a complete vocabulary file against the schema.
    
    Args:
        data: Dictionary containing the vocabulary data
        
    Returns:
        bool: True if validation passes
        
    Raises:
        jsonschema.exceptions.ValidationError: If validation fails
    """
    validate(instance=data, schema=VOCAB_FILE_SCHEMA)
    return True

def validate_vocabulary_entry(entry: Dict) -> bool:
    """
    Validate a single vocabulary entry against the schema.
    
    Args:
        entry: Dictionary containing a single vocabulary entry
        
    Returns:
        bool: True if validation passes
        
    Raises:
        jsonschema.exceptions.ValidationError: If validation fails
    """
    validate(instance=entry, schema=VOCABULARY_ENTRY_SCHEMA)
    return True

def validate_vocabulary_group(group: Dict) -> bool:
    """
    Validate a vocabulary group against the schema.
    
    Args:
        group: Dictionary containing a vocabulary group
        
    Returns:
        bool: True if validation passes
        
    Raises:
        jsonschema.exceptions.ValidationError: If validation fails
    """
    validate(instance=group, schema=VOCABULARY_GROUP_SCHEMA)
    return True 
"""Utilities for working with vocabulary files."""
import json
from typing import Dict, List, Optional
from datetime import datetime
from .validators import (
    validate_vocabulary_file,
    validate_vocabulary_entry,
    validate_vocabulary_group
)

class VocabFileError(Exception):
    """Base exception for vocabulary file operations."""
    pass

def load_vocab_file(file_path: str) -> Dict:
    """
    Load and validate a vocabulary file.
    
    Args:
        file_path: Path to the vocabulary file
        
    Returns:
        Dict: The validated vocabulary data
        
    Raises:
        VocabFileError: If file cannot be read or validation fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        validate_vocabulary_file(data)
        return data
    except json.JSONDecodeError as e:
        raise VocabFileError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise VocabFileError(f"Error loading vocabulary file: {str(e)}")

def save_vocab_file(data: Dict, file_path: str) -> None:
    """
    Validate and save vocabulary data to a file.
    
    Args:
        data: The vocabulary data to save
        file_path: Path where to save the file
        
    Raises:
        VocabFileError: If validation fails or file cannot be written
    """
    try:
        validate_vocabulary_file(data)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise VocabFileError(f"Error saving vocabulary file: {str(e)}")

def create_vocab_group(
    language: str,
    group: str,
    vocab: List[Dict],
    generated_at: Optional[str] = None
) -> Dict:
    """
    Create a new vocabulary group with validation.
    
    Args:
        language: Language code (ja, fr, ar, es)
        group: Group name
        vocab: List of vocabulary entries
        generated_at: Optional timestamp (ISO format)
        
    Returns:
        Dict: A validated vocabulary group
        
    Raises:
        VocabFileError: If validation fails
    """
    if generated_at is None:
        generated_at = datetime.utcnow().isoformat() + "Z"
    
    group_data = {
        "language": language,
        "group": group,
        "generated_at": generated_at,
        "vocab": vocab
    }
    
    try:
        validate_vocabulary_group(group_data)
        return group_data
    except Exception as e:
        raise VocabFileError(f"Error creating vocabulary group: {str(e)}")

def merge_vocab_files(file1_data: Dict, file2_data: Dict) -> Dict:
    """
    Merge two vocabulary files, avoiding duplicates.
    
    Args:
        file1_data: First vocabulary file data
        file2_data: Second vocabulary file data
        
    Returns:
        Dict: Merged vocabulary data
        
    Raises:
        VocabFileError: If validation fails
    """
    try:
        validate_vocabulary_file(file1_data)
        validate_vocabulary_file(file2_data)
        
        # Create a set of tuples for easy comparison
        existing_entries = set()
        merged_groups = []
        
        # Process all groups from both files
        all_groups = (file1_data["vocab_examples"] + 
                     file2_data["vocab_examples"])
        
        for group in all_groups:
            # Create a key for the group
            group_key = (group["language"], group["group"])
            
            if group_key not in existing_entries:
                existing_entries.add(group_key)
                merged_groups.append(group)
            else:
                # Merge vocab entries for existing group
                existing_group = next(
                    g for g in merged_groups 
                    if (g["language"], g["group"]) == group_key
                )
                
                # Add only new vocab entries
                existing_scripts = {v["script"] for v in existing_group["vocab"]}
                new_entries = [
                    v for v in group["vocab"] 
                    if v["script"] not in existing_scripts
                ]
                
                existing_group["vocab"].extend(new_entries)
        
        merged_data = {"vocab_examples": merged_groups}
        validate_vocabulary_file(merged_data)
        return merged_data
        
    except Exception as e:
        raise VocabFileError(f"Error merging vocabulary files: {str(e)}") 
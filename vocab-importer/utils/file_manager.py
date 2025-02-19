"""File management utilities for vocabulary files."""
import os
import random
import string
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path

from .vocab_file import load_vocab_file, save_vocab_file, VocabFileError, merge_vocab_files

class FileManagerError(Exception):
    """Base exception for file management operations."""
    pass

def generate_random_suffix(length: int = 4) -> str:
    """Generate a random alphanumeric suffix for filenames."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_vocab_filename(language: str, category: str) -> str:
    """
    Create a filename following the convention: [language]_[category].json
    
    Args:
        language: Language code (ja, fr, ar, es)
        category: Category name
        
    Returns:
        str: The formatted filename
    """
    # Sanitize category name for filesystem
    category = category.replace(' ', '_').lower()
    return f"{language}_{category}.json"

class VocabFileManager:
    """Manager for vocabulary file operations."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the file manager.
        
        Args:
            data_dir: Directory for storing vocabulary files
        """
        self.data_dir = Path(data_dir)
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_category_file(self, language: str, category: str) -> Optional[Path]:
        """
        Get the file path for a given language and category.
        
        Args:
            language: Language code
            category: Category name
            
        Returns:
            Optional[Path]: Path to the file if it exists, None otherwise
        """
        filename = create_vocab_filename(language, category)
        file_path = self.data_dir / filename
        return file_path if file_path.exists() else None
    
    def save_vocab_data(self, language: str, category: str, data: Dict) -> Path:
        """
        Save vocabulary data, merging with existing data if present.
        
        Args:
            language: Language code
            category: Category name
            data: Vocabulary data to save
            
        Returns:
            Path: Path to the saved file
            
        Raises:
            FileManagerError: If file operations fail
        """
        try:
            file_path = self.data_dir / create_vocab_filename(language, category)
            
            if file_path.exists():
                # Load and merge with existing data
                existing_data = load_vocab_file(str(file_path))
                data = merge_vocab_files(existing_data, data)
            
            save_vocab_file(data, str(file_path))
            return file_path
            
        except (VocabFileError, Exception) as e:
            raise FileManagerError(f"Error saving vocabulary data: {str(e)}")
    
    def list_categories(self, language: Optional[str] = None) -> List[str]:
        """
        List all available categories.
        
        Args:
            language: Optional language code to filter by
            
        Returns:
            List[str]: List of unique categories
        """
        pattern = f"{language}_*.json" if language else "*.json"
        files = self.data_dir.glob(pattern)
        
        categories = set()
        for file in files:
            # Extract category from filename
            parts = file.stem.split('_')
            if len(parts) >= 2:
                categories.add(parts[1])
        
        return sorted(categories)
    
    def get_file_info(self, file_path: Path) -> Dict:
        """
        Get information about a vocabulary file.
        
        Args:
            file_path: Path to the vocabulary file
            
        Returns:
            Dict: File information including stats
        """
        try:
            data = load_vocab_file(str(file_path))
            stats = {
                'filename': file_path.name,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                'size': file_path.stat().st_size,
                'word_count': sum(len(group['vocab']) 
                                for group in data['vocab_examples'])
            }
            return stats
        except Exception as e:
            raise FileManagerError(f"Error getting file info: {str(e)}")
    
    def backup_file(self, language: str, category: str) -> Optional[Path]:
        """
        Create a backup of a vocabulary file before significant changes.
        
        Args:
            language: Language code
            category: Category name
            
        Returns:
            Optional[Path]: Path to backup file if created, None if source doesn't exist
        """
        source_path = self.get_category_file(language, category)
        if not source_path:
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
        backup_path = self.data_dir / "backups" / backup_name
        
        # Ensure backups directory exists
        os.makedirs(backup_path.parent, exist_ok=True)
        
        # Copy file to backup
        import shutil
        shutil.copy2(source_path, backup_path)
        return backup_path 
"""Tests for prompt management utilities."""
import pytest
from pathlib import Path
import json
from utils.prompt_manager import PromptManager

@pytest.fixture
def prompt_manager(tmp_path):
    """Create a prompt manager with temporary templates."""
    templates_dir = tmp_path / "prompt_templates"
    templates_dir.mkdir()
    
    # Create base template
    base_template = """
    ${language_name} Template
    Category: ${category}
    Words: ${num_words}
    Language: ${language_code}
    ${previously_used_words_section}
    ${language_specific_instructions}
    """
    (templates_dir / "base_template.md").write_text(base_template)
    
    # Create language templates
    for lang in ["ja", "fr", "ar", "es"]:
        (templates_dir / f"{lang}_template.md").write_text(
            f"Instructions for {lang}"
        )
    
    return PromptManager(str(templates_dir))

@pytest.fixture
def sample_vocab_data(tmp_path):
    """Create sample vocabulary data file."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    vocab_data = {
        "vocab_examples": [
            {
                "language": "ja",
                "group": "Adjectives",
                "generated_at": "2025-02-18T12:00:00Z",
                "vocab": [
                    {"script": "新しい"},
                    {"script": "古い"}
                ]
            }
        ]
    }
    
    file_path = data_dir / "ja_adjectives.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, ensure_ascii=False)
    
    return str(data_dir)

def test_prompt_manager_initialization(prompt_manager):
    """Test prompt manager initialization."""
    assert prompt_manager.base_template
    assert len(prompt_manager.language_templates) == 4
    assert all(lang in prompt_manager.language_templates 
              for lang in ["ja", "fr", "ar", "es"])

def test_get_used_words(prompt_manager, sample_vocab_data):
    """Test retrieving used words from vocabulary file."""
    words = prompt_manager.get_used_words(
        language="ja",
        category="Adjectives",
        data_dir=sample_vocab_data
    )
    assert len(words) == 2
    assert "新しい" in words
    assert "古い" in words

def test_get_used_words_nonexistent_file(prompt_manager, tmp_path):
    """Test retrieving used words when file doesn't exist."""
    words = prompt_manager.get_used_words(
        language="fr",
        category="Adjectives",
        data_dir=str(tmp_path)
    )
    assert words == []

def test_format_previously_used_section(prompt_manager):
    """Test formatting the previously used words section."""
    used_words = ["新しい", "古い"]
    section = prompt_manager.format_previously_used_section(used_words)
    assert "新しい" in section
    assert "古い" in section
    assert "should NOT be generated again" in section

def test_format_previously_used_section_empty(prompt_manager):
    """Test formatting empty previously used words section."""
    section = prompt_manager.format_previously_used_section([])
    assert section == ""

def test_get_prompt(prompt_manager):
    """Test generating a complete prompt."""
    prompt = prompt_manager.get_prompt(
        language="ja",
        category="Adjectives",
        num_words=5,
        used_words=["新しい", "古い"]
    )
    
    # Check template variables are replaced
    assert "Japanese Template" in prompt
    assert "Category: Adjectives" in prompt
    assert "Words: 5" in prompt
    assert "Language: ja" in prompt
    assert "新しい" in prompt
    assert "古い" in prompt
    assert "Instructions for ja" in prompt

def test_get_prompt_invalid_language(prompt_manager):
    """Test generating prompt with invalid language."""
    with pytest.raises(ValueError, match="Unsupported language"):
        prompt_manager.get_prompt(
            language="invalid",
            category="Adjectives"
        )

def test_get_semantic_categories(prompt_manager):
    """Test getting semantic categories for word types."""
    categories = prompt_manager.get_semantic_categories("Adjectives")
    assert len(categories) > 0
    assert "Physical Qualities" in categories
    assert "Emotions" in categories

def test_get_semantic_categories_unknown(prompt_manager):
    """Test getting semantic categories for unknown word type."""
    categories = prompt_manager.get_semantic_categories("Unknown")
    assert categories == [] 
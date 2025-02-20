"""Tests for vocabulary generation functionality."""
import json
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
from pathlib import Path
from streamlit.testing.v1 import AppTest
import streamlit as st

from utils.vocab_generator import VocabGenerator, VocabGeneratorError
from components.vocab_generator import (
    initialize_session_state,
    get_categories_for_language,
    render_generation_form,
    handle_save_changes,
    handle_generate_more,
    handle_export,
    display_results,
    render_generator,
    show_generation_progress
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

@pytest.fixture
def mock_streamlit(monkeypatch):
    """Mock Streamlit functions."""
    mock_st = {
        'button': MagicMock(return_value=False),
        'markdown': MagicMock(),
        'selectbox': MagicMock(),
        'slider': MagicMock(),
        'expander': MagicMock(),
        'error': MagicMock(),
        'success': MagicMock(),
        'info': MagicMock(),
        'empty': MagicMock(),
        'progress': MagicMock()
    }
    
    def mock_function(name):
        return mock_st[name]
    
    # Patch all Streamlit functions
    for name in mock_st:
        monkeypatch.setattr(st, name, mock_st[name])
    
    return mock_st

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

@pytest.fixture
def mock_session_state(monkeypatch):
    """Mock Streamlit's session state."""
    class SessionState(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.generation_error = None
            self.validation_error = None
            self.generated_vocab = None
            self.show_generator = False
            self.generation_inputs = {
                'category': 'Adjectives',
                'num_words': 10,
                'difficulty': 'Intermediate',
                'include_examples': True,
                'include_notes': True
            }
        
        def __getattr__(self, name):
            if name in self:
                return self[name]
            return None
        
        def __setattr__(self, name, value):
            self[name] = value

    mock_state = SessionState()
    monkeypatch.setattr(st, 'session_state', mock_state)
    return mock_state

def test_initialize_session_state(mock_session_state):
    """Test session state initialization."""
    # Clear session state
    mock_session_state.clear()
    
    # Initialize session state
    initialize_session_state()
    
    # Verify all required keys are present with default values
    assert 'generation_inputs' in st.session_state
    assert st.session_state['generation_inputs']['category'] == 'Adjectives'
    assert st.session_state['generation_inputs']['num_words'] == 10
    assert 'generated_vocab' in st.session_state
    assert st.session_state['generated_vocab'] is None
    assert 'show_generator' in st.session_state
    assert st.session_state['show_generator'] is False
    assert 'generation_error' in st.session_state
    assert st.session_state['generation_error'] is None

def test_get_categories_for_language():
    """Test getting categories for different languages."""
    # Test Japanese categories
    ja_categories = get_categories_for_language("Japanese 🇯🇵")
    assert "Verbs" in ja_categories
    assert "Adjectives" in ja_categories
    assert len(ja_categories) == 4
    
    # Test French categories
    fr_categories = get_categories_for_language("French 🇫🇷")
    assert "Adjectives" in fr_categories
    assert "Verbs" in fr_categories
    assert len(fr_categories) == 4
    
    # Test invalid language
    invalid_categories = get_categories_for_language("Invalid Language")
    assert invalid_categories == []

def test_handle_save_changes(mock_session_state):
    """Test saving changes to vocabulary entries."""
    # Setup test data
    mock_session_state['generated_vocab'] = [{
        'word': 'Old Word',
        'meaning': 'Old Meaning',
        'pronunciation': 'old-pron',
        'part_of_speech': 'noun',
        'notes': 'Old notes',
        'examples': ['Old example']
    }]
    
    # Setup form input values in session state
    mock_session_state.update({
        'word_1': 'New Word',
        'meaning_1': 'New Meaning',
        'pron_1': 'new-pron',
        'pos_1': 'verb',
        'notes_1': 'New notes',
        'examples_1': 'New example 1\nNew example 2'
    })
    
    # Call handle_save_changes
    handle_save_changes(1, mock_session_state['generated_vocab'][0])
    
    # Verify changes
    updated_word = mock_session_state['generated_vocab'][0]
    assert updated_word['word'] == 'New Word'
    assert updated_word['meaning'] == 'New Meaning'
    assert updated_word['pronunciation'] == 'new-pron'
    assert updated_word['part_of_speech'] == 'verb'
    assert updated_word['notes'] == 'New notes'
    assert len(updated_word['examples']) == 2
    assert 'New example 1' in updated_word['examples']

def test_handle_generate_more(mock_session_state):
    """Test handling generate more action."""
    # Setup initial state
    mock_session_state['generated_vocab'] = [{'word': 'Test'}]
    mock_session_state['show_generator'] = False
    
    # Call handle_generate_more
    handle_generate_more()
    
    # Verify state is reset
    assert mock_session_state['show_generator'] is True
    assert mock_session_state['generated_vocab'] is None

def test_handle_export(mock_session_state):
    """Test handling export action."""
    # Setup test data
    mock_session_state['generated_vocab'] = [{
        'word': 'Test Word',
        'meaning': 'Test Meaning'
    }]
    
    # Call handle_export
    # Note: We can't fully test the download functionality in unit tests
    # but we can verify it doesn't raise errors
    handle_export()

def test_display_results_error(mock_session_state):
    """Test displaying error in results."""
    # Test error display
    display_results(error="Test Error")
    
    # Test successful display
    test_vocab = [{
        'word': 'Test Word',
        'meaning': 'Test Meaning'
    }]
    display_results(vocab_list=test_vocab)

def test_render_generator_flow(mock_session_state, mock_streamlit):
    """Test the complete generator flow."""
    # Mock generate button click
    mock_streamlit['button'].return_value = True
    
    # Initial render
    render_generator("Japanese 🇯🇵")
    
    # Verify generator is shown
    assert mock_session_state['show_generator'] is True
    mock_streamlit['markdown'].assert_called()
    mock_streamlit['selectbox'].assert_called()
    mock_streamlit['slider'].assert_called()
    
    # Mock form submission
    mock_session_state['generation_inputs'] = {
        'category': 'Adjectives',
        'num_words': 5,
        'difficulty': 'Intermediate',
        'include_examples': True,
        'include_notes': True
    }
    
    # Re-render with form data
    render_generator("Japanese 🇯🇵")
    
    # Verify form elements are called
    mock_streamlit['selectbox'].assert_called()
    mock_streamlit['slider'].assert_called()
    mock_streamlit['button'].assert_called()

def test_integration_flow(mock_session_state, mock_streamlit):
    """Test the complete integration flow."""
    # Setup initial state
    mock_session_state['show_generator'] = False
    mock_session_state['generated_vocab'] = None
    mock_session_state['generation_error'] = None
    
    # Mock generate button click
    mock_streamlit['button'].return_value = True
    
    # Initial render
    render_generator("Japanese 🇯🇵")
    
    # Verify generator is shown
    assert mock_session_state['show_generator'] is True
    mock_streamlit['markdown'].assert_called()
    
    # Mock form submission
    mock_session_state['generation_inputs'] = {
        'category': 'Adjectives',
        'num_words': 5,
        'difficulty': 'Intermediate',
        'include_examples': True,
        'include_notes': True
    }
    
    # Mock successful generation
    mock_session_state['generated_vocab'] = SAMPLE_VOCAB_DATA['vocab_examples'][0]['vocab']
    
    # Initialize form state for each word
    for i, word in enumerate(mock_session_state['generated_vocab'], 1):
        mock_session_state[f"word_{i}"] = word.get('word', '')
        mock_session_state[f"meaning_{i}"] = word.get('meaning', '')
        mock_session_state[f"pron_{i}"] = word.get('pronunciation', '')
        mock_session_state[f"pos_{i}"] = word.get('part_of_speech', '')
        mock_session_state[f"notes_{i}"] = word.get('notes', '')
        mock_session_state[f"examples_{i}"] = '\n'.join(word.get('examples', []))
    
    # Re-render with generated vocab
    render_generator("Japanese 🇯🇵")
    
    # Verify results are displayed
    mock_streamlit['markdown'].assert_called()
    mock_streamlit['expander'].assert_called()
    assert not mock_session_state['generation_error']

def test_render_generation_form_with_error(mock_session_state, mock_streamlit):
    """Test rendering generation form when an error occurs."""
    mock_session_state.generation_error = "Test error"
    mock_session_state.show_generator = True
    render_generator("Japanese 🇯🇵")
    mock_streamlit['error'].assert_called_with("Test error")

def test_show_generation_progress_with_error(mock_session_state, mock_streamlit):
    """Test showing generation progress with error."""
    mock_session_state.generation_error = "Progress error"
    mock_streamlit['empty'].return_value = mock_streamlit['empty']
    progress, status = show_generation_progress()
    mock_streamlit['error'].assert_called_with("Progress error")
    assert progress == mock_streamlit['empty']
    assert status == mock_streamlit['empty']

def test_handle_save_changes_with_invalid_data(mock_session_state):
    """Test handling save changes with invalid data."""
    word = {"script": "", "meaning": ""}  # Invalid data
    handle_save_changes(0, word)
    assert "Invalid vocabulary data" in str(mock_session_state.validation_error)

def test_display_results_with_validation_error(mock_session_state, mock_streamlit):
    """Test displaying results with validation error."""
    mock_session_state.validation_error = "Validation error"
    display_results()  # Call without vocab_list to trigger validation error check
    mock_streamlit['error'].assert_called_with("Validation error") 
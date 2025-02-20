"""Tests for vocabulary generator component."""
import json
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
from pathlib import Path
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
    render_generator
)

# Sample test data
SAMPLE_VOCAB = {
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
                        {"unit": "新", "readings": ["a", "ta", "ra"]},
                        {"unit": "しい", "readings": ["shi", "i"]}
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
def mock_session_state(monkeypatch):
    """Mock Streamlit's session state."""
    mock_state = {
        'generation_inputs': {
            'category': 'Adjectives',
            'num_words': 10,
            'difficulty': 'Intermediate',
            'include_examples': True,
            'include_notes': True
        },
        'generated_vocab': None,
        'show_generator': False,
        'generation_error': None
    }
    
    monkeypatch.setattr(st, 'session_state', mock_state)
    return mock_state

@pytest.fixture
def mock_streamlit(monkeypatch):
    """Mock Streamlit functions for testing."""
    # Create mock functions
    mocks = {
        "markdown": MagicMock(),
        "selectbox": MagicMock(return_value="Adjectives"),
        "slider": MagicMock(return_value=5),
        "expander": MagicMock(),
        "button": MagicMock(return_value=False),
        "session_state": {},
        "columns": MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()]),
        "radio": MagicMock(return_value="Japanese 🇯🇵"),
        "checkbox": MagicMock(return_value=True),
        "error": MagicMock(),
        "success": MagicMock(),
        "info": MagicMock(),
        "write": MagicMock(),
        "empty": MagicMock()
    }

    # Mock the context manager for expander
    mocks["expander"].return_value.__enter__ = MagicMock()
    mocks["expander"].return_value.__exit__ = MagicMock()

    # Mock the context manager for columns
    for col in mocks["columns"].return_value:
        col.__enter__ = MagicMock()
        col.__exit__ = MagicMock()

    def patch_streamlit(name):
        """Patch a specific Streamlit function."""
        monkeypatch.setattr(f"streamlit.{name}", mocks[name])

    # Patch all mock functions
    for name in mocks:
        patch_streamlit(name)

    return mocks

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
    """Test getting categories for a language."""
    categories = get_categories_for_language("Japanese 🇯🇵")
    assert isinstance(categories, list)
    assert len(categories) > 0
    assert "Adjectives" in categories

def test_handle_save_changes(mock_session_state):
    """Test saving changes to vocabulary entries."""
    # Setup test data
    mock_session_state['generated_vocab'] = [{
        'script': 'Old Word',
        'meaning': 'Old Meaning',
        'transliteration': 'old-pron',
        'part_of_speech': 'noun',
        'notes': 'Old notes',
        'usage_examples': [{'script': 'Old example', 'meaning': 'Old meaning'}]
    }]
    
    # Mock form inputs
    mock_session_state.update({
        'script_0': 'New Word',
        'meaning_0': 'New Meaning',
        'transliteration_0': 'new-pron',
        'part_of_speech_0': 'verb',
        'notes_0': 'New notes',
        'usage_examples_0': 'New example\nNew meaning'
    })
    
    # Call handle_save_changes
    handle_save_changes(0, mock_session_state['generated_vocab'][0])
    
    # Verify changes
    updated_word = mock_session_state['generated_vocab'][0]
    assert updated_word['script'] == 'New Word'
    assert updated_word['meaning'] == 'New Meaning'
    assert updated_word['transliteration'] == 'new-pron'
    assert updated_word['part_of_speech'] == 'verb'
    assert updated_word['notes'] == 'New notes'
    assert len(updated_word['usage_examples']) == 1

def test_handle_generate_more(mock_session_state):
    """Test handling generate more action."""
    mock_session_state['generated_vocab'] = [{'script': 'Test'}]
    mock_session_state['show_generator'] = False
    
    handle_generate_more()
    
    assert mock_session_state['show_generator'] is True
    assert mock_session_state['generated_vocab'] is None

def test_handle_export(mock_session_state, tmp_path):
    """Test handling export action."""
    mock_session_state['generated_vocab'] = SAMPLE_VOCAB['vocab_examples'][0]['vocab']
    
    with patch('streamlit.download_button') as mock_download:
        handle_export()
        mock_download.assert_called_once()

def test_display_results_error(mock_session_state, mock_streamlit):
    """Test displaying error in results."""
    display_results(error="Test Error")
    mock_streamlit['error'].assert_called_once_with("Test Error")
    
    mock_session_state['generated_vocab'] = SAMPLE_VOCAB['vocab_examples'][0]['vocab']
    display_results(vocab_list=mock_session_state['generated_vocab'])
    mock_streamlit['markdown'].assert_called()

def test_render_generation_form(mock_session_state, mock_streamlit):
    """Test rendering the generation form."""
    result = render_generation_form("Japanese 🇯🇵")
    
    assert isinstance(result, dict)
    assert 'category' in result
    assert 'num_words' in result
    mock_streamlit['selectbox'].assert_called()
    mock_streamlit['slider'].assert_called()

def test_render_generator(mock_session_state, mock_streamlit):
    """Test rendering the generator component."""
    render_generator("Japanese 🇯🇵")
    mock_streamlit['markdown'].assert_called()
    
    # Test with error
    mock_session_state['generation_error'] = "Test Error"
    render_generator("Japanese 🇯🇵")
    mock_streamlit['error'].assert_called_with("Test Error")
    
    # Test with generated vocab
    mock_session_state['generation_error'] = None
    mock_session_state['generated_vocab'] = SAMPLE_VOCAB['vocab_examples'][0]['vocab']
    render_generator("Japanese 🇯🇵")
    mock_streamlit['markdown'].assert_called()

def test_render_generator_flow(mock_session_state, mock_streamlit):
    """Test the complete generator flow."""
    # Initial state
    mock_session_state['show_generator'] = False
    mock_session_state['generated_vocab'] = None
    mock_session_state['generation_error'] = None
    mock_session_state['generation_inputs'] = {
        'category': 'Adjectives',
        'num_words': 5,
        'difficulty': 'Intermediate',
        'include_examples': True,
        'include_notes': True
    }

    # Mock generate button click
    mock_streamlit['button'].return_value = True

    # Initial render
    render_generator("Japanese 🇯🇵")

    # Verify initial render
    mock_streamlit['markdown'].assert_called()
    assert mock_session_state['show_generator'] is True

    # Verify form elements
    mock_streamlit['selectbox'].assert_called_with(
        "Word Category",
        ["Verbs", "Adjectives", "Nouns", "Expressions"],
        key="generation_inputs.category",
        format_func=lambda x: f"📑 {x}",
        help="Select the type of words to generate"
    )

    mock_streamlit['slider'].assert_called()
    mock_streamlit['button'].assert_called()

def test_integration_flow(mock_session_state, mock_streamlit):
    """Test the complete integration flow."""
    # Setup initial state
    mock_session_state['show_generator'] = False
    mock_session_state['generated_vocab'] = None
    mock_session_state['generation_error'] = None
    mock_session_state['generation_inputs'] = {
        'category': 'Adjectives',
        'num_words': 5,
        'difficulty': 'Intermediate',
        'include_examples': True,
        'include_notes': True
    }

    # Mock generate button click
    mock_streamlit['button'].return_value = True

    # Initial render
    render_generator("Japanese 🇯🇵")

    # Verify generator is shown
    assert mock_session_state['show_generator'] is True
    mock_streamlit['markdown'].assert_called()

    # Mock successful generation
    mock_session_state['generated_vocab'] = SAMPLE_VOCAB['vocab_examples'][0]['vocab']

    # Initialize form state for each word
    for i, word in enumerate(mock_session_state['generated_vocab'], 1):
        mock_session_state[f"word_{i}"] = word.get('script', '')
        mock_session_state[f"meaning_{i}"] = word.get('meaning', '')
        mock_session_state[f"pron_{i}"] = word.get('transliteration', '')
        mock_session_state[f"pos_{i}"] = word.get('part_of_speech', '')
        mock_session_state[f"notes_{i}"] = word.get('notes', '')
        mock_session_state[f"examples_{i}"] = '\n'.join(
            [ex['script'] for ex in word.get('usage_examples', [])]
        )

    # Re-render with generated vocab
    render_generator("Japanese 🇯🇵")

    # Verify results are displayed
    mock_streamlit['markdown'].assert_called()
    mock_streamlit['expander'].assert_called()
    assert not mock_session_state['generation_error']

def test_initialize_session_state_with_existing_data(mock_session_state):
    """Test session state initialization when data already exists."""
    # Setup existing state
    mock_session_state['generation_inputs'] = {
        'category': 'Verbs',
        'num_words': 20,
        'difficulty': 'Advanced',
        'include_examples': False,
        'include_notes': False
    }
    
    # Initialize session state
    initialize_session_state()
    
    # Verify existing data is preserved
    assert mock_session_state['generation_inputs']['category'] == 'Verbs'
    assert mock_session_state['generation_inputs']['num_words'] == 20
    assert mock_session_state['generation_inputs']['difficulty'] == 'Advanced'
    assert mock_session_state['generation_inputs']['include_examples'] is False
    assert mock_session_state['generation_inputs']['include_notes'] is False

def test_handle_save_changes_with_empty_examples(mock_session_state):
    """Test saving changes when examples field is empty."""
    mock_session_state['generated_vocab'] = [{
        'script': 'Test Word',
        'meaning': 'Test Meaning',
        'transliteration': 'test-pron',
        'part_of_speech': 'noun',
        'notes': 'Test notes',
        'usage_examples': []
    }]
    
    mock_session_state.update({
        'script_0': 'Updated Word',
        'meaning_0': 'Updated Meaning',
        'transliteration_0': 'updated-pron',
        'part_of_speech_0': 'verb',
        'notes_0': 'Updated notes',
        'usage_examples_0': ''  # Empty examples
    })
    
    handle_save_changes(0, mock_session_state['generated_vocab'][0])
    
    updated_word = mock_session_state['generated_vocab'][0]
    assert updated_word['script'] == 'Updated Word'
    assert updated_word['usage_examples'] == []

def test_handle_export_empty_vocab(mock_session_state):
    """Test export handling when vocabulary is empty."""
    mock_session_state['generated_vocab'] = None
    
    with patch('streamlit.download_button') as mock_download:
        handle_export()
        mock_download.assert_not_called()

def test_display_results_with_empty_vocab(mock_session_state, mock_streamlit):
    """Test displaying results with empty vocabulary."""
    display_results(vocab_list=[])
    mock_streamlit['markdown'].assert_called()
    assert not mock_streamlit['error'].called

def test_render_generation_form_with_invalid_category(mock_session_state, mock_streamlit):
    """Test rendering form when current category is invalid for selected language."""
    # Setup invalid category
    mock_session_state['generation_inputs']['category'] = 'InvalidCategory'
    
    result = render_generation_form("Japanese 🇯🇵")
    
    # Should reset to first available category
    assert result['category'] in get_categories_for_language("Japanese 🇯🇵")
    mock_streamlit['selectbox'].assert_called()

def test_render_generator_with_generation_error(mock_session_state, mock_streamlit):
    """Test rendering generator when there's a generation error."""
    mock_session_state['generation_error'] = "Test generation error"
    mock_session_state['show_generator'] = True
    
    render_generator("Japanese 🇯🇵")
    
    mock_streamlit['error'].assert_called_with("Test generation error")
    assert mock_session_state['show_generator'] is True

def test_render_generator_with_empty_vocab(mock_session_state, mock_streamlit):
    """Test rendering generator with empty vocabulary."""
    mock_session_state['show_generator'] = True
    mock_session_state['generated_vocab'] = []
    
    render_generator("Japanese 🇯🇵")
    
    mock_streamlit['markdown'].assert_called()
    assert mock_session_state['show_generator'] is True 
"""Vocabulary generation interface component."""
import streamlit as st
from typing import Optional, Dict, List
import json
import tempfile
import os
from gtts import gTTS
from utils.vocab_generator import VocabGenerator, VocabGeneratorError
import base64
import time

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'generation_inputs' not in st.session_state:
        st.session_state.generation_inputs = {
            'category': 'Adjectives',
            'num_words': 10,
            'difficulty': 'Intermediate',
            'include_examples': True,
            'include_notes': True
        }
    if 'generated_vocab' not in st.session_state:
        st.session_state.generated_vocab = None
    if 'has_unsaved_changes' not in st.session_state:
        st.session_state.has_unsaved_changes = False
    if 'last_language' not in st.session_state:
        st.session_state.last_language = None
    if 'generation_error' not in st.session_state:
        st.session_state.generation_error = None
    if 'validation_error' not in st.session_state:
        st.session_state.validation_error = None
    if 'language_code' not in st.session_state:
        st.session_state.language_code = None
    if 'vocab_generator' not in st.session_state:
        try:
            st.session_state.vocab_generator = VocabGenerator()
        except Exception as e:
            st.error(f"Failed to initialize vocabulary generator: {str(e)}")
            st.session_state.vocab_generator = None
    if 'audio_cache' not in st.session_state:
        st.session_state.audio_cache = {}
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'ui_state' not in st.session_state:
        st.session_state.ui_state = {
            'editing_words': set(),   # Track which words are being edited
            'loading_states': {},     # Track loading states for async operations
            'error_words': set(),     # Track words with errors
            'audio_timestamps': {}    # Track when audio was last used
        }

def cleanup_audio_cache():
    """Clean up old audio cache entries (older than 5 minutes)."""
    current_time = time.time()
    audio_timestamps = st.session_state.ui_state['audio_timestamps']
    
    # Remove old audio entries
    for text in list(st.session_state.audio_cache.keys()):
        if text in audio_timestamps:
            if current_time - audio_timestamps[text] > 300:  # 5 minutes
                del st.session_state.audio_cache[text]
                del audio_timestamps[text]

def get_categories_for_language(language: str) -> List[str]:
    """Get available categories for the selected language."""
    # Extract language code from the display name (e.g., "Japanese 🇯🇵" -> "ja")
    language_map = {
        "Japanese 🇯🇵": "ja",
        "French 🇫🇷": "fr",
        "Arabic 🇸🇦": "ar",
        "Spanish 🇪🇸": "es"
    }
    language_code = language_map.get(language)
    if not language_code:
        return ["Adjectives", "Nouns", "Verbs"]  # Default categories
    
    if not st.session_state.vocab_generator:
        return ["Adjectives", "Nouns", "Verbs"]  # Default categories
    try:
        categories = st.session_state.vocab_generator.get_available_categories(language_code)
        if not categories:  # If no categories found, return defaults
            return ["Adjectives", "Nouns", "Verbs"]
        return categories
    except Exception:
        return ["Adjectives", "Nouns", "Verbs"]  # Fallback to defaults

def handle_language_change(selected_language: str) -> bool:
    """Handle language change and return whether to proceed with the change."""
    if st.session_state.last_language != selected_language:
        if st.session_state.has_unsaved_changes:
            save_col1, save_col2 = st.columns(2)
            with save_col1:
                if st.button("Save Current Words", type="primary"):
                    try:
                        handle_export()
                        st.success("Words saved successfully!")
                        st.session_state.has_unsaved_changes = False
                        return True
                    except Exception as e:
                        st.error(f"Failed to save words: {str(e)}")
                        return False
            with save_col2:
                if st.button("Discard Changes"):
                    st.session_state.has_unsaved_changes = False
                    return True
            st.info("Please choose to save or discard your current words before changing language.")
            return False
        return True
    return True

def reset_generation_state():
    """Reset the generation state for new words."""
    st.session_state.generated_vocab = None
    st.session_state.has_unsaved_changes = False
    st.session_state.ui_state['editing_words'].clear()
    st.session_state.ui_state['error_words'].clear()
    cleanup_audio_cache()

def render_generator(selected_language: str):
    """Main function to render the vocabulary generator interface."""
    # Initialize session state
    initialize_session_state()
    
    # Handle language change
    if not handle_language_change(selected_language):
        return
    
    # Update last language
    st.session_state.last_language = selected_language
    
    # Show generation form
    st.markdown("""
    <div class="stcard">
        <h3>📚 Vocabulary Generator</h3>
        <p style="color: #a0aec0; margin-bottom: 1.5rem;">Configure your vocabulary list generation:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category selection based on selected language
    categories = get_categories_for_language(selected_language)
    
    # If current category isn't valid for this language, reset it
    if st.session_state.generation_inputs['category'] not in categories and categories:
        st.session_state.generation_inputs['category'] = categories[0]
    
    # Form elements
    category = st.selectbox(
        "Word Category",
        options=categories,
        index=categories.index(st.session_state.generation_inputs['category']) if st.session_state.generation_inputs['category'] in categories else 0,
        key="generation_inputs.category",
        format_func=lambda x: f"📑 {x}",
        help="Select the type of words to generate"
    )
    
    # Update session state with selected category
    st.session_state.generation_inputs['category'] = category
    
    # Number of words slider
    num_words = st.slider(
        "Number of Words",
        min_value=5,
        max_value=50,
        value=st.session_state.generation_inputs['num_words'],
        step=5,
        key="generation_inputs.num_words",
        help="Choose how many words to generate"
    )
    
    # Update session state with selected number of words
    st.session_state.generation_inputs['num_words'] = num_words
    
    # Advanced options in expander
    with st.expander("Advanced Options"):
        st.select_slider(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.generation_inputs['difficulty'],
            key="generation_inputs.difficulty",
            help="Select the difficulty level of generated words"
        )
        
        st.checkbox(
            "Include Usage Examples",
            value=st.session_state.generation_inputs['include_examples'],
            key="generation_inputs.include_examples",
            help="Generate example sentences for each word"
        )
        
        st.checkbox(
            "Include Grammar Notes",
            value=st.session_state.generation_inputs['include_notes'],
            key="generation_inputs.include_notes",
            help="Add grammatical information and usage notes"
        )
    
    # Generate button
    generate_col1, generate_col2 = st.columns([3, 1])
    with generate_col1:
        if st.button("Generate Words", type="primary", use_container_width=True):
            if st.session_state.has_unsaved_changes:
                st.warning("You have unsaved changes. Please save or discard them first.")
            else:
                reset_generation_state()
                generate_vocabulary(selected_language)
    
    if st.session_state.has_unsaved_changes:
        with generate_col2:
            if st.button("Save Words", use_container_width=True):
                handle_export()
                st.success("Words saved successfully!")
                st.session_state.has_unsaved_changes = False
    
    # Display results if available
    if st.session_state.generation_error:
        st.error(st.session_state.generation_error)
    elif st.session_state.generated_vocab:
        display_results()

def generate_vocabulary(selected_language: str):
    """Generate vocabulary based on current settings."""
    progress_bar, status = show_generation_progress()
    
    try:
        if not st.session_state.vocab_generator:
            raise VocabGeneratorError("Vocabulary generator not initialized")
        
        # Get language code from the mapping
        language_map = {
            "Japanese 🇯🇵": "ja",
            "French 🇫🇷": "fr",
            "Arabic 🇸🇦": "ar",
            "Spanish 🇪🇸": "es"
        }
        language_code = language_map.get(selected_language)
        if not language_code:
            raise VocabGeneratorError(f"Unsupported language: {selected_language}")
        
        # Store language code in session state
        st.session_state.language_code = language_code
        
        # Update progress
        progress_bar.progress(25)
        status.info("Generating vocabulary...")
        
        # Generate vocabulary
        selected_num_words = st.session_state.generation_inputs['num_words']
        
        result = st.session_state.vocab_generator.generate_vocabulary(
            language=language_code,
            category=st.session_state.generation_inputs['category'],
            num_words=selected_num_words,
            save_to_file=False
        )
        
        # Process results
        vocab_entries = result["vocab_examples"][0]["vocab"]
        if len(vocab_entries) != selected_num_words:
            st.warning(f"Expected {selected_num_words} words but received {len(vocab_entries)} words.")
        
        # Convert to UI format
        st.session_state.generated_vocab = [
            {
                "script": entry["script"],
                "transliteration": entry["transliteration"],
                "pronunciation_aid": entry.get("pronunciation_aid", []),
                "meaning": entry["meaning"],
                "part_of_speech": entry["part_of_speech"],
                "usage_examples": entry.get("usage_examples", []),
                "notes": entry.get("notes", "")
            }
            for entry in vocab_entries
        ]
        
        # Mark as having unsaved changes
        st.session_state.has_unsaved_changes = True
        
        # Initialize form state
        for i, word in enumerate(st.session_state.generated_vocab, 1):
            st.session_state[f"word_{i}"] = word["script"]
            st.session_state[f"meaning_{i}"] = word["meaning"]
            st.session_state[f"trans_{i}"] = word["transliteration"]
            st.session_state[f"pos_{i}"] = word["part_of_speech"]
            st.session_state[f"notes_{i}"] = word["notes"]
            
            for j, unit in enumerate(word["pronunciation_aid"]):
                st.session_state[f"unit_{i}_{j}"] = unit["unit"]
                st.session_state[f"readings_{i}_{j}"] = ", ".join(unit["readings"])
            
            for j, example in enumerate(word["usage_examples"]):
                st.session_state[f"ex_script_{i}_{j}"] = example["script"]
                st.session_state[f"ex_meaning_{i}_{j}"] = example["meaning"]
        
        # Update progress
        progress_bar.progress(100)
        status.success("Generation complete!")
        
    except Exception as e:
        st.session_state.generation_error = str(e)
    finally:
        progress_bar.empty()
        status.empty()

def show_generation_progress():
    """Show progress during vocabulary generation."""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    if st.session_state.generation_error:
        st.error(st.session_state.generation_error)
        return progress_placeholder, status_placeholder
    
    with st.spinner("Generating vocabulary..."):
        progress_placeholder.progress(0)
        status_placeholder.text("Starting generation...")
    
    return progress_placeholder, status_placeholder

def handle_save_changes(i: int, word: Dict):
    """Handle saving changes to a vocabulary entry."""
    word_id = f"word_{i}"
    
    try:
        # Clear any previous errors
        st.session_state.validation_error = None
        st.session_state.ui_state['error_words'].discard(word_id)
        
        # Validate required fields
        if not word or not isinstance(word, dict):
            st.session_state.validation_error = "Invalid vocabulary data"
            st.session_state.ui_state['error_words'].add(word_id)
            return
        
        # Initialize generated_vocab if needed
        if 'generated_vocab' not in st.session_state:
            st.session_state.generated_vocab = []
        
        # Convert to 0-based index for list operations
        list_index = i - 1
        
        # Ensure the list has enough space
        while len(st.session_state.generated_vocab) <= list_index:
            st.session_state.generated_vocab.append({})
        
        # Update the word
        st.session_state.generated_vocab[list_index] = word
        
        # Clear edit state
        st.session_state.ui_state['editing_words'].discard(word_id)
        
    except Exception as e:
        st.session_state.validation_error = f"Failed to save changes: {str(e)}"
        st.session_state.ui_state['error_words'].add(word_id)

def handle_generate_more():
    """Handle generating more vocabulary."""
    # Clear all states
    st.session_state.has_unsaved_changes = True
    st.session_state.generated_vocab = None
    st.session_state.ui_state['editing_words'].clear()
    st.session_state.ui_state['error_words'].clear()
    cleanup_audio_cache()  # Clean up audio cache

def handle_export():
    """Handle exporting vocabulary list."""
    if st.session_state.generated_vocab:
        col1, col2 = st.columns(2)
        with col1:
            # Save to JSON file button
            if st.button("Save to File"):
                try:
                    result = st.session_state.vocab_generator.generate_vocabulary(
                        language=st.session_state.language_code,  # We need to store this in session state
                        category=st.session_state.generation_inputs['category'],
                        num_words=len(st.session_state.generated_vocab),
                        save_to_file=True,
                        vocab_data={"vocab_examples": [{"vocab": st.session_state.generated_vocab}]}
                    )
                    st.success("Saved vocabulary to file successfully!")
                except Exception as e:
                    st.error(f"Failed to save vocabulary: {str(e)}")
        
        with col2:
            # Download JSON button
            json_str = json.dumps(st.session_state.generated_vocab, indent=2, ensure_ascii=False)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="vocabulary.json",
                mime="application/json"
            )

def generate_audio(text: str, lang: str) -> str:
    """Generate audio file for the given text and return the path."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            # Generate audio
            tts = gTTS(text=text, lang=lang)
            # Save to temporary file
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Failed to generate audio: {str(e)}")
        return None

def play_audio(text: str, lang: str, key: str, button_text: str = "🔊"):
    """Create an audio player for the given text."""
    cleanup_audio_cache()  # Clean up old cache entries
    
    # Generate and cache audio if not already cached
    if text not in st.session_state.audio_cache:
        loading_key = f"loading_{key}"
        st.session_state.ui_state['loading_states'][loading_key] = True
        
        try:
            audio_file = generate_audio(text, lang)
            if audio_file:
                with open(audio_file, 'rb') as f:
                    st.session_state.audio_cache[text] = f.read()
                    st.session_state.ui_state['audio_timestamps'][text] = time.time()
                os.unlink(audio_file)
        except Exception as e:
            st.error(f"Failed to generate audio: {str(e)}")
        finally:
            st.session_state.ui_state['loading_states'].pop(loading_key, None)
    
    # Show loading spinner or audio player
    loading_key = f"loading_{key}"
    if loading_key in st.session_state.ui_state['loading_states']:
        st.spinner("Generating audio...")
        return
    
    # Get audio bytes from cache
    audio_bytes = st.session_state.audio_cache.get(text)
    if audio_bytes:
        # Create a small container for the audio player
        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )

def display_results(vocab_list: Optional[List[Dict]] = None, error: Optional[str] = None):
    """Display generated vocabulary results or error message."""
    if error:
        st.error(error)
        return
    
    if not vocab_list and not st.session_state.generated_vocab:
        if st.session_state.validation_error:
            st.error(st.session_state.validation_error)
        elif st.session_state.generation_error:
            st.error(st.session_state.generation_error)
        return
    
    # Use provided vocab list or get from session state
    vocab_to_display = vocab_list if vocab_list else st.session_state.generated_vocab
    
    try:
        # Display each word in a container to isolate state
        for i, word in enumerate(vocab_to_display):
            word_id = f"word_{i+1}"
            
            # Create a container for each word to isolate its state
            with st.container():
                # Basic word info in expander
                with st.expander(f"Word {i+1}: {word.get('script', '')}", expanded=False):
                    try:
                        # Check edit state
                        is_editing = word_id in st.session_state.ui_state['editing_words']
                        
                        # Main content area
                        main_cols = st.columns([3, 3, 2])
                        
                        # Column 1: Script and Meaning
                        with main_cols[0]:
                            if not is_editing:
                                st.markdown(f"**Script:** {word.get('script', '')}")
                                st.markdown(f"**Meaning:** {word.get('meaning', '')}")
                            else:
                                st.text_input("Script", value=word.get('script', ''), key=f"{word_id}_script")
                                st.text_input("Meaning", value=word.get('meaning', ''), key=f"{word_id}_meaning")
                        
                        # Column 2: Part of Speech and Transliteration
                        with main_cols[1]:
                            if not is_editing:
                                st.markdown(f"**Part of Speech:** {word.get('part_of_speech', '')}")
                                st.markdown(f"**Transliteration:** {word.get('transliteration', '')}")
                            else:
                                st.text_input("Part of Speech", value=word.get('part_of_speech', ''), key=f"{word_id}_pos")
                                st.text_input("Transliteration", value=word.get('transliteration', ''), key=f"{word_id}_trans")
                        
                        # Column 3: Audio Player
                        with main_cols[2]:
                            if word.get('script'):
                                st.markdown("**Audio:**")
                                play_audio(word['script'], st.session_state.language_code, key=f"{word_id}_audio")
                        
                        # Edit/Save Button
                        if st.button("Edit" if not is_editing else "Save", key=f"{word_id}_edit", use_container_width=True):
                            try:
                                if is_editing:
                                    # Save changes
                                    updated_word = {
                                        "script": st.session_state[f"{word_id}_script"],
                                        "meaning": st.session_state[f"{word_id}_meaning"],
                                        "part_of_speech": st.session_state[f"{word_id}_pos"],
                                        "transliteration": st.session_state[f"{word_id}_trans"],
                                        "pronunciation_aid": word.get("pronunciation_aid", []),
                                        "usage_examples": word.get("usage_examples", []),
                                        "notes": word.get("notes", "")
                                    }
                                    handle_save_changes(i+1, updated_word)
                                    st.session_state.ui_state['editing_words'].remove(word_id)
                                else:
                                    st.session_state.ui_state['editing_words'].add(word_id)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to save changes: {str(e)}")
                        
                        # Additional sections in tabs
                        if any([word.get('pronunciation_aid'), word.get('notes'), word.get('usage_examples')]):
                            tabs = st.tabs(["Pronunciation", "Notes", "Examples"])
                            
                            # Pronunciation Aid tab
                            with tabs[0]:
                                if word.get('pronunciation_aid'):
                                    for j, unit in enumerate(word['pronunciation_aid']):
                                        cols = st.columns([3, 3, 2])
                                        with cols[0]:
                                            if is_editing:
                                                st.text_input(f"Unit {j+1}", value=unit.get('unit', ''), key=f"{word_id}_unit_{j}")
                                            else:
                                                st.markdown(f"**{unit.get('unit', '')}**")
                                        with cols[1]:
                                            if is_editing:
                                                st.text_input(f"Readings {j+1}", value=", ".join(unit.get('readings', [])), key=f"{word_id}_readings_{j}")
                                            else:
                                                st.markdown(f"{', '.join(unit.get('readings', []))}")
                                        with cols[2]:
                                            if unit.get('unit'):
                                                st.markdown("**Audio:**")
                                                play_audio(unit['unit'], st.session_state.language_code, key=f"{word_id}_unit_audio_{j}")
                            
                            # Notes tab
                            with tabs[1]:
                                if word.get('notes'):
                                    if is_editing:
                                        st.text_area("Notes", value=word['notes'], key=f"{word_id}_notes")
                                    else:
                                        st.markdown(word['notes'])
                            
                            # Examples tab
                            with tabs[2]:
                                if word.get('usage_examples'):
                                    for j, example in enumerate(word['usage_examples']):
                                        cols = st.columns(2)
                                        with cols[0]:
                                            if is_editing:
                                                st.text_input(f"Example {j+1} Script", value=example.get('script', ''), key=f"{word_id}_example_{j}_script")
                                            else:
                                                st.markdown(f"**{example.get('script', '')}**")
                                        with cols[1]:
                                            if is_editing:
                                                st.text_input(f"Example {j+1} Meaning", value=example.get('meaning', ''), key=f"{word_id}_example_{j}_meaning")
                                            else:
                                                st.markdown(f"_{example.get('meaning', '')}_")
                    
                    except Exception as e:
                        st.error(f"Error displaying word content: {str(e)}")
        
        # Action buttons
        action_cols = st.columns(2)
        with action_cols[0]:
            if st.button("Generate More", use_container_width=True):
                handle_generate_more()
        with action_cols[1]:
            if st.button("Export", use_container_width=True):
                handle_export()
    
    except Exception as e:
        st.error(f"Error displaying vocabulary list: {str(e)}") 
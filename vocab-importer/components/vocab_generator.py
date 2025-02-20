"""Vocabulary generation interface component."""
import streamlit as st
from typing import Optional, Dict, List
import json

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'generation_inputs' not in st.session_state:
        st.session_state['generation_inputs'] = {
            'category': 'Adjectives',
            'num_words': 10,
            'difficulty': 'Intermediate',
            'include_examples': True,
            'include_notes': True
        }
    if 'generated_vocab' not in st.session_state:
        st.session_state['generated_vocab'] = None
    if 'show_generator' not in st.session_state:
        st.session_state['show_generator'] = False
    if 'generation_error' not in st.session_state:
        st.session_state['generation_error'] = None

def get_categories_for_language(language: str) -> List[str]:
    """Get available categories for a language."""
    categories = {
        "Japanese 🇯🇵": ["Verbs", "Adjectives", "Nouns", "Expressions"],
        "French 🇫🇷": ["Adjectives", "Verbs", "Nouns", "Adverbs"],
        "Arabic 🇸🇦": ["Nouns", "Verbs", "Adjectives", "Phrases"],
        "Spanish 🇪🇸": ["Verbs", "Adjectives", "Nouns", "Common Phrases"]
    }
    return categories.get(language, [])

def render_generation_form(selected_language: str) -> Dict[str, str]:
    """Render the vocabulary generation form and return user inputs."""
    st.markdown("""
    <div class="stcard">
        <h3>📚 Generate Vocabulary</h3>
        <p style="color: #a0aec0; margin-bottom: 1.5rem;">Configure your vocabulary list generation:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category selection based on selected language
    categories = get_categories_for_language(selected_language)
    
    # If current category isn't valid for this language, reset it
    if st.session_state['generation_inputs']['category'] not in categories and categories:
        st.session_state['generation_inputs']['category'] = categories[0]
    
    st.selectbox(
        "Word Category",
        categories,
        key="generation_inputs.category",
        format_func=lambda x: f"📑 {x}",
        help="Select the type of words to generate"
    )
    
    # Number of words
    st.slider(
        "Number of Words",
        min_value=5,
        max_value=50,
        value=10,
        step=5,
        key="generation_inputs.num_words",
        help="Choose how many words to generate"
    )
    
    # Advanced options in expander
    with st.expander("Advanced Options"):
        st.select_slider(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state['generation_inputs']['difficulty'],
            key="generation_inputs.difficulty",
            help="Select the difficulty level of generated words"
        )
        
        st.checkbox(
            "Include Usage Examples",
            value=st.session_state['generation_inputs']['include_examples'],
            key="generation_inputs.include_examples",
            help="Generate example sentences for each word"
        )
        
        st.checkbox(
            "Include Grammar Notes",
            value=st.session_state['generation_inputs']['include_notes'],
            key="generation_inputs.include_notes",
            help="Add grammatical information and usage notes"
        )
    
    return {
        "language": selected_language,
        **st.session_state['generation_inputs']
    }

def show_generation_progress():
    """Display a progress bar and status messages during generation."""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    return progress_placeholder, status_placeholder

def handle_save_changes(i: int, word: Dict):
    """Handle saving changes to a vocabulary entry."""
    # Update the word in session state
    st.session_state['generated_vocab'][i-1].update({
        'word': st.session_state[f"word_{i}"],
        'meaning': st.session_state[f"meaning_{i}"],
        'pronunciation': st.session_state.get(f"pron_{i}", ""),
        'part_of_speech': st.session_state.get(f"pos_{i}", ""),
        'notes': st.session_state.get(f"notes_{i}", ""),
        'examples': st.session_state.get(f"examples_{i}", "").split('\n')
    })
    st.success("Changes saved!")

def handle_generate_more():
    """Handle generating more vocabulary."""
    st.session_state['show_generator'] = True
    st.session_state['generated_vocab'] = None

def handle_export():
    """Handle exporting vocabulary list."""
    if st.session_state['generated_vocab']:
        # Convert to JSON for download
        json_str = json.dumps(st.session_state['generated_vocab'], indent=2, ensure_ascii=False)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="vocabulary.json",
            mime="application/json"
        )

def display_results(vocab_list: Optional[List[Dict]] = None, error: Optional[str] = None):
    """Display generation results or error message."""
    if error:
        st.error(f"Generation failed: {error}")
        if st.button("Try Again"):
            st.session_state['generation_error'] = None
            st.session_state['show_generator'] = True
        return
    
    if not vocab_list and not st.session_state['generated_vocab']:
        return
    
    vocab_list = vocab_list or st.session_state['generated_vocab']
    
    st.markdown("""
    <div class="stcard">
        <h3>✨ Generated Vocabulary</h3>
        <p style="color: #a0aec0; margin-bottom: 1.5rem;">Review and edit the generated words:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each word in an expander for easy review
    for i, word in enumerate(vocab_list, 1):
        with st.expander(f"{i}. {word.get('word', 'Unknown')} - {word.get('meaning', 'No meaning')}"):
            # Word details in columns
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Word", value=word.get('word', ''), key=f"word_{i}")
                st.text_input("Meaning", value=word.get('meaning', ''), key=f"meaning_{i}")
                if word.get('pronunciation'):
                    st.text_input("Pronunciation", value=word['pronunciation'], key=f"pron_{i}")
            
            with col2:
                if word.get('part_of_speech'):
                    st.text_input("Part of Speech", value=word['part_of_speech'], key=f"pos_{i}")
                if word.get('notes'):
                    st.text_area("Notes", value=word['notes'], key=f"notes_{i}")
            
            # Examples in full width
            if word.get('examples'):
                st.text_area("Examples", value='\n'.join(word['examples']), key=f"examples_{i}")
            
            # Save button for this word
            if st.button("Save Changes", key=f"save_{i}", use_container_width=True):
                handle_save_changes(i, word)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate More", use_container_width=True):
            handle_generate_more()
    with col2:
        handle_export()

def render_generator(selected_language: str):
    """Main function to render the vocabulary generator interface."""
    # Initialize session state
    initialize_session_state()
    
    if st.session_state['generation_error']:
        display_results(error=st.session_state['generation_error'])
        return
    
    if st.session_state['generated_vocab']:
        display_results()
        return
    
    # Show generate button first if generator is not shown
    if not st.session_state['show_generator']:
        st.markdown("""
        <div class="stcard">
            <h3>📚 Vocabulary Generator</h3>
            <p style="color: #a0aec0; margin-bottom: 1.5rem;">Click the button below to start generating vocabulary:</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Vocabulary", type="primary", use_container_width=True):
            st.session_state['show_generator'] = True
    
    # Show form if generator is enabled
    if st.session_state['show_generator']:
        st.markdown("""
        <div class="stcard">
            <h3>📚 Generate Vocabulary</h3>
            <p style="color: #a0aec0; margin-bottom: 1.5rem;">Configure your vocabulary list generation:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Category selection based on selected language
        categories = get_categories_for_language(selected_language)
        
        # If current category isn't valid for this language, reset it
        if st.session_state['generation_inputs']['category'] not in categories and categories:
            st.session_state['generation_inputs']['category'] = categories[0]
        
        # Form elements
        st.selectbox(
            "Word Category",
            categories,
            key="generation_inputs.category",
            format_func=lambda x: f"📑 {x}",
            help="Select the type of words to generate"
        )
        
        st.slider(
            "Number of Words",
            min_value=5,
            max_value=50,
            value=st.session_state['generation_inputs']['num_words'],
            step=5,
            key="generation_inputs.num_words",
            help="Choose how many words to generate"
        )
        
        # Advanced options in expander
        with st.expander("Advanced Options"):
            st.select_slider(
                "Difficulty Level",
                options=["Beginner", "Intermediate", "Advanced"],
                value=st.session_state['generation_inputs']['difficulty'],
                key="generation_inputs.difficulty",
                help="Select the difficulty level of generated words"
            )
            
            st.checkbox(
                "Include Usage Examples",
                value=st.session_state['generation_inputs']['include_examples'],
                key="generation_inputs.include_examples",
                help="Generate example sentences for each word"
            )
            
            st.checkbox(
                "Include Grammar Notes",
                value=st.session_state['generation_inputs']['include_notes'],
                key="generation_inputs.include_notes",
                help="Add grammatical information and usage notes"
            )
        
        # Generate button for actual generation
        if st.button("Generate Words", type="primary", use_container_width=True):
            progress_bar, status = show_generation_progress()
            
            try:
                # Placeholder for actual generation logic
                progress_bar.progress(0)
                status.info("Initializing generation...")
                # TODO: Add actual generation logic here
                
                # Placeholder vocab list for testing
                st.session_state['generated_vocab'] = [
                    {
                        "word": "Example",
                        "meaning": "A sample word",
                        "pronunciation": "eg-zam-pul",
                        "part_of_speech": "noun",
                        "notes": "This is a sample note",
                        "examples": ["This is an example sentence.", "Another example here."]
                    }
                ]
                
                # Initialize form state for each word
                for i, word in enumerate(st.session_state['generated_vocab'], 1):
                    st.session_state[f"word_{i}"] = word.get('word', '')
                    st.session_state[f"meaning_{i}"] = word.get('meaning', '')
                    st.session_state[f"pron_{i}"] = word.get('pronunciation', '')
                    st.session_state[f"pos_{i}"] = word.get('part_of_speech', '')
                    st.session_state[f"notes_{i}"] = word.get('notes', '')
                    st.session_state[f"examples_{i}"] = '\n'.join(word.get('examples', []))
                
                display_results(vocab_list=st.session_state['generated_vocab'])
                
            except Exception as e:
                st.session_state['generation_error'] = str(e)
                display_results(error=str(e))
            finally:
                progress_bar.empty()
                status.empty() 
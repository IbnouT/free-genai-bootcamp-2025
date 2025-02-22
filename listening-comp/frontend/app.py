"""
Main Streamlit application for the Language Listening App.
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_path = str(Path(__file__).parent.parent / 'backend')
sys.path.append(backend_path)

import streamlit as st
from transcript_extractor import get_transcript
from llm_data_generator import generate_learning_content

# Set page config
st.set_page_config(
    page_title="Language Listening App",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 45px;
        margin-top: 25px;
    }
    /* Dark theme adjustments */
    [data-testid="stAppViewContainer"] {
        color: var(--text-color);
    }
    .transcript-container {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .transcript-text {
        font-size: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        color: var(--text-color);
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .video-info {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 1rem;
        color: var(--text-color);
    }
    div[data-testid="stHorizontalBlock"] {
        align-items: flex-end;
    }
    /* Input field dark theme fix */
    .stTextInput input {
        color: var(--text-color);
        background-color: rgba(255, 255, 255, 0.1);
    }
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    /* Success message dark theme fix */
    .stSuccess {
        background-color: rgba(40, 167, 69, 0.2);
        border-color: rgb(40, 167, 69);
    }
    /* Warning message dark theme fix */
    .stWarning {
        background-color: rgba(255, 193, 7, 0.2);
        border-color: rgb(255, 193, 7);
    }
    /* Error message dark theme fix */
    .stError {
        background-color: rgba(220, 53, 69, 0.2);
        border-color: rgb(220, 53, 69);
    }
    /* Debug info styling */
    .debug-info {
        font-family: monospace;
        font-size: 14px;
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.1);
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def display_debug_info(debug_info: dict):
    """Display debug information in a collapsible section."""
    with st.expander("🔍 Debug Information"):
        st.markdown("### API Request Details")
        st.markdown("**Model Used:** " + debug_info['model_used'])
        if debug_info.get('token_usage'):
            st.markdown("**Token Usage:** " + str(debug_info['token_usage']))
        
        st.markdown("### Prompt Used")
        st.code(debug_info['prompt_used'], language='markdown')
        
        st.markdown("### Raw LLM Response")
        if debug_info.get('raw_response'):
            st.code(debug_info['raw_response'], language='json')
        
        if debug_info.get('error_details'):
            st.markdown("### Error Details")
            st.error(debug_info['error_details'])

def display_learning_content(content: list):
    """Display the parsed learning content."""
    for i, section in enumerate(content, 1):
        st.markdown(f"### Dialog Section {i}")
        
        # Display dialog
        with st.container():
            st.markdown("#### Conversation")
            for speaker, text in section['dialogue']:
                st.markdown(f"**{speaker}:** {text}")
        
        # Display question and answers
        st.markdown("#### Question")
        st.markdown(section['question'])
        
        # Display answers as radio buttons
        st.markdown("#### Options")
        answer_options = section['answers']
        selected_answer = st.radio(
            "Select your answer:",
            options=range(len(answer_options)),
            format_func=lambda x: f"{chr(65+x)}. {answer_options[x]}",
            key=f"question_{i}"
        )
        
        # Show if answer is correct
        if st.button("Check Answer", key=f"check_{i}"):
            if selected_answer == section['correct_answer_index']:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is: {answer_options[section['correct_answer_index']]}")
        
        st.markdown("---")

def main():
    # Header with app title and description
    st.title("🎧 Language Listening App")
    st.markdown("""
    ### Improve your French listening skills with YouTube videos
    Enter a YouTube video URL below to get started. The app will fetch the French transcript 
    for your learning session.
    """)
    
    # Create two columns for input
    col1, col2 = st.columns([4, 1])
    
    # Input for YouTube URL
    with col1:
        youtube_url = st.text_input(
            "Enter YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )
    
    # Fetch button
    with col2:
        fetch_button = st.button("📝 Fetch Transcript")
    
    if fetch_button:
        if youtube_url:
            with st.spinner("Fetching transcript..."):
                # Get transcript
                transcript_result = get_transcript(youtube_url)
                
                if transcript_result['success']:
                    st.success("✨ Transcript fetched successfully!")
                    
                    # Generate learning content
                    with st.spinner("Generating learning content..."):
                        result = generate_learning_content(transcript_result['transcript'])
                        
                        if result['success']:
                            # Video info section
                            st.markdown("### 📺 Video Information")
                            with st.container():
                                st.markdown(f"""
                                <div class="video-info">
                                    <strong>Source:</strong> {youtube_url}<br>
                                    <strong>Language:</strong> French
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Toggle between original and parsed content
                            view_mode = st.radio(
                                "Select View Mode:",
                                ["Parsed Content", "Original Transcript"],
                                horizontal=True
                            )
                            
                            if view_mode == "Parsed Content":
                                display_learning_content(result['content'])
                            else:
                                st.markdown("### 📜 Original Transcript")
                                with st.container():
                                    st.markdown("""
                                    <div class="transcript-container">
                                        <div class="transcript-text">
                                        {}
                                        </div>
                                    </div>
                                    """.format(result['debug_info']['original_transcript'].replace('\n', '<br>')), 
                                    unsafe_allow_html=True)
                            
                            # Debug information
                            display_debug_info(result['debug_info'])
                            
                        else:
                            st.error(f"❌ Error generating learning content: {result['error']}")
                else:
                    st.error(f"❌ Error fetching transcript: {transcript_result['error']}")
        else:
            st.warning("⚠️ Please enter a YouTube URL")

if __name__ == "__main__":
    main() 
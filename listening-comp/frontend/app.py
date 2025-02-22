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

# Set page config
st.set_page_config(
    page_title="Language Listening App",
    page_icon="🎧",
    layout="wide"
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
    .transcript-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .transcript-text {
        font-size: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .video-info {
        background-color: #e1e5eb;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    div[data-testid="stHorizontalBlock"] {
        align-items: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)

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
                result = get_transcript(youtube_url)
                
                if result['success']:
                    st.success("✨ Transcript fetched successfully!")
                    
                    # Video info section
                    st.markdown("### 📺 Video Information")
                    with st.container():
                        st.markdown(f"""
                        <div class="video-info">
                            <strong>Source:</strong> {youtube_url}<br>
                            <strong>Language:</strong> French
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Transcript display
                    st.markdown("### 📜 Transcript")
                    with st.container():
                        st.markdown("""
                        <div class="transcript-container">
                            <div class="transcript-text">
                            {}
                            </div>
                        </div>
                        """.format(result['transcript'].replace('\n', '<br>')), 
                        unsafe_allow_html=True)
                    
                    # Learning tips
                    with st.expander("💡 Learning Tips"):
                        st.markdown("""
                        - Listen to the video while reading the transcript
                        - Try to understand the context before looking at the transcript
                        - Practice speaking by repeating after the audio
                        - Note down new vocabulary and expressions
                        """)
                else:
                    st.error(f"❌ Error fetching transcript: {result['error']}")
        else:
            st.warning("⚠️ Please enter a YouTube URL")

if __name__ == "__main__":
    main() 
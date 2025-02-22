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
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎧 Language Listening App")
    st.markdown("### YouTube Transcript Extractor")
    
    # Input for YouTube URL
    youtube_url = st.text_input(
        "Enter YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )
    
    if st.button("Fetch Transcript"):
        if youtube_url:
            with st.spinner("Fetching transcript..."):
                result = get_transcript(youtube_url)
                
                if result['success']:
                    st.success("Transcript fetched successfully!")
                    st.markdown("### Transcript")
                    st.text_area(
                        "Video Transcript",
                        value=result['transcript'],
                        height=400,
                        disabled=True
                    )
                else:
                    st.error(f"Error fetching transcript: {result['error']}")
        else:
            st.warning("Please enter a YouTube URL")

if __name__ == "__main__":
    main() 
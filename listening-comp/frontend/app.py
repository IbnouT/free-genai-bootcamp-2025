"""
Main Streamlit application for the Language Listening App.
"""
import sys
import os
from pathlib import Path
import json

# Add backend directory to Python path
backend_path = str(Path(__file__).parent.parent / 'backend')
sys.path.append(backend_path)

import streamlit as st
from transcript_extractor import get_transcript
from timestamp_extractor import extract_sequence_timestamps
from audio_segmenter import segment_audio
from audio_transcriber import transcribe_audio_segments

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
    /* Pipeline stages styling */
    .pipeline-stage {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .stage-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .stage-content {
        font-family: monospace;
        font-size: 14px;
        white-space: pre-wrap;
    }
    /* Audio player styling */
    .audio-player {
        width: 100%;
        margin: 10px 0;
    }
    /* Success/error message styling */
    .success-message {
        color: #28a745;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        color: #dc3545;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    /* Transcript display styling */
    .transcript-display {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def format_transcript(transcript):
    """Format transcript segments for display."""
    formatted = []
    for segment in transcript:
        start_time = int(segment['start'])
        minutes = start_time // 60
        seconds = start_time % 60
        timestamp = f"{minutes:02d}:{seconds:02d}"
        formatted.append(f"[{timestamp}] {segment['text']}")
    return "\n".join(formatted)

def process_video(youtube_url: str):
    """Process a YouTube video through the pipeline."""
    with st.spinner("Processing video..."):
        # Step 1: Get transcript
        st.markdown("### Step 1: Transcript Extraction")
        with st.expander("Show Details", expanded=True):
            transcript_result = get_transcript(youtube_url)
            if not transcript_result['success']:
                st.error(f"❌ Error fetching transcript: {transcript_result['error']}")
                return
            st.success("✅ Transcript fetched successfully")
            
            # Display full transcript in a scrollable area
            st.markdown("**Full Transcript:**")
            st.markdown('<div class="transcript-display">', unsafe_allow_html=True)
            st.text(format_transcript(transcript_result['transcript']))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 2: Extract timestamps
        st.markdown("### Step 2: Timestamp Extraction")
        with st.expander("Show Details", expanded=True):
            try:
                timestamps = extract_sequence_timestamps(transcript_result['transcript'])
                if timestamps:
                    st.success(f"✅ Found {len(timestamps)} sequences")
                    for i, (start, end) in enumerate(timestamps, 1):
                        st.text(f"Sequence {i}: {start} -> {end}")
                else:
                    st.warning("⚠️ No sequences found. The video might be too short or have insufficient gaps.")
            except Exception as e:
                st.error(f"❌ Error extracting timestamps: {str(e)}")
                return
        
        # Step 3: Segment audio
        st.markdown("### Step 3: Audio Segmentation")
        with st.expander("Show Details", expanded=True):
            if not timestamps:
                st.error("❌ Cannot proceed with audio segmentation: No timestamps available")
                return
                
            video_id = youtube_url.split('v=')[-1]
            output_folder = segment_audio(video_id, timestamps)
            
            if not output_folder:
                st.error("❌ Audio segmentation failed")
                return
                
            st.success("✅ Audio segments created")
            st.text("Generated audio files:")
            for file in os.listdir(output_folder):
                st.text(f"  - {file}")
                if file.endswith('.mp3'):
                    with open(os.path.join(output_folder, file), 'rb') as f:
                        st.audio(f.read(), format='audio/mp3')
        
        # Step 4: Transcribe audio segments
        st.markdown("### Step 4: Audio Transcription")
        with st.expander("Show Details", expanded=True):
            transcriptions = transcribe_audio_segments(output_folder)
            
            if "error" in transcriptions:
                st.error(f"❌ Transcription failed: {transcriptions['error']}")
                return
            
            st.success("✅ Transcription completed")
            for filename, transcript in transcriptions.items():
                st.markdown(f"**{filename}:**")
                if transcript.startswith("ERROR:"):
                    st.error(transcript)
                else:
                    st.text(transcript)

def main():
    st.title("🎧 Language Listening App - Pipeline Testing")
    st.markdown("""
    ### Test the audio processing pipeline
    Enter a YouTube video URL below to process it through the pipeline:
    1. Transcript extraction
    2. Timestamp extraction
    3. Audio segmentation
    4. Audio transcription
    """)
    
    # YouTube URL input
    youtube_url = st.text_input(
        "Enter YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )
    
    # Process button
    if st.button("🚀 Process Video"):
        if youtube_url:
            process_video(youtube_url)
        else:
            st.warning("⚠️ Please enter a YouTube URL")

if __name__ == "__main__":
    main() 
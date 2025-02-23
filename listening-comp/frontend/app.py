"""
Main Streamlit application for the Language Listening App.
"""
import sys
import os
from pathlib import Path
import json
import time
import logging

# Add backend directory to Python path
backend_path = str(Path(__file__).parent.parent / 'backend')
sys.path.append(backend_path)

import streamlit as st
from transcript_extractor import get_transcript
from timestamp_extractor import extract_sequence_timestamps
from audio_segmenter import segment_audio
from audio_transcriber import transcribe_audio_segments
from llm_data_generator import generate_learning_content
from test_modules import setup_logging

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
    /* Step header styling */
    .step-header {
        display: flex;
        align-items: center;
        gap: 10px;
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

def sort_sequence_files(files):
    """Sort files by sequence number."""
    def get_sequence_num(filename):
        try:
            # Extract sequence number from filename (e.g., 'video_id_sequence_1.mp3' -> 1)
            return int(filename.split('sequence_')[-1].split('.')[0])
        except:
            return float('inf')  # Put files without sequence number at the end
    return sorted(files, key=get_sequence_num)

def process_video(youtube_url: str, debug: bool = False):
    """Process a YouTube video through the pipeline."""
    
    # Set up logging based on debug mode
    setup_logging(debug)
    
    # Step 1: Get transcript
    st.markdown(
        '<div class="step-header">'
        '<h3>Step 1: Transcript Extraction</h3>'
        '<div class="step-spinner"></div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Extracting transcript..."):
        with st.expander("Show Details", expanded=False):
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
    st.markdown(
        '<div class="step-header">'
        '<h3>Step 2: Timestamp Extraction</h3>'
        '<div class="step-spinner"></div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Extracting timestamps..."):
        with st.expander("Show Details", expanded=False):
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
    st.markdown(
        '<div class="step-header">'
        '<h3>Step 3: Audio Segmentation</h3>'
        '<div class="step-spinner"></div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Segmenting audio..."):
        with st.expander("Show Details", expanded=False):
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
    st.markdown(
        '<div class="step-header">'
        '<h3>Step 4: Audio Transcription</h3>'
        '<div class="step-spinner"></div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Transcribing audio segments..."):
        with st.expander("Show Details", expanded=False):
            transcriptions = transcribe_audio_segments(output_folder)
            
            if "error" in transcriptions:
                st.error(f"❌ Transcription failed: {transcriptions['error']}")
                return
                
            st.success("✅ Transcription completed")
            
            # Sort filenames by sequence number
            sorted_filenames = sort_sequence_files(transcriptions.keys())
            
            # Display transcripts in sequence order
            for filename in sorted_filenames:
                transcript = transcriptions[filename]
                # Extract sequence number for display
                seq_num = filename.split('sequence_')[-1].split('.')[0]
                st.markdown(f"**Sequence {seq_num}:**")
                if transcript.startswith("ERROR:"):
                    st.error(transcript)
                else:
                    st.text(transcript)
                    
                # Add a separator between sequences
                st.markdown("---")

    # Step 5: Generate TCF Exercises
    st.markdown(
        '<div class="step-header">'
        '<h3>Step 5: TCF Exercise Generation</h3>'
        '<div class="step-spinner"></div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.spinner("Generating TCF exercises..."):
        with st.expander("Show Details", expanded=False):
            if "error" in transcriptions:
                st.error("❌ Cannot generate exercises: No transcriptions available")
                return
                
            st.info("🤖 Generating TCF-style exercises using AI...")
            
            # Sort filenames by sequence number
            sorted_filenames = sort_sequence_files(transcriptions.keys())
            
            # Generate exercises for each sequence
            for filename in sorted_filenames:
                transcript = transcriptions[filename]
                if transcript.startswith("ERROR:"):
                    continue
                    
                # Extract sequence number for display
                seq_num = filename.split('sequence_')[-1].split('.')[0]
                st.markdown(f"**Sequence {seq_num}:**")
                
                # Generate exercise
                result = generate_learning_content(transcript)
                
                if result['success']:
                    # The content is a list of exercises, but we'll use just the first one
                    # since we're processing segment by segment
                    exercise = result['content'][0] if result['content'] else None
                    
                    if exercise:
                        # Display dialogue
                        st.markdown("**Dialogue:**")
                        for speaker, text in exercise['dialogue']:
                            st.markdown(f"**{speaker}:** {text}")
                            
                        # Display question and answers
                        st.markdown("\n**Question:**")
                        st.markdown(exercise['question'])
                        
                        st.markdown("\n**Options:**")
                        for i, answer in enumerate(exercise['answers']):
                            if i == exercise['correct_answer_index']:
                                st.markdown(f"✅ {chr(65+i)}. {answer}")
                            else:
                                st.markdown(f"⬜ {chr(65+i)}. {answer}")
                                
                        # Display speakers info if available
                        if 'speakers_info' in exercise:
                            st.markdown("\n**Locuteurs identifiés:**")
                            st.markdown(", ".join(exercise['speakers_info']))
                            
                        # Display debug info in columns if available
                        if 'debug_info' in result:
                            st.markdown("---")
                            st.markdown("**🔍 Debug Information**")
                            cols = st.columns(2)
                            with cols[0]:
                                st.markdown("**Model Used:**")
                                st.code(result['debug_info'].get('model_used', 'N/A'))
                                if 'token_usage' in result['debug_info']:
                                    st.markdown("**Token Usage:**")
                                    st.json(result['debug_info']['token_usage'])
                            with cols[1]:
                                st.markdown("**Original Transcript:**")
                                st.text_area("", result['debug_info'].get('original_transcript', 'N/A'), height=100, key=f"debug_transcript_{seq_num}")
                    else:
                        st.error("❌ No exercise generated for this segment")
                else:
                    st.error(f"❌ Failed to generate exercise: {result['error']}")
                    # Display error debug info in columns
                    if 'debug_info' in result:
                        st.markdown("---")
                        st.markdown("**🔍 Error Debug Information**")
                        cols = st.columns(2)
                        with cols[0]:
                            st.markdown("**Error Type:**")
                            st.code(result['debug_info'].get('error_type', 'Unknown'))
                            st.markdown("**Error Details:**")
                            st.code(result['debug_info'].get('error_details', 'No details available'))
                        with cols[1]:
                            st.markdown("**Original Transcript:**")
                            st.text_area("", result['debug_info'].get('original_transcript', 'N/A'), height=100, key=f"error_transcript_{seq_num}")
                
                # Add a separator between sequences
                st.markdown("---")
            
            st.success("✅ Exercise generation completed")

def main():
    st.title("🎧 Language Listening App - Pipeline Testing")
    st.markdown("""
    ### Test the audio processing pipeline
    Enter a YouTube video URL below to process it through the pipeline:
    1. Transcript extraction
    2. Timestamp extraction
    3. Audio segmentation
    4. Audio transcription
    5. TCF exercise generation
    """)
    
    # Add debug mode toggle
    debug_mode = st.sidebar.checkbox("Enable Debug Output", value=False, help="Show detailed debug logs")
    
    # YouTube URL input
    youtube_url = st.text_input(
        "Enter YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )
    
    # Process button
    if st.button("🚀 Process Video"):
        if youtube_url:
            process_video(youtube_url, debug=debug_mode)
        else:
            st.warning("⚠️ Please enter a YouTube URL")

if __name__ == "__main__":
    main() 
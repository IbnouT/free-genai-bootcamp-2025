"""
Module for transcribing audio segments using OpenAI's Whisper API.
"""
from typing import Dict, Optional
import os
import logging
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()  # The API key will be automatically loaded from OPENAI_API_KEY environment variable

def transcribe_audio_segments(segmented_audio_folder: str) -> Dict[str, str]:
    """
    Transcribe all audio segments in the given folder using Whisper API.
    
    Args:
        segmented_audio_folder (str): Path to folder containing segmented audio files
        
    Returns:
        Dict[str, str]: Dictionary mapping audio filenames to their transcripts
    """
    try:
        transcriptions = {}
        audio_files = [f for f in os.listdir(segmented_audio_folder) if f.endswith('.mp3')]
        
        for audio_filename in audio_files:
            audio_filepath = os.path.join(segmented_audio_folder, audio_filename)
            try:
                logger.info(f"Transcribing {audio_filename}...")
                
                with open(audio_filepath, "rb") as audio_file:
                    transcript_response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="fr",  # Explicitly specify French
                        response_format="text"  # Get plain text response
                    )
                    
                    # Store the transcript
                    transcriptions[audio_filename] = transcript_response
                    logger.info(f"Successfully transcribed {audio_filename}")
                    
            except Exception as e:
                logger.error(f"Error transcribing {audio_filename}: {str(e)}")
                # Store error message in transcriptions
                transcriptions[audio_filename] = f"ERROR: {str(e)}"
                continue
        
        return transcriptions
        
    except Exception as e:
        logger.error(f"Error in transcribe_audio_segments: {str(e)}")
        return {"error": str(e)}

def validate_audio_file(file_path: str) -> Optional[str]:
    """
    Validate that an audio file exists and is accessible.
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        Optional[str]: Error message if validation fails, None if successful
    """
    if not os.path.exists(file_path):
        return f"Audio file not found: {file_path}"
    
    if not os.path.isfile(file_path):
        return f"Path is not a file: {file_path}"
    
    if not os.access(file_path, os.R_OK):
        return f"Audio file is not readable: {file_path}"
    
    return None 
"""
Module for extracting transcripts from YouTube videos.
"""
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from typing import Optional, Dict, Any, List
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.

    Args:
        url (str): YouTube video URL

    Returns:
        Optional[str]: Video ID if found, None otherwise
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(url: str) -> Dict[str, Any]:
    """
    Fetch French transcript from YouTube video URL.

    Args:
        url (str): YouTube video URL

    Returns:
        Dict[str, Any]: Dictionary containing:
            - success (bool): Whether the operation was successful
            - error (Optional[str]): Error message if any
            - transcript (Optional[List[Dict]]): List of transcript segments with timestamps if successful
                Each segment is a dict with:
                - text (str): The transcript text
                - start (float): Start time in seconds
                - duration (float): Duration in seconds
    """
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return {
                'success': False,
                'error': 'Invalid YouTube URL',
                'transcript': None
            }

        try:
            # Get raw transcript with timestamps
            logger.debug(f"Fetching transcript for video ID: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])
            
            # Log transcript structure
            if transcript:
                logger.debug(f"Transcript structure (first entry): {transcript[0]}")
                logger.debug(f"Number of transcript entries: {len(transcript)}")
            
            return {
                'success': True,
                'error': None,
                'transcript': transcript  # Return raw transcript with timestamps
            }

        except TranscriptsDisabled:
            logger.error("Transcripts are disabled for this video")
            return {
                'success': False,
                'error': 'Transcripts are disabled for this video',
                'transcript': None
            }
        except Exception as e:
            logger.error(f"Error fetching transcripts: {str(e)}")
            return {
                'success': False,
                'error': f'Error fetching transcripts: {str(e)}',
                'transcript': None
            }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'transcript': None
        }
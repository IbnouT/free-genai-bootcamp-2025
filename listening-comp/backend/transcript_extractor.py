"""
Module for extracting transcripts from YouTube videos.
"""
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from typing import Optional, Dict, Any
import re

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

def get_transcript(url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch transcript from YouTube video URL.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing transcript text and status,
                                 or None if extraction fails
    """
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return {
                'success': False,
                'error': 'Invalid YouTube URL',
                'transcript': None
            }
            
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)
        
        return {
            'success': True,
            'error': None,
            'transcript': transcript_text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'transcript': None
        } 
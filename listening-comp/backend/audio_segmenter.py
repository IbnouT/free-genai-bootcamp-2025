"""
Module for downloading and segmenting audio from YouTube videos.
"""
from typing import List, Tuple, Optional
import os
from pydub import AudioSegment
from datetime import datetime
import yt_dlp

def timestamp_to_milliseconds(timestamp_str: str) -> int:
    """
    Convert a timestamp string "MM:SS" to milliseconds.
    
    Args:
        timestamp_str (str): Timestamp string in format "MM:SS"
        
    Returns:
        int: Time in milliseconds
    """
    try:
        minutes, seconds = map(int, timestamp_str.split(':'))
        return (minutes * 60 + seconds) * 1000
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}. Expected format: 'MM:SS'")

def segment_audio(
    video_id: str,
    sequence_timestamps: List[Tuple[str, str]],
    output_folder: str = "segmented_audio"
) -> Optional[str]:
    """
    Download audio from YouTube video and segment it based on timestamps.
    
    Args:
        video_id (str): YouTube video ID
        sequence_timestamps (List[Tuple[str, str]]): List of (start, end) timestamp tuples
        output_folder (str): Path to folder where segments will be saved
        
    Returns:
        Optional[str]: Path to the output folder if successful, None if failed
    """
    try:
        # Create output folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_folder = os.path.join(output_folder, f"{video_id}_{timestamp}")
        os.makedirs(video_folder, exist_ok=True)
        print(f"Created output folder: {video_folder}")

        # Configure yt-dlp with simple options (from fetch_v4.py)
        base_filename = f"{video_id}"  # without extension
        audio_file = os.path.join(video_folder, f"{base_filename}.mp3")
        print(f"Will download to: {audio_file}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(video_folder, base_filename),  # yt-dlp will add .mp3.mp3
            'quiet': False  # Enable output for debugging
        }

        # Download audio using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
            except Exception as e:
                raise Exception(f"Failed to download audio: {str(e)}")

        print(f"Directory contents: {os.listdir(video_folder)}")
        
        # Find the actual audio file (it might have .mp3.mp3 extension)
        actual_audio_file = None
        for file in os.listdir(video_folder):
            if file.startswith(base_filename) and file.endswith('.mp3'):
                actual_audio_file = os.path.join(video_folder, file)
                break

        if not actual_audio_file or not os.path.exists(actual_audio_file):
            raise Exception(f"Audio file not found in {video_folder}")

        print(f"Found audio file at: {actual_audio_file}")

        # Load the audio file
        audio = AudioSegment.from_mp3(actual_audio_file)

        # Segment the audio
        for i, (start_time, end_time) in enumerate(sequence_timestamps, 1):
            # Convert timestamps to milliseconds
            start_ms = timestamp_to_milliseconds(start_time)
            end_ms = timestamp_to_milliseconds(end_time)

            # Extract segment
            segment = audio[start_ms:end_ms]

            # Save segment
            segment_filename = f"{video_id}_sequence_{i}.mp3"
            segment_path = os.path.join(video_folder, segment_filename)
            segment.export(segment_path, format="mp3")

        # Clean up the full audio file
        os.remove(actual_audio_file)

        return video_folder

    except Exception as e:
        print(f"Error in audio segmentation: {str(e)}")
        # Print current working directory and file existence for debugging
        print(f"Current working directory: {os.getcwd()}")
        if 'video_folder' in locals():
            print(f"Video folder exists: {os.path.exists(video_folder)}")
            if os.path.exists(video_folder):
                print(f"Video folder contents: {os.listdir(video_folder)}")
        return None 
"""
Simple test script for timestamp extraction and audio segmentation.
"""
from transcript_extractor import get_transcript
from timestamp_extractor import extract_sequence_timestamps
from audio_segmenter import segment_audio
import os

def test_pipeline(youtube_url: str):
    print(f"Testing pipeline with URL: {youtube_url}")
    
    # Step 1: Get transcript
    print("\n1. Getting transcript...")
    result = get_transcript(youtube_url)
    if not result['success']:
        print(f"Error getting transcript: {result['error']}")
        return
    
    print("✓ Transcript fetched successfully")
    
    # Step 2: Extract timestamps
    print("\n2. Extracting timestamps...")
    timestamps = extract_sequence_timestamps(result['transcript'])
    print(f"Found {len(timestamps)} sequences:")
    for i, (start, end) in enumerate(timestamps, 1):
        print(f"  Sequence {i}: {start} -> {end}")
    
    # Step 3: Segment audio
    print("\n3. Segmenting audio...")
    video_id = youtube_url.split('v=')[-1]
    output_folder = segment_audio(video_id, timestamps)
    
    if output_folder:
        abs_path = os.path.abspath(output_folder)
        print(f"✓ Audio segments saved to: {abs_path}")
        print(f"Contents of the output folder:")
        for file in os.listdir(output_folder):
            print(f"  - {file}")
    else:
        print("✗ Audio segmentation failed")

if __name__ == "__main__":
    # Replace with your test YouTube URL
    TEST_URL = "https://www.youtube.com/watch?v=_O3AMgo5lOQ"
    print("Enter a YouTube URL (or press Enter to use default):")
    url = input().strip() or TEST_URL
    test_pipeline(url) 
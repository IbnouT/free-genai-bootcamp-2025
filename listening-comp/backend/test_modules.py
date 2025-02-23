"""
Simple test script for timestamp extraction, audio segmentation, and transcription.
"""
from transcript_extractor import get_transcript
from timestamp_extractor import extract_sequence_timestamps
from audio_segmenter import segment_audio
from audio_transcriber import transcribe_audio_segments
import os
import json

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
    
    if not output_folder:
        print("✗ Audio segmentation failed")
        return
        
    abs_path = os.path.abspath(output_folder)
    print(f"✓ Audio segments saved to: {abs_path}")
    print(f"Contents of the output folder:")
    for file in os.listdir(output_folder):
        print(f"  - {file}")
    
    # Step 4: Transcribe audio segments
    print("\n4. Transcribing audio segments...")
    transcriptions = transcribe_audio_segments(output_folder)
    
    if "error" in transcriptions:
        print(f"✗ Transcription failed: {transcriptions['error']}")
        return
        
    print("✓ Transcription completed")
    print("\nTranscription results:")
    for filename, transcript in transcriptions.items():
        if transcript.startswith("ERROR:"):
            print(f"\n❌ {filename}:")
            print(f"  {transcript}")
        else:
            print(f"\n✓ {filename}:")
            print(f"  {transcript[:200]}..." if len(transcript) > 200 else transcript)
    
    # Save results to a JSON file for reference
    results_file = os.path.join(output_folder, "transcription_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(transcriptions, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed results saved to: {results_file}")

if __name__ == "__main__":
    # Replace with your test YouTube URL
    TEST_URL = "https://www.youtube.com/watch?v=_O3AMgo5lOQ"
    print("Enter a YouTube URL (or press Enter to use default):")
    url = input().strip() or TEST_URL
    test_pipeline(url) 
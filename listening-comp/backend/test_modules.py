"""
Simple test script for the complete audio processing and data management pipeline.
"""
from transcript_extractor import get_transcript
from timestamp_extractor import extract_sequence_timestamps
from audio_segmenter import segment_audio
from audio_transcriber import transcribe_audio_segments
from data_manager import DataManager
import os
import json

def test_pipeline(youtube_url: str):
    print(f"Testing pipeline with URL: {youtube_url}")
    
    # Initialize DataManager
    print("\nInitializing DataManager...")
    data_manager = DataManager()
    print("✓ DataManager initialized")
    
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
    
    # Step 5: Save data to Vector DB and permanent storage
    print("\n5. Saving data to Vector DB and permanent storage...")
    # TODO: Create JSON sequences from transcriptions
    # For now, we'll use a simple structure for testing
    sequences_json_list = []
    for i, (filename, transcript) in enumerate(transcriptions.items()):
        if not transcript.startswith("ERROR:"):
            sequence_json = {
                "dialogue": [["Speaker", transcript]],
                "question": "Sample question for testing",
                "answers": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "correct_answer_index": 0
            }
            sequences_json_list.append(sequence_json)
    
    save_result = data_manager.save_video_data(
        youtube_url=youtube_url,
        sequences_json_list=sequences_json_list,
        audio_segments_folder_path=output_folder
    )
    
    if save_result['success']:
        print(f"✓ Data saved successfully")
        print(f"  Video ID: {save_result['video_id']}")
        print(f"  Timestamp: {save_result['timestamp']}")
        print(f"  Number of sequences: {save_result['num_sequences']}")
        
        # Test topic-based retrieval
        print("\n6. Testing topic-based retrieval...")
        test_topic = "conversation"  # Generic topic for testing
        exercises = data_manager.get_exercises_by_topic(test_topic, num_exercises=2)
        print(f"Retrieved {len(exercises)} exercises for topic '{test_topic}'")
        for i, exercise in enumerate(exercises, 1):
            print(f"\nExercise {i}:")
            print(f"  Question: {exercise['question']}")
            print(f"  Audio file: {exercise['audio_file']}")
    else:
        print(f"✗ Failed to save data: {save_result['error']}")

if __name__ == "__main__":
    # Replace with your test YouTube URL
    TEST_URL = "https://www.youtube.com/watch?v=_O3AMgo5lOQ"
    print("Enter a YouTube URL (or press Enter to use default):")
    url = input().strip() or TEST_URL
    test_pipeline(url) 
"""
Simple test script for the complete audio processing and data management pipeline.
"""
from transcript_extractor import get_transcript
from timestamp_extractor import extract_sequence_timestamps
from audio_segmenter import segment_audio
from audio_transcriber import transcribe_audio_segments
from llm_data_generator import generate_learning_content
from data_manager import DataManager
import os
import json
from pprint import pprint
import logging

def setup_logging(debug: bool):
    """Configure logging based on debug mode."""
    # Configure root logger to only show WARNING and above
    logging.getLogger().setLevel(logging.WARNING)
    
    # Configure format to only show the message
    logging.basicConfig(format='%(message)s')
    
    # Silence third-party loggers completely unless in debug mode
    if not debug:
        logging.getLogger("openai").setLevel(logging.ERROR)
        logging.getLogger("httpx").setLevel(logging.ERROR)
        logging.getLogger("httpcore").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)

def print_separator():
    """Print a separator line."""
    print("\n" + "-"*40 + "\n")

def test_pipeline(youtube_url: str, debug: bool = False):
    """
    Test the complete pipeline.
    
    Args:
        youtube_url (str): URL of the YouTube video to process
        debug (bool): Whether to show detailed debug information
    """
    # Set up logging based on debug mode
    setup_logging(debug)
    
    print(f"Testing pipeline with URL: {youtube_url}")
    print_separator()
    
    # Step 1: Get transcript
    print("1. Getting transcript...")
    result = get_transcript(youtube_url)
    if not result['success']:
        print(f"Error getting transcript: {result['error']}")
        return
    
    print("✓ Transcript fetched successfully")
    print("\nFirst few lines of transcript:")
    for segment in result['transcript'][:3]:
        print(f"[{int(segment['start'])}s] {segment['text']}")
    print_separator()
    
    # Step 2: Extract timestamps
    print("2. Extracting timestamps...")
    timestamps = extract_sequence_timestamps(result['transcript'])
    print(f"Found {len(timestamps)} sequences")
    for i, (start, end) in enumerate(timestamps, 1):
        print(f"  Sequence {i}: {start} -> {end}")
    print_separator()
    
    # Step 3: Segment audio
    print("3. Segmenting audio...")
    video_id = youtube_url.split('v=')[-1]
    output_folder = segment_audio(video_id, timestamps)
    
    if not output_folder:
        print("✗ Audio segmentation failed")
        return
        
    abs_path = os.path.abspath(output_folder)
    print(f"✓ Audio segments saved to: {abs_path}")
    print("Contents of the output folder:")
    for file in os.listdir(output_folder):
        print(f"  - {file}")
    print_separator()
    
    # Step 4: Transcribe audio segments
    print("4. Transcribing audio segments...")
    transcriptions = transcribe_audio_segments(output_folder)
    
    if "error" in transcriptions:
        print(f"✗ Transcription failed: {transcriptions['error']}")
        return
        
    print("✓ Transcription completed")
    print("\nTranscription results:")
    for filename, transcript in transcriptions.items():
        print(f"\n[{filename}]")
        if transcript.startswith("ERROR:"):
            print(f"❌ {transcript}")
        else:
            print(f"✓ {transcript[:200]}..." if len(transcript) > 200 else transcript)
    print_separator()
    
    # Step 5: Generate TCF Exercises
    print("5. Generating TCF exercises...")
    successful_exercises = 0
    failed_exercises = 0
    exercises_data = []
    
    for filename, transcript in transcriptions.items():
        if transcript.startswith("ERROR:"):
            continue
            
        print(f"\n📝 Processing {filename}...")
        print("-" * 40)
        
        # Generate exercise
        result = generate_learning_content(transcript)
        
        if not result['success']:
            failed_exercises += 1
            print(f"❌ Exercise generation failed: {result['error']}")
            if 'debug_info' in result and 'raw_response' in result['debug_info']:
                print("\nRaw LLM Response:")
                print("-" * 20)
                print(result['debug_info']['raw_response'])
                print("-" * 20)
            continue
            
        # Get the first (and only) exercise from the list
        exercise = result['content'][0] if result['content'] else None
        
        if exercise:
            successful_exercises += 1
            exercises_data.append(exercise)
            print("\n✅ Exercise Generated Successfully")
            
            print("\n🏷️ Topics & Level:")
            print(f"Topics: {', '.join(exercise['topics'])}")
            print(f"Difficulty Level: {exercise['difficulty_level']}")
            
            print("\nDialogue:")
            for speaker, text in exercise['dialogue']:
                print(f"{speaker}: {text}")
            
            print("\nQuestion:")
            print(exercise['question'])
            
            print("\nAnswer Options:")
            for i, answer in enumerate(exercise['answers']):
                correct = "✓" if i == exercise['correct_answer_index'] else " "
                print(f"[{correct}] {chr(65+i)}. {answer}")
            
            if 'speakers_info' in exercise:
                print("\nSpeakers:")
                print(", ".join(exercise['speakers_info']))
        else:
            failed_exercises += 1
            print(f"❌ Failed to generate exercise for sequence {filename}")
            if 'debug_info' in result:
                print("\nDebug Info:")
                pprint(result['debug_info'])
        
        print("-" * 40)
    
    # Print summary
    print(f"\nExercise Generation Summary:")
    print(f"✓ Successful exercises: {successful_exercises}")
    print(f"❌ Failed exercises: {failed_exercises}")
    print(f"Total sequences processed: {successful_exercises + failed_exercises}")
    
    # Save results to a JSON file for reference
    results_file = os.path.join(output_folder, "test_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'youtube_url': youtube_url,
            'video_id': video_id,
            'num_sequences': len(timestamps),
            'transcriptions': transcriptions,
            'exercises': exercises_data
        }, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed test results saved to: {results_file}")

def main():
    """Main function with argument parsing."""
    print("Language Listening App - Pipeline Test Script")
    print("=" * 50)
    print("\nThis script will test the complete pipeline.")
    print("Enter a YouTube URL to process (or press Enter for default test URL):")
    print("Default: https://www.youtube.com/watch?v=_O3AMgo5lOQ")
    
    url = input("\nYouTube URL: ").strip() or "https://www.youtube.com/watch?v=_O3AMgo5lOQ"
    
    debug_input = input("\nEnable debug output? (y/N): ").strip().lower()
    debug = debug_input == 'y'
    
    if debug:
        print("\nDebug mode enabled - showing detailed information")
    else:
        print("\nDebug mode disabled - showing only essential progress")
    
    test_pipeline(url, debug)

if __name__ == "__main__":
    main() 
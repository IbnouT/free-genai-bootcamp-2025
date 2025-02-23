"""
Module for extracting timestamp sequences from transcripts.
"""
from typing import List, Tuple, Dict, Any
from datetime import timedelta

def timedelta_to_timestamp(td: timedelta) -> str:
    """
    Convert a timedelta object to a timestamp string format "MM:SS".
    
    Args:
        td (timedelta): The timedelta object to convert
        
    Returns:
        str: Formatted timestamp string "MM:SS"
    """
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def timestamp_to_timedelta(timestamp_str: str) -> timedelta:
    """
    Convert a timestamp string "MM:SS" to a timedelta object.
    
    Args:
        timestamp_str (str): Timestamp string in format "MM:SS"
        
    Returns:
        timedelta: Corresponding timedelta object
    """
    try:
        minutes, seconds = map(int, timestamp_str.split(':'))
        return timedelta(minutes=minutes, seconds=seconds)
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}. Expected format: 'MM:SS'")

def extract_sequence_timestamps(
    transcript: List[Dict[str, Any]], 
    gap_threshold_seconds: int = 10,
    end_buffer_seconds: int = 10,
    min_entries: int = 2
) -> List[Tuple[str, str]]:
    """
    Extract sequence timestamps from transcript based on gaps between segments.
    
    Args:
        transcript (List[Dict[str, Any]]): List of transcript segments with timestamps
        gap_threshold_seconds (int): Minimum gap in seconds to consider as sequence boundary
        end_buffer_seconds (int): Number of seconds to add as buffer at sequence end
        min_entries (int): Minimum number of transcript entries required for a valid sequence
        
    Returns:
        List[Tuple[str, str]]: List of (start_timestamp, end_timestamp) tuples
    """
    if not transcript:
        return []

    sequence_timestamps = []
    current_sequence_start = timedelta(seconds=transcript[0]['start'])
    last_timestamp = current_sequence_start
    sequence_entries = 1  # Count entries in current sequence

    for i in range(1, len(transcript)):
        current_segment = transcript[i]
        current_timestamp = timedelta(seconds=current_segment['start'])
        gap = current_timestamp - last_timestamp

        # If gap exceeds threshold, check sequence length and start new one
        if gap.total_seconds() > gap_threshold_seconds:
            # Only add sequence if it has enough entries
            if sequence_entries >= min_entries:
                # Add buffer to sequence end
                buffered_end = last_timestamp + timedelta(seconds=end_buffer_seconds)
                
                sequence_timestamps.append((
                    timedelta_to_timestamp(current_sequence_start),
                    timedelta_to_timestamp(buffered_end)
                ))
            
            # Start new sequence
            current_sequence_start = current_timestamp
            sequence_entries = 1
        else:
            sequence_entries += 1

        last_timestamp = current_timestamp

    # Add the final sequence if it has enough entries
    if transcript and sequence_entries >= min_entries:
        last_segment = transcript[-1]
        final_end = timedelta(seconds=last_segment['start'] + last_segment['duration'])
        buffered_end = final_end + timedelta(seconds=end_buffer_seconds)
        
        sequence_timestamps.append((
            timedelta_to_timestamp(current_sequence_start),
            timedelta_to_timestamp(buffered_end)
        ))

    return sequence_timestamps 
"""
Module for managing data persistence and Vector DB integration.
"""
from typing import List, Dict, Any, Optional
import os
import json
import logging
from datetime import datetime
from pathlib import Path
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, base_dir: str = "data"):
        """
        Initialize DataManager with storage directories and ChromaDB client.
        
        Args:
            base_dir (str): Base directory for data storage
        """
        self.base_dir = Path(base_dir)
        self.audio_dir = self.base_dir / "audio"
        self.metadata_dir = self.base_dir / "metadata"
        self.db_dir = self.base_dir / "vectordb"
        
        # Create necessary directories
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.db_dir))
        
        # Use OpenAI's embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="french_listening_exercises",
            embedding_function=self.embedding_function,
            metadata={"description": "French listening comprehension exercises"}
        )
        
        logger.info("DataManager initialized successfully")

    def save_video_data(
        self,
        youtube_url: str,
        sequences_json_list: List[Dict[str, Any]],
        audio_segments_folder_path: str
    ) -> Dict[str, Any]:
        """
        Save processed video data including JSON sequences and audio files.
        
        Args:
            youtube_url (str): Source YouTube video URL
            sequences_json_list (List[Dict[str, Any]]): List of structured JSON objects for each sequence
            audio_segments_folder_path (str): Path to folder containing audio segments
            
        Returns:
            Dict[str, Any]: Status of the save operation
        """
        try:
            # Extract video ID from URL
            video_id = youtube_url.split('v=')[-1]
            
            # Create video-specific directories
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_dir = self.audio_dir / f"{video_id}_{timestamp}"
            video_dir.mkdir(parents=True, exist_ok=True)
            
            # Move audio segments to permanent storage
            audio_files = {}
            source_dir = Path(audio_segments_folder_path)
            for audio_file in source_dir.glob("*.mp3"):
                dest_path = video_dir / audio_file.name
                os.rename(audio_file, dest_path)
                audio_files[audio_file.name] = str(dest_path)
            
            # Save metadata
            metadata = {
                "youtube_url": youtube_url,
                "video_id": video_id,
                "processing_date": timestamp,
                "audio_files": audio_files
            }
            metadata_file = self.metadata_dir / f"{video_id}_{timestamp}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            # Add sequences to Vector DB
            for i, sequence_json in enumerate(sequences_json_list):
                # Create a summary of the dialogue for embedding
                dialogue_summary = " ".join([text for _, text in sequence_json['dialogue']])
                
                # Prepare document for Vector DB
                self.collection.add(
                    documents=[dialogue_summary],
                    metadatas=[{
                        "youtube_url": youtube_url,
                        "video_id": video_id,
                        "sequence_number": i + 1,
                        "audio_filename": f"{video_id}_sequence_{i+1}.mp3",
                        "timestamp": timestamp,
                        "json_data": json.dumps(sequence_json, ensure_ascii=False)
                    }],
                    ids=[f"{video_id}_sequence_{i+1}"]
                )
            
            logger.info(f"Successfully saved data for video {video_id}")
            return {
                "success": True,
                "video_id": video_id,
                "timestamp": timestamp,
                "num_sequences": len(sequences_json_list)
            }
            
        except Exception as e:
            logger.error(f"Error saving video data: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_exercises_by_topic(self, topic: str, num_exercises: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve exercise sequences from Vector DB based on topic.
        
        Args:
            topic (str): Topic to search for
            num_exercises (int): Maximum number of exercises to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of exercise sequences relevant to the topic
        """
        try:
            # Query Vector DB
            results = self.collection.query(
                query_texts=[topic],
                n_results=num_exercises
            )
            
            exercises = []
            for i, metadata in enumerate(results['metadatas'][0]):
                # Parse JSON data from metadata
                sequence_data = json.loads(metadata['json_data'])
                
                # Add audio file path
                audio_path = self.audio_dir / f"{metadata['video_id']}_{metadata['timestamp']}" / metadata['audio_filename']
                sequence_data['audio_file'] = str(audio_path)
                
                exercises.append(sequence_data)
            
            return exercises
            
        except Exception as e:
            logger.error(f"Error retrieving exercises: {str(e)}")
            return []

    def cleanup_old_data(self, days_old: int = 30) -> Dict[str, Any]:
        """
        Clean up old data files and Vector DB entries.
        
        Args:
            days_old (int): Remove data older than this many days
            
        Returns:
            Dict[str, Any]: Status of the cleanup operation
        """
        # TODO: Implement cleanup logic for old files and DB entries
        pass 
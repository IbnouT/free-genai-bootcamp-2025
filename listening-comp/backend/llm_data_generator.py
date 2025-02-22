"""
Module for generating learning content from transcripts using LLM.
"""
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt_template() -> str:
    """
    Load the prompt template from the prompts directory.
    
    Returns:
        str: The prompt template content
    """
    prompt_path = Path(__file__).parent / 'llm_prompts' / 'parsing_prompt_template.md'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_prompt(transcript: str) -> str:
    """
    Create a prompt for the LLM to generate learning content.
    
    Args:
        transcript (str): The transcript text to process
        
    Returns:
        str: The formatted prompt
    """
    template = load_prompt_template()
    return template.replace('{here_the_transcript}', transcript)

def generate_learning_content(transcript: str) -> Optional[Dict[str, Any]]:
    """
    Generate learning content from transcript using LLM.
    
    Args:
        transcript (str): The transcript text to process
        
    Returns:
        Optional[Dict[str, Any]]: Generated learning content in JSON format,
                                 or None if generation fails
    """
    try:
        # Create completion with GPT-4
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 instead of GPT-3.5-turbo
            messages=[
                {"role": "system", "content": "Vous êtes un expert dans la création de matériel d'apprentissage du français langue étrangère, spécialisé dans le style TCF."},
                {"role": "user", "content": create_prompt(transcript)}
            ],
            temperature=0.7,
            max_tokens=4000  # Increased token limit for GPT-4
        )
        
        # Extract and parse JSON from response
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"Error generating learning content: {str(e)}")
        return None

def validate_learning_content(content: List[Dict[str, Any]]) -> bool:
    """
    Validate the structure and content of generated learning content.
    
    Args:
        content (List[Dict[str, Any]]): The generated content to validate
        
    Returns:
        bool: True if content is valid, False otherwise
    """
    try:
        if not isinstance(content, list):
            return False
            
        # Validate each section
        for section in content:
            # Check required keys
            required_keys = {'dialogue', 'question', 'answers', 'correct_answer_index'}
            if not all(key in section for key in required_keys):
                return False
            
            # Validate dialogue structure
            if not isinstance(section['dialogue'], list):
                return False
            for turn in section['dialogue']:
                if not isinstance(turn, list) or len(turn) != 2:
                    return False
            
            # Validate answers
            if not isinstance(section['answers'], list) or len(section['answers']) != 4:
                return False
            
            # Validate correct_answer_index
            if not isinstance(section['correct_answer_index'], int) or not 0 <= section['correct_answer_index'] <= 3:
                return False
            
            # Validate speakers_info if present
            if 'speakers_info' in section and not isinstance(section['speakers_info'], list):
                return False
                
        return True
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False 
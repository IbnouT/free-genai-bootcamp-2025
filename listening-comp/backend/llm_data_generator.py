"""
Module for generating learning content from transcripts using LLM.
"""
from typing import Dict, List, Any, Optional
import json
import os
import logging
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()  # The API key will be automatically loaded from OPENAI_API_KEY environment variable

# Select the model to use
SELECTED_MODEL = "gpt-4o"

def log_llm_interaction(request_data: Dict[str, Any], response_data: Any, error: Optional[Exception] = None) -> None:
    """
    Log LLM request and response data for debugging.
    
    Args:
        request_data (Dict[str, Any]): The request data sent to the LLM
        response_data (Any): The response received from the LLM
        error (Optional[Exception]): Any error that occurred during the interaction
    """
    logger.info("=== LLM Interaction Log ===")
    logger.info("Request:")
    logger.info(json.dumps(request_data, indent=2))
    logger.info("Response:")
    logger.info(json.dumps(response_data if isinstance(response_data, (dict, list)) else str(response_data), indent=2))
    if error:
        logger.error(f"Error occurred: {str(error)}")
        logger.error(f"Error type: {type(error).__name__}")

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

def generate_learning_content(transcript: str) -> Dict[str, Any]:
    """
    Generate learning content from transcript using LLM.
    
    Args:
        transcript (str): The transcript text to process
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - success: bool indicating if generation was successful
            - error: Optional error message if success is False
            - content: Generated learning content in JSON format if success is True
            - debug_info: Dictionary containing debug information
    """
    try:
        # Create the prompt
        prompt = create_prompt(transcript)
        
        # Prepare request data
        request_data = {
            "model": SELECTED_MODEL,
            "messages": [
                {"role": "system", "content": "Vous êtes un expert dans la création de matériel d'apprentissage du français langue étrangère, spécialisé dans le style TCF."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000,
            "response_format": { "type": "json_object" }  # Ensure JSON response
        }
        
        # Log request before sending
        logger.info("Sending request to OpenAI API...")
        
        # Create completion with GPT-4
        response = client.chat.completions.create(**request_data)
        
        # Extract content and log response
        content = response.choices[0].message.content
        log_llm_interaction(request_data, {
            "content": content,
            "usage": response.usage.model_dump() if response.usage else None,
            "model": SELECTED_MODEL
        })
        
        try:
            parsed_content = json.loads(content)
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON parsing error: {str(json_err)}")
            logger.error(f"Raw content that failed to parse: {content}")
            raise
        
        # Validate the content
        is_valid = validate_learning_content(parsed_content)
        if not is_valid:
            logger.error("Content validation failed")
            logger.error(f"Invalid content structure: {json.dumps(parsed_content, indent=2)}")
            return {
                'success': False,
                'error': 'Generated content failed validation',
                'content': None,
                'debug_info': {
                    'original_transcript': transcript,
                    'prompt_used': prompt,
                    'raw_response': content,
                    'model_used': SELECTED_MODEL,
                    'validation_error': 'Content structure validation failed',
                    'parsed_content': parsed_content  # Include the parsed content for debugging
                }
            }
        
        return {
            'success': True,
            'error': None,
            'content': parsed_content,
            'debug_info': {
                'original_transcript': transcript,
                'prompt_used': prompt,
                'raw_response': content,
                'model_used': SELECTED_MODEL,
                'token_usage': response.usage.model_dump() if response.usage else None,
                'request_data': request_data
            }
        }
        
    except json.JSONDecodeError as e:
        log_llm_interaction(
            request_data if 'request_data' in locals() else {"error": "Request data not available"},
            content if 'content' in locals() else "No response content available",
            error=e
        )
        return {
            'success': False,
            'error': 'Failed to parse LLM response as JSON',
            'content': None,
            'debug_info': {
                'original_transcript': transcript,
                'prompt_used': prompt if 'prompt' in locals() else None,
                'raw_response': content if 'content' in locals() else None,
                'model_used': SELECTED_MODEL,
                'error_details': str(e),
                'error_type': 'JSONDecodeError',
                'request_data': request_data if 'request_data' in locals() else None
            }
        }
    except Exception as e:
        log_llm_interaction(
            request_data if 'request_data' in locals() else {"error": "Request data not available"},
            "Error occurred before getting response" if 'response' not in locals() else str(response),
            error=e
        )
        return {
            'success': False,
            'error': str(e),
            'content': None,
            'debug_info': {
                'original_transcript': transcript,
                'prompt_used': prompt if 'prompt' in locals() else None,
                'raw_response': None,
                'model_used': SELECTED_MODEL,
                'error_details': str(e),
                'error_type': type(e).__name__,
                'request_data': request_data if 'request_data' in locals() else None
            }
        }

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
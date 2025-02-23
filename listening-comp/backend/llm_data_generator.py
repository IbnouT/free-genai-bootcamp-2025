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
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

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
    if not template:
        return None
    return template.replace('{here_the_transcript}', transcript)

def validate_learning_content(content):
    """
    Validates that the generated learning content has the correct structure and data types.
    
    Args:
        content (dict): The learning content to validate
        
    Returns:
        bool: True if content is valid, False otherwise
    """
    try:
        # Log the content being validated
        logger.debug("Validating content structure:")
        logger.debug(json.dumps(content, indent=2, ensure_ascii=False))
        
        # Check if all required keys are present
        required_keys = ['dialogue', 'question', 'answers', 'correct_answer_index', 'topics', 'difficulty_level']
        if not all(key in content for key in required_keys):
            missing_keys = [key for key in required_keys if key not in content]
            logger.error(f"Missing required keys: {missing_keys}")
            return False
            
        # Validate dialogue structure
        if not isinstance(content['dialogue'], list):
            logger.error("Dialogue must be a list")
            return False
            
        for i, turn in enumerate(content['dialogue']):
            if not isinstance(turn, list) or len(turn) != 2:
                logger.error(f"Dialogue turn {i} must be a list of [speaker, text], got: {turn}")
                return False
            if not isinstance(turn[0], str) or not isinstance(turn[1], str):
                logger.error(f"Dialogue turn {i} must contain two strings, got types: {type(turn[0])}, {type(turn[1])}")
                return False
                
        # Validate question
        if not isinstance(content['question'], str):
            logger.error(f"Question must be a string, got: {type(content['question'])}")
            return False
            
        # Validate answers
        if not isinstance(content['answers'], list):
            logger.error(f"Answers must be a list, got: {type(content['answers'])}")
            return False
            
        if len(content['answers']) != 4:
            logger.error(f"Answers must contain exactly 4 items, got: {len(content['answers'])}")
            return False
            
        for i, answer in enumerate(content['answers']):
            if not isinstance(answer, str):
                logger.error(f"Answer {i} must be a string, got: {type(answer)}")
                return False
                
        # Validate correct_answer_index
        if not isinstance(content['correct_answer_index'], int):
            logger.error(f"correct_answer_index must be an integer, got: {type(content['correct_answer_index'])}")
            return False
            
        if content['correct_answer_index'] not in [0, 1, 2, 3]:
            logger.error(f"correct_answer_index must be 0, 1, 2, or 3, got: {content['correct_answer_index']}")
            return False
            
        # Validate optional speakers_info if present
        if 'speakers_info' in content:
            if not isinstance(content['speakers_info'], list):
                logger.error(f"speakers_info must be a list, got: {type(content['speakers_info'])}")
                return False
            for i, speaker in enumerate(content['speakers_info']):
                if not isinstance(speaker, str):
                    logger.error(f"Speaker {i} in speakers_info must be a string, got: {type(speaker)}")
                    return False

        # Validate topics
        if not isinstance(content['topics'], list):
            logger.error(f"topics must be a list, got: {type(content['topics'])}")
            return False
        
        if len(content['topics']) < 2 or len(content['topics']) > 4:
            logger.error(f"topics must contain 2-4 items, got: {len(content['topics'])}")
            return False
        
        for i, topic in enumerate(content['topics']):
            if not isinstance(topic, str):
                logger.error(f"Topic {i} must be a string, got: {type(topic)}")
                return False

        # Validate difficulty_level
        if not isinstance(content['difficulty_level'], str):
            logger.error(f"difficulty_level must be a string, got: {type(content['difficulty_level'])}")
            return False
        
        valid_levels = ['A1', 'A2', 'B1', 'B2']
        if content['difficulty_level'] not in valid_levels:
            logger.error(f"difficulty_level must be one of {valid_levels}, got: {content['difficulty_level']}")
            return False
                    
        logger.debug("Content validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return False

def generate_learning_content(transcript: str) -> Dict[str, Any]:
    """
    Generates learning content from a transcript using OpenAI's API.
    
    Args:
        transcript (str): The transcript to generate content from
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - success (bool): Whether generation was successful
            - error (Optional[str]): Error message if any
            - content (Optional[List]): Generated content if successful
            - debug_info (Dict): Debug information including raw response
    """
    try:
        # Create the prompt
        prompt = create_prompt(transcript)
        if not prompt:
            return {
                'success': False,
                'error': 'Failed to create prompt',
                'content': None,
                'debug_info': {'error': 'Prompt creation failed'}
            }
            
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": transcript}
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={ "type": "json_object" }  # Request JSON response
        )
        
        # Get the raw response content
        raw_content = response.choices[0].message.content
        
        # Log the raw response for debugging
        logger.info("Raw LLM Response:")
        logger.info(raw_content)
        
        # Clean the response content - remove markdown code block if present
        cleaned_content = raw_content.strip()
        if cleaned_content.startswith("```"):
            # Find the first and last ``` and extract content between them
            start_idx = cleaned_content.find("\n") + 1
            end_idx = cleaned_content.rfind("```")
            if end_idx == -1:  # No closing ```
                end_idx = len(cleaned_content)
            cleaned_content = cleaned_content[start_idx:end_idx].strip()
        
        # Parse the response
        try:
            content = json.loads(cleaned_content)
            # If content is a list with one item, take the first item
            if isinstance(content, list) and len(content) > 0:
                content = content[0]
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error("Raw content that failed to parse:")
            logger.error(raw_content)
            logger.error("Cleaned content that failed to parse:")
            logger.error(cleaned_content)
            return {
                'success': False,
                'error': f'Failed to parse JSON response: {str(e)}',
                'content': None,
                'debug_info': {
                    'raw_response': raw_content,
                    'cleaned_response': cleaned_content,
                    'error_type': 'JSONDecodeError',
                    'error_details': str(e)
                }
            }
            
        # Validate the content
        if not validate_learning_content(content):
            logger.error("Content validation failed")
            return {
                'success': False,
                'error': 'Content validation failed',
                'content': None,
                'debug_info': {
                    'raw_response': raw_content,
                    'cleaned_response': cleaned_content,
                    'parsed_content': content,
                    'error_type': 'ValidationError'
                }
            }
            
        return {
            'success': True,
            'error': None,
            'content': [content],  # Wrap in list for backward compatibility
            'debug_info': {
                'raw_response': raw_content,
                'cleaned_response': cleaned_content,
                'token_usage': response.usage.model_dump() if response.usage else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating learning content: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'content': None,
            'debug_info': {
                'error_type': type(e).__name__,
                'error_details': str(e)
            }
        }

def generate_learning_content_old(transcript: str) -> Dict[str, Any]:
    """
    Generate learning content from transcript using LLM.
    
    Args:
        transcript (str): The transcript text to process
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - success: bool indicating if generation was successful
            - error: Optional error message if success is False
            - content: Generated learning content if success is True
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
            'content': [parsed_content],  # Wrap in list for backward compatibility
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
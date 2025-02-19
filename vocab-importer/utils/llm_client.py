"""LLM client for vocabulary generation."""
import os
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod
import json
from datetime import datetime

import groq
import openai
from google import generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate_vocabulary(self, prompt: str) -> Dict:
        """
        Generate vocabulary using the LLM.
        
        Args:
            prompt: The formatted prompt to send to the LLM
            
        Returns:
            Dict: The generated vocabulary data
            
        Raises:
            LLMError: If generation fails
        """
        pass
    
    def _parse_llm_response(self, content: str) -> Dict:
        """
        Parse the LLM response and extract the JSON data.
        
        Args:
            content: The raw response content from the LLM
            
        Returns:
            Dict: The parsed vocabulary data
            
        Raises:
            LLMError: If parsing fails
        """
        try:
            # Find JSON content between triple backticks if present
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                content = content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                content = content[start:end].strip()
            
            # Parse the JSON content
            data = json.loads(content)
            
            # Ensure the response has the expected structure
            if "vocab_examples" not in data:
                raise LLMError("Response missing 'vocab_examples' key")
            
            # Update timestamps if missing
            for group in data["vocab_examples"]:
                if "generated_at" not in group:
                    group["generated_at"] = datetime.utcnow().isoformat() + "Z"
            
            return data
            
        except json.JSONDecodeError as e:
            raise LLMError(f"Failed to parse LLM response as JSON: {str(e)}")
        except Exception as e:
            raise LLMError(f"Error processing LLM response: {str(e)}")

class GroqClient(BaseLLMClient):
    """Client for Groq LLM API."""
    
    def __init__(self):
        """Initialize the Groq client."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LLMError("GROQ_API_KEY not found in environment")
        self.client = groq.Client(api_key=api_key)
    
    def generate_vocabulary(self, prompt: str) -> Dict:
        """Generate vocabulary using Groq."""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=4000
            )
            
            # Extract and parse JSON from response
            content = response.choices[0].message.content
            return self._parse_llm_response(content)
            
        except Exception as e:
            raise LLMError(f"Groq generation failed: {str(e)}")

class OpenAIClient(BaseLLMClient):
    """Client for OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMError("OPENAI_API_KEY not found in environment")
        self.client = openai.Client(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    def generate_vocabulary(self, prompt: str) -> Dict:
        """Generate vocabulary using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=4000
            )
            
            # Extract and parse JSON from response
            content = response.choices[0].message.content
            return self._parse_llm_response(content)
            
        except Exception as e:
            raise LLMError(f"OpenAI generation failed: {str(e)}")

class GeminiClient(BaseLLMClient):
    """Client for Google's Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise LLMError("GOOGLE_API_KEY not found in environment")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-pro"))
    
    def generate_vocabulary(self, prompt: str) -> Dict:
        """Generate vocabulary using Gemini."""
        try:
            response = self.model.generate_content(prompt)
            
            # Extract and parse JSON from response
            content = response.text
            return self._parse_llm_response(content)
            
        except Exception as e:
            raise LLMError(f"Gemini generation failed: {str(e)}")

def create_llm_client(provider: str = None) -> BaseLLMClient:
    """
    Create an LLM client based on the specified provider.
    
    Args:
        provider: The LLM provider to use (groq, openai, gemini)
                 If None, uses the value from LLM_PROVIDER env var
                 
    Returns:
        BaseLLMClient: An initialized LLM client
        
    Raises:
        LLMError: If provider is invalid or initialization fails
    """
    provider = provider or os.getenv("LLM_PROVIDER", "groq").lower()
    
    clients = {
        "groq": GroqClient,
        "openai": OpenAIClient,
        "gemini": GeminiClient
    }
    
    if provider not in clients:
        raise LLMError(f"Invalid LLM provider: {provider}")
    
    try:
        return clients[provider]()
    except Exception as e:
        raise LLMError(f"Failed to initialize {provider} client: {str(e)}") 
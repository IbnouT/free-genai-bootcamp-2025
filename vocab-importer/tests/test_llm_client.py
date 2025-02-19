"""Tests for the LLM client module."""
import json
from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime

from utils.llm_client import (
    LLMError,
    BaseLLMClient,
    GroqClient,
    OpenAIClient,
    GeminiClient,
    create_llm_client
)

# Sample valid response for testing
VALID_RESPONSE = {
    "vocab_examples": [
        {
            "script": "新しい",
            "transliteration": "atarashii",
            "pronunciation_aid": [{"value": "あたらしい", "type": "hiragana"}],
            "meaning": "new",
            "part_of_speech": "adjective",
            "usage_examples": ["新しい車を買った。"],
            "notes": "Common adjective",
            "generated_at": "2024-03-15T12:00:00Z"
        }
    ]
}

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for all tests."""
    monkeypatch.setenv("GROQ_API_KEY", "mock-groq-key")
    monkeypatch.setenv("OPENAI_API_KEY", "mock-openai-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "mock-google-key")
    monkeypatch.setenv("LLM_PROVIDER", "groq")

def test_create_llm_client_groq():
    """Test creating a Groq client."""
    client = create_llm_client("groq")
    assert isinstance(client, GroqClient)

def test_create_llm_client_openai():
    """Test creating an OpenAI client."""
    client = create_llm_client("openai")
    assert isinstance(client, OpenAIClient)

def test_create_llm_client_gemini():
    """Test creating a Gemini client."""
    client = create_llm_client("gemini")
    assert isinstance(client, GeminiClient)

def test_create_llm_client_invalid():
    """Test creating client with invalid provider."""
    with pytest.raises(LLMError, match="Invalid LLM provider"):
        create_llm_client("invalid")

def test_create_llm_client_missing_key(monkeypatch):
    """Test creating client with missing API key."""
    # Clear all API keys
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    
    with pytest.raises(LLMError, match="Failed to initialize groq client"):
        create_llm_client("groq")

@patch("groq.Client")
def test_groq_client_generate(mock_groq):
    """Test Groq client vocabulary generation."""
    # Set up mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=json.dumps(VALID_RESPONSE)))
    ]
    mock_groq.return_value.chat.completions.create.return_value = mock_response
    
    client = GroqClient()
    result = client.generate_vocabulary("test prompt")
    
    assert result == VALID_RESPONSE
    mock_groq.return_value.chat.completions.create.assert_called_once()

@patch("openai.Client")
def test_openai_client_generate(mock_openai):
    """Test OpenAI client vocabulary generation."""
    # Set up mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=json.dumps(VALID_RESPONSE)))
    ]
    mock_openai.return_value.chat.completions.create.return_value = mock_response
    
    client = OpenAIClient()
    result = client.generate_vocabulary("test prompt")
    
    assert result == VALID_RESPONSE
    mock_openai.return_value.chat.completions.create.assert_called_once()

@patch("google.generativeai.GenerativeModel")
def test_gemini_client_generate(mock_gemini):
    """Test Gemini client vocabulary generation."""
    # Set up mock response
    mock_response = MagicMock()
    mock_response.text = json.dumps(VALID_RESPONSE)
    mock_gemini.return_value.generate_content.return_value = mock_response
    
    client = GeminiClient()
    result = client.generate_vocabulary("test prompt")
    
    assert result == VALID_RESPONSE
    mock_gemini.return_value.generate_content.assert_called_once()

def test_parse_llm_response_valid():
    """Test parsing valid LLM response."""
    client = GroqClient()  # Use any client to test parsing
    json_str = json.dumps(VALID_RESPONSE)
    result = client._parse_llm_response(json_str)
    assert result == VALID_RESPONSE

def test_parse_llm_response_with_backticks():
    """Test parsing response with backticks."""
    client = GroqClient()  # Use any client to test parsing
    json_str = f"```json\n{json.dumps(VALID_RESPONSE)}\n```"
    result = client._parse_llm_response(json_str)
    assert result == VALID_RESPONSE

def test_parse_llm_response_invalid_json():
    """Test parsing invalid JSON response."""
    client = GroqClient()  # Use any client to test parsing
    with pytest.raises(LLMError, match="Failed to parse LLM response as JSON"):
        client._parse_llm_response("invalid json")

def test_parse_llm_response_missing_key():
    """Test parsing response missing required key."""
    client = GroqClient()  # Use any client to test parsing
    invalid_response = {"some_key": []}
    with pytest.raises(LLMError, match="Response missing 'vocab_examples' key"):
        client._parse_llm_response(json.dumps(invalid_response))

def test_parse_llm_response_adds_timestamp():
    """Test that missing timestamps are added."""
    client = GroqClient()  # Use any client to test parsing
    response = {
        "vocab_examples": [
            {
                "script": "新しい",
                "transliteration": "atarashii",
                "pronunciation_aid": [{"value": "あたらしい", "type": "hiragana"}],
                "meaning": "new",
                "part_of_speech": "adjective",
                "usage_examples": ["新しい車を買った。"],
                "notes": "Common adjective"
            }
        ]
    }
    
    result = client._parse_llm_response(json.dumps(response))
    assert "generated_at" in result["vocab_examples"][0]
    # Verify timestamp format
    datetime.fromisoformat(result["vocab_examples"][0]["generated_at"].rstrip("Z")) 
import pytest
from streamlit.testing.v1 import AppTest

@pytest.fixture
def app_test():
    """Fixture that provides a Streamlit app test instance."""
    return AppTest.from_file("app.py")

@pytest.fixture
def test_data_dir(tmp_path):
    """Fixture that provides a temporary directory for test data."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    return test_dir

@pytest.fixture
def mock_llm_response():
    """Fixture that provides a mock LLM response for testing."""
    return {
        "vocab_examples": [
            {
                "language": "ja",
                "group": "Adjectives",
                "generated_at": "2025-02-18T12:00:00Z",
                "vocab": [
                    {
                        "script": "忙しい",
                        "transliteration": "isogashii",
                        "pronunciation_aid": [
                            {"unit": "忙", "readings": ["i", "so", "ga"]},
                            {"unit": "し", "readings": ["shi"]},
                            {"unit": "い", "readings": ["i"]}
                        ],
                        "meaning": "busy",
                        "part_of_speech": "adjective",
                        "usage_examples": [
                            {
                                "script": "彼はいつも忙しい。",
                                "meaning": "He is always busy."
                            }
                        ],
                        "notes": "Common adjective used to describe a busy state."
                    }
                ]
            }
        ]
    } 
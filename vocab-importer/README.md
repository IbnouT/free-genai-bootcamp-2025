# Vocab Importer

A Streamlit-based internal tool for generating and managing vocabulary lists for multiple languages (Japanese, French, Arabic, Spanish) with potential for expansion to other languages.

## Overview

This tool is part of the language learning portal ecosystem, specifically designed to help generate and manage vocabulary lists that will be used in the main learning portal. It provides functionality to:

- Generate vocabulary lists using LLM
- Review and edit vocabulary entries
- Import existing vocabulary lists
- Export vocabulary in the correct format for the learning portal
- Manage vocabulary across multiple languages

## Documentation

- [Implementation Plan](implementation-plan.md) - Detailed project implementation steps and progress
- [Technical Specifications](tech-specs/technical-specs.md) - Technical requirements and specifications

## Requirements

- Python 3.8+
- Streamlit
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
2. Update the configuration values in `secrets.toml`:
   - Add your LLM API credentials
   - Configure any other necessary settings

## Usage

1. Activate the virtual environment (if not already activated)
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Development

### Project Structure
```
vocab-importer/
├── app.py                  # Main Streamlit application
├── components/            # Streamlit UI components
│   ├── __init__.py
│   ├── sidebar.py         # Sidebar with language/category selection
│   ├── generator.py       # Vocabulary generation interface
│   ├── editor.py          # Vocabulary review/edit interface
│   └── importer.py        # Import/Export interface
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── file_ops.py        # File operations (save/load JSON)
│   ├── llm.py            # LLM integration
│   └── validators.py      # JSON schema validation
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_components/   # UI component tests
│   ├── test_utils/       # Utility function tests
│   └── test_data/        # Test data files
├── data/                  # Generated vocabulary files
│   └── README.md         # Data directory documentation
├── prompt_templates/      # LLM prompt templates by language
│   ├── ja.txt            # Japanese prompts
│   ├── fr.txt            # French prompts
│   ├── ar.txt            # Arabic prompts
│   └── es.txt            # Spanish prompts
├── .streamlit/           # Streamlit configuration
│   ├── config.toml       # Streamlit settings
│   └── secrets.toml.example  # Template for secrets
└── docs/                 # Additional documentation
```

### Running Tests

Run all tests with coverage:
```bash
pytest --cov=. tests/
```

Generate coverage report:
```bash
pytest --cov=. --cov-report=html tests/
```

## Contributing

1. Create a new branch for your feature
2. Follow the implementation plan
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request

## License

[Insert License Information]

---
**Note**: This README will be updated as new features are implemented and additional setup steps are required. 
# Language Listening App

An interactive web application for language learning, focusing on listening comprehension skills using YouTube video transcripts.

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# OR
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run frontend/app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Project Structure

- `frontend/`: Streamlit web application
- `backend/`: Python backend components
  - `transcript_extractor.py`: YouTube transcript extraction
  - `llm_data_generator.py`: LLM processing and data generation
  - `audio_generator.py`: Text-to-speech generation
  - `data_manager.py`: Data persistence
  - `vector_db_manager.py`: Vector database integration (future)
- `docs/`: Project documentation
  - `technical-specifications.md`: Detailed technical specifications
  - `implementation-plan.md`: Implementation phases and timeline 
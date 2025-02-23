## Implementation Plan: Language Listening App Prototype

**Phase 1: Setup and Basic Transcript Extraction (Week 1)**

1.  **Project Setup:**
    *   Create Python project, virtual environment.
    *   Install libraries: `streamlit`, `youtube-transcript-api`, `openai`, `gTTS`, `chromadb` (if using VectorDB early).
    *   Create files: `app.py`, `transcript_extractor.py`, `llm_data_generator.py`, `audio_generator.py`, `data_manager.py`, `vector_db_manager.py`.

2.  **Implement `transcript_extractor.py`:**
    *   Fetch transcript from YouTube URL using `youtube-transcript-api`.
    *   Test with sample video URLs.
    *   Implement error handling.

3.  **Basic Streamlit Frontend (`app.py`):**
    *   Input field for YouTube URL.
    *   "Fetch Transcript" button.
    *   Text area to display transcript.
    *   Run `streamlit run app.py`.
    *   Integrate `transcript_extractor.py` to display fetched transcript in frontend.

**Phase 2: LLM Prompt Engineering and Data Generation (`llm_data_generator.py`) (Week 2-3)**

4.  **Implement `llm_data_generator.py` and Prompt Design:**
    *   Design detailed LLM prompt for dialog segmentation, question extraction, answer generation, correct answer ID, and JSON output.
    *   Code to call LLM API with transcript and prompt.
    *   Code to parse JSON output.
    *   Error handling for API and JSON parsing.

5.  **Testing and Prompt Refinement (Iterative):**
    *   Test `llm_data_generator.py` with transcripts.
    *   Examine JSON output: JSON validity, dialog segmentation, question extraction (TCF format), answer generation (4 options, TCF style, distractors), correct answer ID, overall quality.
    *   Iterate and refine prompt based on testing. Consider few-shot learning examples in prompt.

**Phase 3: Basic Frontend Display of LLM Generated Data (Week 4)**

6.  **Modify Streamlit App (`app.py`):**
    *   Remove old dialog extraction logic.
    *   Integrate `llm_data_generator.py`.
    *   Pass transcript to `llm_data_generator.py` in `app.py`.
    *   Parse JSON data in `app.py`.
    *   Display extracted dialogs, questions, and initial answers (preview only, no interactivity yet) in structured format in frontend.

**Phase 4: Interactive Learning UI (Week 5)**

7.  **Implement Interactive UI in `app.py`:**
    *   Display questions and answer options (radio buttons/numbered list).
    *   Implement answer submission and feedback logic:
        *   Hardcode correct answer index initially for testing.
        *   Compare user answer to correct answer.
        *   Display "Correct/Incorrect" feedback, show correct answer.
        *   "Next Question" button.

**Phase 5: Audio Generation and Data Persistence (Week 6)**

8.  **Implement `audio_generator.py`:**
    *   Generate audio for dialog text using `gTTS` or similar.
    *   Test audio generation and playback.

9.  **Integrate Audio Playback in `app.py`:**
    *   Generate audio for each dialog using `audio_generator.py`.
    *   Add audio player in Streamlit app to play dialog audio.

10. **Implement `data_manager.py` and Data Storage:**
    *   Define data structure.
    *   `data_manager.py` functions to:
        *   Format data to structure.
        *   Save data to JSON file.
        *   Load data from JSON file.
    *   Modify `app.py` to:
        *   Load data from JSON (or hardcoded lists initially).
        *   Implement topic selection: Load relevant data based on selected topic.

**Phase 6: Vector Database Integration (Optional, Week 7-8)**

11. **Set up Vector Database (ChromaDB):**
    *   Install and setup ChromaDB locally.
    *   Explore ChromaDB Python library.

12. **Implement `vector_db_manager.py`:**
    *   Functions to connect to ChromaDB, create collection.
    *   Embed dialog/question text.
    *   Save data to VectorDB with embeddings and metadata.
    *   Implement topic-based search function in `vector_db_manager.py`.

13. **Integrate Vector DB in `app.py`:**
    *   On topic selection, use `vector_db_manager.py` to fetch dialogs from ChromaDB.
    *   Display fetched dialogs for learning session.

**Testing and Refinement (Throughout all phases):**

*   Test functionality after each step.
*   User testing (optional) for feedback.
*   Refine code, prompts, UI/UX based on testing and feedback.
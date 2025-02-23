## Updated Implementation Plan: Language Listening App Prototype

**Phase 1: Setup and Initial Audio & Transcript Pipeline**

1.  **Project Setup:**
    *   Create Python project, virtual environment.
    *   Install core libraries: `streamlit`, `youtube-transcript-api`, `openai`, `gTTS`, `chromadb` (if using VectorDB early), `pytube`, `librosa`, `pydub`.
    *   Create core files: `app.py`, `timestamp_extractor.py`, `audio_segmenter.py`, `audio_transcriber.py`, `llm_json_generator.py`, `audio_generator.py`, `data_manager.py`, `vector_db_manager.py`.

2.  **Implement `timestamp_extractor.py`:**
    *   Fetch video metadata from YouTube URL using `pytube` or `youtube-transcript-api` to extract timestamps and segment titles (if available in description/chapters).
    *   Implement logic to parse timestamps into structured format (start, end).
    *   Test with sample video URLs, especially videos with and without clear timestamps.
    *   Implement basic error handling for timestamp extraction.

3.  **Implement `audio_segmenter.py`:**
    *   Download audio from YouTube URL using `pytube`.
    *   Segment audio into clips based on timestamps extracted by `timestamp_extractor.py` using `pydub` or `librosa`.
    *   Ensure segments are correctly split and saved as individual audio files (e.g., .wav or .mp3).
    *   Test segmentation and handling of different audio formats.
    *   Implement basic error handling for audio download and segmentation.

4.  **Implement `audio_transcriber.py` (Whisper Integration):**
    *   Integrate OpenAI Whisper for audio transcription.
    *   Function in `audio_transcriber.py` to take a segmented audio file as input and output a text transcript using Whisper.
    *   Test transcription quality with sample audio segments.
    *   Consider basic post-processing for transcript cleaning (if time allows in Phase 1, defer to Phase 2 if needed).

5.  **Basic Streamlit Frontend for Pipeline Testing (`app.py`):**
    *   Input field for YouTube URL.
    *   "Process Video" button.
    *   Button to trigger `timestamp_extractor.py`, `audio_segmenter.py`, and `audio_transcriber.py` sequentially for a given URL.
    *   Display extracted timestamps and segmented transcripts in separate text areas in the frontend for verification.
    *   Run `streamlit run app.py`.
    *   Basic UI to visualize the output of each stage of the initial pipeline.

**Phase 2: LLM Prompt Engineering and Segmented Data Generation (`llm_json_generator.py`)**

6.  **Implement `llm_json_generator.py` and TCF Prompt Design for Segments:**
    *   Design detailed LLM prompt specifically for processing *segmented transcripts* to generate TCF-style exercises (as previously refined).  Ensure prompt clearly instructs the LLM to:
        *   Process one segment at a time
        *   Structure dialogue with speaker identification
        *   Generate TCF-style questions and answers
        *   Identify relevant topics (2-4) from predefined categories
        *   Estimate TCF difficulty level
    *   Code in `llm_json_generator.py` to:
        *   Receive a single segmented transcript as input
        *   Call LLM API with the segmented transcript and TCF prompt
        *   Parse and validate the JSON output including topics
        *   Implement error handling for API calls and JSON parsing

7.  **Testing and Iterative Prompt Refinement with Segmented Transcripts:**
    *   Test `llm_json_generator.py` with *segmented transcripts* output from `audio_transcriber.py`.
    *   Examine JSON output for each segment: JSON validity, dialogue segmentation (within the segment if needed), question extraction (TCF format), answer generation (4 options, TCF style, distractors), correct answer ID, overall quality and relevance *to the segment*.
    *   Iterate and refine the TCF prompt specifically based on the performance with *segmented transcripts*.  Incorporate few-shot examples tailored to segmented dialogues.

**Phase 3: Frontend Display of Segmented LLM Generated Data (`app.py`)**

8.  **Modify Streamlit App (`app.py`) for Segmented Exercises:**
    *   Update `app.py` to process video URL through the full pipeline (timestamp extraction, audio segmentation, transcription, LLM processing).
    *   For each segment, display the:
        *   Extracted dialogue (structured as list of lists).
        *   Generated question.
        *   Answer options (initially, just displayed, no interactivity yet).
        *   Structure the frontend to clearly present exercises *segment by segment*.
        *   Remove any old logic related to full transcript processing by LLM.

**Phase 4: Vector DB Integration and Topic-Based Learning**

9. **Set up Vector DB Infrastructure:**
   - Install and configure ChromaDB
   - Design document structure for sequences
   - Create embeddings pipeline
   - Set up data persistence

10. **Implement Sequence Storage:**
    - Store processed sequences in Vector DB
    - Generate and store embeddings
    - Link audio files
    - Add metadata and topic tags

11. **Implement Topic-Based Retrieval:**
    - Create topic selection interface
    - Implement semantic search
    - Add sequence ordering logic
    - Handle audio file retrieval

**Phase 5: Interactive Learning UI (Current Focus)**

12. **Implement Interactive UI in `app.py` for Segmented Exercises:**
    - For each segment displayed in the UI:
      - Present the question and answer options (radio buttons/numbered list)
      - Implement answer submission and feedback logic
      - Display "Correct/Incorrect" feedback
      - Provide navigation controls
    - Add session state management to track:
      - Current segment index
      - User's selected answers
      - Score tracking
      - Exercise history

13. **Add User Progress and Session Management:**
    - Implement session state persistence
    - Add progress indicators
    - Create summary view
    - Track performance statistics

14. **Enhance Exercise Navigation and Control:**
    - Add navigation controls
    - Implement exercise flow control
    - Add keyboard shortcuts
    - Prevent accidental progression

**Phase 6: Audio Playback and Data Persistence**

15. **Integrate Audio Playback:**
    - Add audio player controls
    - Implement playback features:
      - Play/pause/replay
      - Speed control
      - Segment looping
    - Add visual audio timeline

16. **Implement Data Persistence:**
    - Store exercise data
    - Save user progress
    - Track completion status
    - Manage audio file storage

**Testing and Refinement:**
- Rigorous testing of interactive features
- User feedback collection
- Performance optimization
- UI/UX improvements based on testing

**Next Steps:**
1. Begin implementing interactive answer submission
2. Add session state management
3. Create progress tracking system
4. Develop navigation controls
5. Test and refine user interaction flow

**Phase 7: Vector Database Integration for Segmented Data (Optional)**

17. **Set up Vector Database (ChromaDB) for Segmented Data:**
    *   Install and set up ChromaDB locally (if not done in Phase 1).
    *   Explore ChromaDB Python library for handling segmented data.

18. **Implement `vector_db_manager.py` for Segmented Data:**
    *   Functions to connect to ChromaDB and create collections suitable for *segmented exercises*.
    *   Embed dialogue/question text *for each segment individually*.
    *   Save *segmented exercise data* to VectorDB, including embeddings and metadata linking back to segments.
    *   Implement topic/video-based search function in `vector_db_manager.py` to retrieve relevant *segments*.

19. **Integrate Vector DB in `app.py` for Segmented Exercises:**
    *   On topic/video selection, use `
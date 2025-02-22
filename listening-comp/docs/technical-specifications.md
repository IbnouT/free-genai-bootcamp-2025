## Technical Specifications Document: Language Listening App

**1. Introduction**

This document outlines the technical specifications for the Language Listening App, a web application designed for language learning, specifically targeting listening comprehension skills. The app will generate listening exercises from YouTube video transcripts and provide an interactive learning experience.

**2. Frontend Specifications (Streamlit App)**

**2.1. Core Pages/Sections:**

*   **2.1.1. Topic Selection Page:**
    *   **Description:** Landing page for users to choose a learning topic.
    *   **UI Elements:**
        *   **Topic Dropdown/Selection Box:** List of topics (e.g., "Daily Life," "Travel," "Work," "Education," "Hobbies"). Initially hardcoded, later potentially dynamic from backend.
        *   **"Start Learning" Button:** Navigates to the Learning Session Page for the selected topic.
    *   **Functionality:**
        *   On load: Display topic list.
        *   On "Start Learning" click: Navigate to Learning Session Page, passing selected topic.

*   **2.1.2. Learning Session Page:**
    *   **Description:** Presents dialogs, questions, and answer options for interactive learning.
    *   **UI Elements:**
        *   **Dialog Display Area:**
            *   **Structured Format:** Clear display of dialog, potentially with speaker indication (e.g., "Speaker 1: ...", "Speaker 2: ..."). Use Streamlit Markdown (`st.markdown`) or `st.write`.
            *   **Audio Playback Controls:** "Play Audio" button to initiate dialog audio. Optional: Audio progress bar.
        *   **Question Display Area:** Clear display of the question below the dialog.
        *   **Answer Options Area:**
            *   **Radio Buttons/Numbered List:** Four answer options (labeled A, B, C, D or 1, 2, 3, 4).
            *   **"Submit" Button:** To submit the selected answer.
        *   **Feedback Area:** Initially hidden, visible after answer submission.
            *   **Feedback Message:** "Correct!" or "Incorrect."
            *   **Correct Answer Display:** If incorrect, show the correct answer.
            *   **"Next Question" Button:** Load next question for the topic.

**2.2. User Interactions and Logic:**

*   **2.2.1. Topic Selection:** User selects topic and starts session.
*   **2.2.2. Question Loading:** On page load or "Next Question" click:
    *   Fetch (dialog, question, answers, correct answer index) tuple from backend (or local data for prototype), based on topic.
    *   Display dialog, question, and answer options.
*   **2.2.3. Audio Playback:** User clicks "Play Audio" to listen to dialog.
*   **2.2.4. Answer Selection & Submission:**
    *   User selects an answer option.
    *   User clicks "Submit."
*   **2.2.5. Feedback Display:**
    *   Send user's answer and correct index to backend (or compare locally).
    *   Receive feedback (correct/incorrect, correct answer index).
    *   Display feedback message, correct answer in Feedback Area.
    *   Enable "Next Question" button.

**2.3. Data Handling (Frontend - Simple Prototype):**

*   Initially, hardcode sample (dialog, question, answers, correct index) in Streamlit code for UI/logic testing.
*   Later, integrate backend calls to fetch data dynamically.

**3. Backend Specifications (Python Components - Simple Prototype)**

**3.1. Modules/Components:**

*   **3.1.1. `transcript_extractor.py` - YouTube Transcript Extractor:**
    *   **Function:** Fetch transcript from YouTube URL.
    *   **Input:** YouTube video URL (string).
    *   **Processing:** Use `youtube-transcript-api` or `pytube`. Handle errors (no transcript, network issues).
    *   **Output:** Transcript text (string) or `None` on failure.

*   **3.1.2. `llm_data_generator.py` - LLM Processor & Data Generator:**
    *   **Function:** Process transcript using LLM to extract dialogs, questions, generate answers, and identify correct answer.
    *   **Input:** Transcript text (string).
    *   **Processing:**
        *   **LLM Prompt Engineering:** Design prompt for: dialog segmentation, question extraction (TCF format), 4 answer options generation (TCF style), correct answer identification, structured JSON output.
        *   **LLM API Call:** Use LLM API (e.g., OpenAI).
        *   **Output Parsing:** Parse structured JSON output.
        *   **Error Handling:** Handle API failures, JSON parsing errors.
    *   **Output:** List of structured data items in JSON format (see example below).

    ```json
    [
      {
        "dialog": "Speaker 1: ...\nSpeaker 2: ...",
        "question": "...",
        "answers": ["option 1", "option 2", "option 3", "option 4"],
        "correct_answer_index": 0,
        "speakers_info": ["Speaker 1", "Speaker 2"] // Optional
      },
      // ... more dialog-question sets
    ]
    ```

*   **3.1.3. `vector_db_manager.py` - Vector Database Interaction (Future):**
    *   **Function:** (For future scaling) Save and retrieve data from Vector DB for topic-based search.
    *   **Vector DB Choice:**  e.g., ChromaDB (for prototype), FAISS, Pinecone.
    *   **Data Indexing:** Embed dialog/question text for topic search.
    *   **Functions:** Save data tuples, fetch by topic query.
    *   **Initially:** Skip VectorDB, use simpler data storage.

*   **3.1.4. `audio_generator.py` - Audio Generator:**
    *   **Function:** Generate audio for dialog text.
    *   **Input:** Dialog text (string).
    *   **Processing:** Use TTS library (e.g., `gTTS`, `pyttsx3`).
    *   **Output:** Path to audio file (e.g., MP3) or audio data.

*   **3.1.5. `data_manager.py` - Data Formatting and Storage:**
    *   **Function:** Format data, save, and load.
    *   **Data Structure:** Define a consistent data structure (see JSON example in 3.1.2).
    *   **Saving Data:** Function to save data list to file (e.g., JSON).
    *   **Loading Data:** Function to load data from file.

**3.2. Simple Backend Logic:**

*   For prototype: Use Python scripts/functions to orchestrate backend components.
*   Frontend directly calls backend functions.
*   No complex backend server needed initially.
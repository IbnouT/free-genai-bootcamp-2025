# Vocab Importer Technical Specification (Streamlit-Only Prototype)

## 1. Overview
The Vocab Importer is an internal tool designed to generate, review, export, and import enriched vocabulary data for our language learning portal. This prototype supports Japanese, Arabic, French, and Spanish and is intended for a single user. Following the fractional CTO’s directive, the entire prototype will be built using Streamlit as the app prototyping framework. Data persistence will be implemented using file-based storage, with each file corresponding to a word category for a given language. Files are named with the language code, category, current date, and a random element (to avoid duplication) when exporting new vocab lists. When the same language and category are selected for import or further generation, new vocabulary entries will be merged into the same file while avoiding duplicate words.

---

## 2. System Architecture

### 2.1 Application Framework
- **Framework:** Streamlit, providing a modern, engaging, and responsive user interface.
- **File Storage and Organization:**
  - **One File per Word Category:**
    - Vocabulary data will be stored in one file per word category. Each file's name will include the language code and the category. For example:
      ```
      ja_Adjectives_2025-02-18_a7f3.json
      ```
      where:
      - `ja` is the language code,
      - `Adjectives` is the category,
      - `2025-02-18` is the export date, and
      - `a7f3` is a random element to avoid duplicate filenames.
  - **Merging New Vocabulary Entries:**
    - When a user selects a language and category that already has an existing file:
      - The app will load the existing file.
      - New vocabulary entries generated will be merged into this file.
      - The app must check for duplicates (e.g., by comparing the `script` field) to ensure that the same word is not added twice.
      - The original filename is preserved when updating an existing file.
- **LLM Integration:**
  - The system uses a managed LLM API (e.g., GroqCloud) to generate vocabulary entries.
  - Prompt templates are stored as separate files named `llm_prompt_xy` (where `xy` is the language code).
  - The templates include explicit instructions to avoid generating words that already exist in the current vocabulary list.

### 2.2 Key Functionalities
- **Vocabulary Generation:**
  - The user selects a language (e.g., via radio buttons) and a word category.
  - The category input is initially a text box (in English), but once categories are entered, a dropdown is shown listing previously used categories while still allowing new input.
  - The app constructs the generation prompt by loading the corresponding `llm_prompt_xy` file and, if applicable, references already-generated words to avoid duplicates.
  - The LLM returns vocabulary entries in the defined JSON schema.
- **Review & Edit:**
  - Generated vocabulary entries are displayed in an interactive list or table.
  - The user can load an existing vocabulary file, review, and update entries directly in the app.
- **Export:**
  - The user can export the vocabulary list as a JSON file.
  - When exporting, if no file exists for the selected language and category, a new file is created using the naming convention:
    ```
    [language]_[category]_[YYYY-MM-DD]_[random].json
    ```
  - If a file already exists for that category, new vocabulary entries are merged, ensuring duplicate words are not added.
- **Import:**
  - The user can upload a JSON file (which must strictly adhere to the schema).
  - The app validates the file and loads the vocabulary into the session for review and editing.

---

## 3. Data Model and JSON Schema

### Top-Level Structure:
A single JSON object with the key `"vocab_examples"`.
**Example:**
```json
{
  "vocab_examples": [
    {
      "language": "ja",
      "group": "Adjectives",
      "generated_at": "2025-02-18T12:00:00Z",
      "vocab": [ /* array of vocabulary entries */ ]
    }
  ]
}
```

### Vocabulary Entry Schema:
Each vocabulary entry in the `"vocab"` array must include:
- `script`: The word in its native form (kanji/kana for Japanese, Arabic script, or standard Latin script for French/Spanish).
- `transliteration`: The romanized or phonetic form.
- `pronunciation_aid`: An array of objects. Each object contains:
  - `unit`: A substring representing a natural phonetic grouping.
  - `readings`: An array of strings representing the correct phonetic readings for that unit.
- `meaning`: The English meaning.
- `part_of_speech`: e.g., `"adjective"`.
- `usage_examples`: An array of objects. Each object contains:
  - `script`: A complete sentence in the target language using the word.
  - `meaning`: The English translation.
- `notes`: A string providing additional commentary (must be meaningful and not empty).

### Example (Japanese):

```json
{
  "script": "忙しい",
  "transliteration": "isogashii",
  "pronunciation_aid": [
    {
      "unit": "忙",
      "readings": ["i", "so", "ga"]
    },
    {
      "unit": "し",
      "readings": ["shi"]
    },
    {
      "unit": "い",
      "readings": ["i"]
    }
  ],
  "meaning": "busy",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "彼はいつも忙しい。",
      "meaning": "He is always busy."
    },
    {
      "script": "今日は忙しい日だ。",
      "meaning": "Today is a busy day."
    }
  ],
  "notes": "Common adjective used to describe a busy state; frequently used in both casual and formal contexts."
}
```
Similar examples should be constructed for Arabic, French, and Spanish following the strict schema.

---

## 4. Application Flow
- **Generation:**
  - User selects language and enters or selects a category (in English).
  - The app loads the corresponding prompt template from the file `llm_prompt_xy`.
  - The prompt includes instructions to avoid duplicate words by referencing the current vocabulary list.
  - The LLM API is called and returns vocabulary entries in the strict JSON format.
- **Review & Edit:**
  - The generated entries are displayed in an interactive list or table.
  - Users can modify entries as needed within the Streamlit interface.
- **Export:**
  - The app saves the vocabulary list to a JSON file.
  - New files are named using the convention `[language]_[category]_[YYYY-MM-DD]_[random].json`.
  - If a file for the same language and category already exists, the new entries are appended (after filtering out duplicates).
- **Import:**
  - The user uploads a JSON file.
  - The app validates the file against the schema and loads the vocabulary for review/edit.

---

## 5. User Interface (UI) Requirements
- **Modern and Engaging UI:**
  - Use Streamlit’s latest features to build a responsive and visually appealing interface.
  - Provide clear navigation for vocabulary generation, review, export, and import.
  - Use dropdowns, editable tables, file upload widgets, and interactive forms.
- **Category Input:**
  - Initially display a text box for category input (in English).
  - Subsequent uses should show a dropdown populated with previously entered categories (while still allowing new category input).
- **Vocabulary Display:**
  - Show a generated list of words and their categories.
  - Allow the user to load existing files, update entries, and merge new vocabulary without duplicating words.
- **Preventing Duplicate Generation:**
  - The prompt sent to the LLM should include an instruction (and possibly a list of already generated words) to avoid generating duplicates.
  - This helps ensure that each generation session produces new words.

---

## 6. Prompt Template Management
- **Prompt Files:**
  - Prompt templates are stored in files named `llm_prompt_xy` (e.g., `llm_prompt_ja` for Japanese, `llm_prompt_fr` for French, etc.).
  - Each template should include language-specific instructions, including a directive to avoid generating duplicate words.
  - Example directive: 
    ```
    Do not generate words that have already been generated in previous sessions for this category.
    ```
  - Review these templates periodically to ensure they remain effective.

---

## 7. Error Handling and Validation
- **JSON Schema Validation:**
  - All generated and imported JSON files must be validated against the strict schema.
  - Missing keys, empty required fields, or deviations should trigger clear error messages.
- **File I/O Errors:**
  - Handle errors during file reading/writing gracefully, with appropriate user feedback.
- **Duplicate Prevention:**
  - When merging new vocabulary entries into an existing file, compare entries (e.g., by the `"script"` field) to prevent duplicates.

---

## 8. Security Considerations
- **Internal Access:**
  - The tool is for internal use only; security measures are minimal but input validation is essential.
- **API Key Management:**
  - The LLM API key should be stored in environment variables.
- **File Access:**
  - Ensure proper file permissions and avoid accidental overwrites by using randomized file name elements for exports.

---

## 9. Testing and Deployment
- **Testing:**
  - Unit tests for file import/export, schema validation, and duplicate checking.
  - Integration tests for the complete flow (generation → review/edit → export/import).
- **Deployment:**
  - Deploy the prototype on an internal server using Streamlit.
  - Set up a continuous integration (CI) pipeline to run tests on every commit.

### Arabic Vocabulary Generation Prompt

**Task:**  
Generate 10 vocabulary entries (adjectives) in Arabic following the strict JSON format below. **Do not change any key names.** The keys must remain exactly as specified, and all fields must be meaningfully populated (no empty strings or null values).

All entries must be output inside a top-level JSON object with the key `"vocab_examples"`.

Use the following instructions for each vocabulary entry.

---

**Overall JSON Structure:**  
The final output must be a single JSON object with a top-level key `"vocab_examples"`. For example:

```json
{
  "vocab_examples": [
    {
      "language": "ar",
      "group": "Adjectives",
      "generated_at": "ISO_8601_timestamp",
      "vocab": [ /* array of vocabulary entries */ ]
    }
  ]
}
```

Replace "ISO_8601_timestamp" with the current timestamp in ISO 8601 format.

***Required Keys for Each Vocabulary Entry:***

Each vocabulary object within the `"vocab"` array must include the following keys exactly:

- **script**:
  - Must contain the Arabic word in its native characters.
  - **Do not leave this field empty.**
- **transliteration**: 
  - The romanized form of the word.  
- **pronunciation_aid**: 
  - An array of objects. Each object must contain:
    - **unit**: A substring representing a natural phonetic grouping (in Arabic script) that reflects the correct pronunciation.
      - **Must not be empty**
    - **readings**: An array of strings representing the correct phonetic readings for that unit. The prononciation should be in the context of the script provided! 
  - **Important**: Ensure that the readings accurately reflect how the substring is pronounced in the context of the word. For example, for the word "جديد" ("jadeed"):
    - The unit corresponding to "ج" should have readings that match its sound in this word.
    - Group letters into natural units instead of splitting arbitrarily by individual letter unless that is appropriate.
    - Verify each unit's reading against standard Arabic pronunciation; do not assign arbitrary or unrelated readings.
- **meaning**: 
  - The English meaning of the word.  
- **part_of_speech**: 
  - The grammatical category (e.g., `"adjective"`).  
- **usage_examples**: 
  - An array of objects, each with:
    - **script**: A sentence in Arabic that uses the word.
      - **This field must be populated with an actual sentence (in kanji/kana).**
    - **meaning**: The English translation of that sentence.
- **notes**: 
  - A string providing additional commentary on the word (e.g., usage context, nuances, common usage).
  - **Provide a meaningful note rather than leaving it empty or null.**

All keys must be present for each vocabulary entry.

**Example of a Good Vocabulary Entry:**  
For the word `"جديد"`` (jadeed), a correct breakdown is:
```json
{
  "script": "جديد",
  "transliteration": "jadeed",
  "pronunciation_aid": [
    {
      "unit": "ج",
      "readings": ["ja"]
    },
    {
      "unit": "ديد",
      "readings": ["deed"]
    }
  ],
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "اشتريت سيارة جديدة.",
      "meaning": "I bought a new car."
    },
    {
      "script": "هذا الكتاب جديد.",
      "meaning": "This book is new."
    }
  ],
  "notes": "Common adjective used to describe something that is new or recently introduced."
}
```
---
**Bad Example 1 (Incorrect `pronunciation_aid` field):**
```json
{
  "script": "جديد",
  "transliteration": "jadeed",
  "pronunciation_aid": "ja-deed",
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "اشتريت سيارة جديدة.",
      "meaning": "I bought a new car."
    }
  ],
  "notes": "This entry is wrong because the pronunciation aid must be an array of objects, not a single string."
}
```
Explanation: This is incorrect because the `pronunciation_aid` field must be an array of objects with each object containing a non-empty `unit` and its corresponding `readings`.
---

**Bad Example 2 (Arbitrary splitting and inaccurate readings)**
Arbitrarily splitting the word without respecting natural syllable boundaries:
```json
{
  "script": "جديد",
  "transliteration": "jadeed",
  "pronunciation_aid": [
    {
      "unit": "ج",
      "readings": ["j"]
    },
    {
      "unit": "د",
      "readings": ["a"]
    },
    {
      "unit": "ي",
      "readings": ["dee"]
    },
    {
      "unit": "د",
      "readings": ["d"]
    }
  ],
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "اشتريت سيارة جديدة.",
      "meaning": "I bought a new car."
    },
    {
      "script": "هذا الكتاب جديد.",
      "meaning": "This book is new."
    }
  ],
  "notes": "This entry is wrong because it splits the word letter-by-letter rather than grouping into natural phonetic units. The natural grouping for 'جديد' is 'ج' and 'ديد'."
}
```
Explanation: The `unit` fields must not be split arbitrarily; they should group letters into units that reflect natural pronunciation. The above example incorrectly splits "ديد" into individual letters rather than treating it as a single unit with the reading "deed".


---

**Instructions for the "pronunciation_aid" Field:**
- Split the Arabic word into natural, logical phonetic units.
- Do not simply split by individual letters unless that is the natural grouping.
- Ensure each unit reflects how the word is pronounced in natural spoken Arabic.
- All units and their corresponding readings must be non-empty and accurate.

**Instructions for the "usage_examples" Field:**
- Provide at least two usage examples per vocabulary entry.
- Each example must include a complete Arabic sentence (in the "script" field) using the word and its English translation (in the "meaning" field).

**Final Output Requirement:**
Generate a complete JSON object containing 10 vocabulary entries for Arabic adjectives that strictly follow the structure and rules above. Ensure that the "notes" field is populated with meaningful commentary for each entry, and that no fields (such as "script", "unit" in "pronunciation_aid", or "usage_examples"'s "script") are left empty.

Please output the final JSON object exactly as specified.

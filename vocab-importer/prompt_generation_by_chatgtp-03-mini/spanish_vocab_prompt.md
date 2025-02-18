### Spanish Vocabulary Generation Prompt

**Task:**  
Generate 10 vocabulary entries (adjectives) in Spanish following the strict JSON format below. **Do not change any key names.** The keys must remain exactly as specified, and all fields must be meaningfully populated (no empty strings or null values).

All entries must be output inside a top-level JSON object with the key `"vocab_examples"`.

Use the following instructions for each vocabulary entry.

---

**Overall JSON Structure:**  
The final output must be a single JSON object with a top-level key `"vocab_examples"`. For example:

```json
{
  "vocab_examples": [
    {
      "language": "es",
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
  - MMust contain the Spanish word in its standard written form (using Latin characters).
  - **Do not leave this field empty.**
- **transliteration**: 
  - The phonetic form of the word. For Spanish, this may be identical to the script or a phonetic rendering if needed.
- **pronunciation_aid**: 
  - An array of objects. Each object must contain:
    - **unit**: A substring representing a natural syllabic or phonetic grouping.
      - **Must not be empty**
    - **readings**: An array of strings representing the correct phonetic readings for that unit. 
  - **Important**: Ensure that the readings accurately reflect how the substring is pronounced in the context of the word. For example, for the word "nuevo", the natural grouping might be:
    - The unit corresponding to "nue" should have a reading like "nwe".
    - The unit corresponding to "vo" should have a reading like "vo".
    - Verify each unit's reading against standard Spanish pronunciation. Do not arbitrarily split the word; follow natural syllable boundaries.
- **meaning**: 
  - The English meaning of the word.  
- **part_of_speech**: 
  - The grammatical category (e.g., `"adjective"`).  
- **usage_examples**: 
  - An array of objects, each with:
    - **script**: A complete Spanish sentence that uses the word.
      - **This field must be populated with an actual sentence (in kanji/kana).**
    - **meaning**: The English translation of that sentence.
- **notes**: 
  - A string providing additional commentary on the word (e.g., usage context, nuances, common usage).
  - **Provide a meaningful note rather than leaving it empty or null.**

All keys must be present for each vocabulary entry.

**Example of a Good Vocabulary Entry:**  
For the word `"nuevo"`` (new), a correct breakdown is:
```json
{
  "script": "nuevo",
  "transliteration": "nuevo",
  "pronunciation_aid": [
    {
      "unit": "nue",
      "readings": ["nwe"]
    },
    {
      "unit": "vo",
      "readings": ["vo"]
    }
  ],
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "Este es un libro nuevo.",
      "meaning": "This is a new book."
    },
    {
      "script": "Compré un coche nuevo.",
      "meaning": "I bought a new car."
    }
  ],
  "notes": "Common adjective used to describe something that is new or recently introduced."
}
```
---
**Bad Example 1 (Incorrect `pronunciation_aid` field):**
```json
{
  "script": "nuevo",
  "transliteration": "nuevo",
  "pronunciation_aid": "nwevo",
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "Este es un libro nuevo.",
      "meaning": "This is a new book."
    }
  ],
  "notes": "This entry is wrong because the pronunciation aid must be an array of objects, not a single string."
}
```
Explanation: The `pronunciation_aid` field must be an array of objects, each with a non-empty `unit` and its corresponding `readings`.
---

**Bad Example 2 (Arbitrary splitting and inaccurate readings)**
Arbitrarily splitting the word without respecting natural syllable boundaries:
```json
{
  "script": "nuevo",
  "transliteration": "nuevo",
  "pronunciation_aid": [
    {
      "unit": "n",
      "readings": ["n"]
    },
    {
      "unit": "u",
      "readings": ["u"]
    },
    {
      "unit": "e",
      "readings": ["e"]
    },
    {
      "unit": "v",
      "readings": ["v"]
    },
    {
      "unit": "o",
      "readings": ["o"]
    }
  ],
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "Este es un libro nuevo.",
      "meaning": "This is a new book."
    },
    {
      "script": "Compré un coche nuevo.",
      "meaning": "I bought a new car."
    }
  ],
  "notes": "This entry is wrong because it splits the word arbitrarily by individual letters instead of grouping into natural syllables. The natural grouping for 'nuevo' is 'nue' and 'vo'."
}
```
Explanation: The `unit` fields must reflect natural syllabic boundaries. Splitting "nuevo" into individual letters or arbitrary segments results in incorrect readings and does not represent natural pronunciation.


---

**Instructions for the "pronunciation_aid" Field:**
- Split the Spanish word into natural, logical phonetic units.
- Do not simply split by individual letters unless that is the natural grouping.
- Ensure each unit reflects how the word is pronounced in natural spoken Spanish.
- All units and their corresponding readings must be non-empty and accurate.

**Instructions for the "usage_examples" Field:**
- Provide at least two usage examples per vocabulary entry.
- Each example must include a complete Spanish sentence (in the "script" field) using the word and its English translation (in the "meaning" field).

**Final Output Requirement:**
Generate a complete JSON object containing 10 vocabulary entries for Spanish adjectives that strictly follow the structure and rules above. Ensure that the "notes" field is populated with meaningful commentary for each entry, and that no fields (such as "script", "unit" in "pronunciation_aid", or "usage_examples"'s "script") are left empty.

Please output the final JSON object exactly as specified.

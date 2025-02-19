### Japanese Vocabulary Generation Prompt

**Task:**  
Generate 5 vocabulary entries (Adjectives) in Japanese following the strict JSON format below. **Do not change any key names.** The keys must remain exactly as specified.

**Diversity Requirements:**
- Generate words across different semantic sub-categories of Adjectives

**Previously Used Words:**
The following words have already been used and should NOT be generated again:
`新しい`, `古い`, `忙しい`

**Overall JSON Structure:**  
The final output must be a single JSON object with a top-level key `"vocab_examples"`. For example:

```json
{
  "vocab_examples": [
    {
      "language": "ja",
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
  - Must contain the word in its native script/characters
  - **Do not leave this field empty**
- **transliteration**: 
  - The romanized form of the word
- **pronunciation_aid**: 
  - An array of objects. Each object must contain:
    - **unit**: A substring representing a natural phonetic grouping
      - **Must not be empty**
    - **readings**: An array of strings representing the correct phonetic readings for that unit
  - **Important**: Ensure that the readings accurately reflect how the substring is pronounced in the context of the word
- **meaning**: 
  - The English meaning of the word
- **part_of_speech**: 
  - The grammatical category (e.g., "Adjectives")
- **usage_examples**: 
  - An array of objects, each with:
    - **script**: A sentence using the word
    - **meaning**: The English translation of that sentence
- **notes**: 
  - A string providing additional commentary on the word (usage context, nuances, common usage)
  - **Provide a meaningful note rather than leaving it empty**

**Example of a Good Vocabulary Entry:**  
For the word `"忙しい"` (isogashii):
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

**Bad Example (Incorrect Readings):**
```json
{
  "script": "新しい",
  "transliteration": "atarashii",
  "pronunciation_aid": [
    {
      "unit": "",
      "readings": ["shi", "ara"]
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
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "彼は新しい車を買った。",
      "meaning": "He bought a new car."
    }
  ],
  "notes": "This entry is wrong because it leaves the 'unit' field empty and assigns incorrect readings."
}
```

Explanation: This breakdown is incorrect because the `unit` fields must not be empty, and the readings must correctly reflect the actual pronunciation. For `新しい`, the unit `新` should be assigned readings that correctly match its sound in this word, not arbitrary ones.

**Instructions for the "pronunciation_aid" Field:**
- Split the word into natural, logical phonetic units
- Do not simply split by individual letters unless that is the natural grouping
- Ensure each unit reflects how the word is pronounced in natural spoken Japanese
- All units and their corresponding readings must be non-empty and accurate

**Instructions for the "usage_examples" Field:**
- Provide at least two usage examples per vocabulary entry
- Each example must include a complete sentence using the word and its English translation

**Final Output Requirement:**
Generate a complete JSON object containing 5 vocabulary entries for Japanese Adjectives that strictly follow the structure and rules above. Ensure that the "notes" field is populated with meaningful commentary for each entry, and that no fields are left empty. 
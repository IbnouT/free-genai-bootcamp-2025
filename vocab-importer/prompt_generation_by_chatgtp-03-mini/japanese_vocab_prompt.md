### Japanese Vocabulary Generation Prompt

**Task:**  
Generate 10 vocabulary entries (adjectives) in Japanese following the strict JSON format below. **Do not change any key names.** The keys must remain exactly as specified.

All entries must be output inside a top-level JSON object with the key `"vocab_examples"`.

Use the following instructions for each vocabulary entry.

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
  - Must contain the Japanese word in its native characters (kanji/kana).
  - **Do not leave this field empty.**
- **transliteration**: 
  - The romanized (romaji) form of the word.  
- **pronunciation_aid**: 
  - An array of objects. Each object must contain:
    - **unit**: A substring representing a natural phonetic grouping (in kanji/kana)
      - **Must not be empty**
    - **readings**: An array of strings representing the correct phonetic readings for that unit. The prononciation should be in the context of the script provided! 
  - **Important**: Ensure that the readings accurately reflect how the substring is pronounced in the context of the word. For example, for the word "新しい" ("atarashii"):
    - The unit corresponding to "新" should have readings that match its pronunciation in "atarashii". Do not assign unrelated readings like "shi" if that does not represent the sound of "新" in this word.
    - Verify each unit's reading against standard Japanese pronunciation. Do not combine multiple potential readings unless both are applicable in the given context.
- **meaning**: 
  - The English meaning of the word.  
- **part_of_speech**: 
  - The grammatical category (e.g., `"adjective"`).  
- **usage_examples**: 
  - An array of objects, each with:
    - **script**: A sentence in Japanese that uses the word.
      - **This field must be populated with an actual sentence (in kanji/kana).**
    - **meaning**: The English translation of that sentence.
- **notes**: 
  - A string providing additional commentary on the word (e.g., usage context, nuances, common usage).
  - **Provide a meaningful note rather than leaving it empty or null.**

All keys must be present for each vocabulary entry.

**Example of a Good Vocabulary Entry:**  
For the word `"忙しい"` (isogashii), a correct breakdown is:
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
---
**Bad Example 1 (Incorrect `pronunciation_aid` field):**
```json
{
  "script": "忙しい",
  "transliteration": "isogashii",
  "pronunciation_aid": "たべる",
  "meaning": "busy",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "彼は忙しい。",
      "meaning": "He is busy."
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
    },
    {
      "script": "新しい靴はとても快適だ。",
      "meaning": "The new shoes are very comfortable."
    }
  ],
  "notes": "This entry is wrong because it leaves the 'unit' field empty in one object and assigns readings to '新' that do not accurately represent its pronunciation in 'atarashii'."
}
```
Explanation: This breakdown is incorrect because the `unit` fields must not be empty, and the readings must correctly reflect the actual pronunciation. For `新しい`, the unit `新` should be assigned readings that correctly match its sound in this word, not arbitrary ones like `shi` if that does not occur.


---

**Instructions for the "pronunciation_aid" Field:**
- Split the Japanese word into natural, logical phonetic units.
- Do not simply split by character unless it naturally forms a syllable.
- Ensure each unit reflects how the word is pronounced in natural spoken Japanese.

**Instructions for the "usage_examples" Field:**
- Provide at least two usage examples per vocabulary entry.
- Each example must include a sentence using the word and its English translation.

**Final Output Requirement:**
Generate a complete JSON object containing 10 vocabulary entries for Japanese adjectives that follow the structure and rules above. Ensure that the "notes" field is populated with meaningful commentary for each entry, not left as null.

Please output the final JSON object exactly as specified.

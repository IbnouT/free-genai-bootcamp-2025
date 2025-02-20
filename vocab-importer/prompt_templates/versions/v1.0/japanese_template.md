**Language-Specific Requirements for Japanese:**
- **For nouns, include appropriate counter information**
- **Include only kana readings (no romaji) in pronunciation aid**
- **List common compound words in notes**
- Ensure proper kanji usage with appropriate readings
- Include common variations or alternate forms if applicable

**Example of a Good Vocabulary Entry:**  
For the word `"本"` (book):
```json
{
  "script": "本",
  "transliteration": "hon",
  "pronunciation_aid": [
    {
      "unit": "本",
      "readings": ["ほん"]
    }
  ],
  "meaning": "book",
  "part_of_speech": "noun",
  "usage_examples": [
    {
      "script": "この本は面白いです。",
      "meaning": "This book is interesting."
    },
    {
      "script": "本を三冊買いました。",
      "meaning": "I bought three books."
    }
  ],
  "notes": "Common noun. Counter: 冊 (さつ). Common compounds: 本屋 (ほんや, bookstore), 教科書 (きょうかしょ, textbook), 本棚 (ほんだな, bookshelf)."
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

**Additional Japanese-Specific Notes:**
- For kanji compounds, break down each character with its correct reading in context
- Include pitch accent information in the readings if relevant
- For な-adjectives, include the な in usage examples where appropriate
- Consider common collocations and set phrases in usage examples 
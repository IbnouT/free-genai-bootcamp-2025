**Language-Specific Requirements for Japanese:**
- For adjectives, include both い-adjectives and な-adjectives
- Ensure proper kanji usage with appropriate readings
- Include common variations or alternate forms if applicable

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

**Additional Japanese-Specific Notes:**
- For kanji compounds, break down each character with its correct reading in context
- Include pitch accent information in the readings if relevant
- For な-adjectives, include the な in usage examples where appropriate
- Consider common collocations and set phrases in usage examples 
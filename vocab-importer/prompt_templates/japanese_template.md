**Language-Specific Requirements for Japanese (v2.0):**
- **For all words:**
  - Use appropriate kanji where common
  - Include pitch accent patterns in romaji
  - List common collocations and compounds
- **For nouns:**
  - Include appropriate counter(s)
  - Show both の-modification and compound forms
  - Note any irregular readings in compounds
- **For adjectives:**
  - Specify type (い-adjective or な-adjective)
  - Include な where appropriate in examples
  - Show both attributive and predicative uses
- **For verbs:**
  - Show base form and polite form
  - Include common conjugations
  - Note transitivity and any irregular forms

**Example of a Good Vocabulary Entry:**  
For the word `"新しい"` (new):
```json
{
  "script": "新しい",
  "transliteration": "atarashii",
  "pronunciation_aid": [
    {
      "unit": "新",
      "readings": ["a", "ta", "ra"]
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
      "script": "新しい本を買った。",
      "meaning": "I bought a new book."
    },
    {
      "script": "これは新しいですか？",
      "meaning": "Is this new?"
    },
    {
      "script": "彼は新しい車を持っています。",
      "meaning": "He has a new car."
    }
  ],
  "notes": "い-adjective. Pitch accent: [atara↓shii]. Common compounds: 新品 (shinpin, brand new item), 新築 (shinchiku, newly built). Casual form ends in い, polite form adds です. Used before nouns directly: 新しい家 (atarashii ie, new house). Related words: 新規 (shinki, new/newly), 新人 (shinjin, newcomer)."
}
```

**Bad Example (Multiple Issues):**
```json
{
  "script": "学生",
  "transliteration": "gakusei",
  "pronunciation_aid": [
    {
      "unit": "学生",
      "readings": ["gakusei"]  // Not properly segmented
    }
  ],
  "meaning": "student",
  "part_of_speech": "noun",
  "usage_examples": [
    {
      "script": "彼は学生です。",
      "meaning": "He is a student."
    }
  ],
  "notes": "A student."  // Too brief, missing important information
}
```

Explanation: The bad example has several issues:
1. Pronunciation aid not properly segmented (should be: 学 [ga, ku] and 生 [se, i])
2. Missing pitch accent information
3. No counter information
4. No compound words
5. Too brief notes
6. Only one usage example
7. No の-modification examples

**Additional Japanese-Specific Notes:**
- Break down kanji compounds into their component readings in romaji
- Include pitch accent patterns using ↓ for downstep
- Show both polite and casual forms in examples
- Include common collocations and set phrases
- Note any irregular readings or pitch patterns
- Show proper particle usage in examples
- Include both written and spoken forms where different 
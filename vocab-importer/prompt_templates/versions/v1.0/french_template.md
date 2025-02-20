**Language-Specific Requirements for French:**
- Include both masculine and feminine forms where applicable
- Note any irregular forms or spelling changes
- Consider position (before/after noun) if relevant
- Include liaison effects where applicable
- **All pronunciation units must be non-empty and use standard IPA notation**
- **Each example must show both masculine and feminine usage where applicable**

**Example of a Good Vocabulary Entry:**  
For the word `"nouveau"` (new):
```json
{
  "script": "nouveau",
  "transliteration": "nouveau",
  "pronunciation_aid": [
    {
      "unit": "nou",
      "readings": ["nu"]
    },
    {
      "unit": "veau",
      "readings": ["vo"]
    }
  ],
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "C'est un nouveau livre.",
      "meaning": "It is a new book."
    },
    {
      "script": "C'est une nouvelle maison.",
      "meaning": "It is a new house."
    }
  ],
  "notes": "Masculine form 'nouveau' becomes 'nouvel' before vowels, feminine form is 'nouvelle'. Common adjective used in both formal and informal contexts."
}
```

**Bad Example (Incorrect Pronunciation Aid):**
```json
{
  "script": "nouveau",
  "transliteration": "nouveau",
  "pronunciation_aid": "nuvo",
  "meaning": "new",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "C'est un nouveau livre.",
      "meaning": "It is a new book."
    }
  ],
  "notes": "This entry is wrong because the pronunciation aid must be an array of objects, not a single string."
}
```

Explanation: The `pronunciation_aid` field must be an array of objects, each with a non-empty `unit` and its corresponding `readings`.

**Additional French-Specific Notes:**
- Note any required elision or liaison
- Include common expressions and collocations
- Specify position relative to the noun
- Note any changes in meaning based on position
- Include register information (formal/informal)
- Consider agreement rules and exceptions 
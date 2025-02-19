**Language-Specific Requirements for Arabic:**
- Include both masculine and feminine forms where applicable
- Consider root patterns and derivations
- Include diacritical marks (tashkeel) in the script where necessary for clarity
- Account for dialectal variations in the notes if relevant

**Example of a Good Vocabulary Entry:**  
For the word `"جديد"` (jadeed):
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
  "notes": "Common adjective used to describe something new. Feminine form is جديدة (jadeeda). From root ج-د-د (j-d-d)."
}
```

**Bad Example (Incorrect Readings):**
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

**Additional Arabic-Specific Notes:**
- Break down words according to their root pattern structure
- Include common idiomatic usage if applicable
- Note any irregular plural forms for adjectives
- Consider formal (MSA) vs colloquial usage where relevant
- Include both definite and indefinite forms in usage examples 
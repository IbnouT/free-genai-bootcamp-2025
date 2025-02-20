**Language-Specific Requirements for Arabic:**
- **Include diacritical marks (tashkeel) in all script entries**
- **Specify verb form (Form I, II, etc.) in notes**
- **Include complete root pattern with all letters**
- **Provide both past and present tense forms**
- Consider root patterns and derivations
- Account for dialectal variations in the notes if relevant

**Example of a Good Vocabulary Entry:**  
For the word `"كَتَبَ"` (kataba):
```json
{
  "script": "كَتَبَ",
  "transliteration": "kataba",
  "pronunciation_aid": [
    {
      "unit": "كَ",
      "readings": ["ka"]
    },
    {
      "unit": "تَ",
      "readings": ["ta"]
    },
    {
      "unit": "بَ",
      "readings": ["ba"]
    }
  ],
  "meaning": "wrote",
  "part_of_speech": "verb",
  "usage_examples": [
    {
      "script": "الطالِبُ كَتَبَ رِسالَةً.",
      "meaning": "The student wrote a letter."
    },
    {
      "script": "يَكْتُبُ الطالِبُ الدَّرْسَ.",
      "meaning": "The student writes the lesson."
    }
  ],
  "notes": "Form I verb (فَعَلَ). Root: ك-ت-ب (k-t-b). Present tense: يَكْتُبُ (yaktubu). Common in both MSA and dialects."
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
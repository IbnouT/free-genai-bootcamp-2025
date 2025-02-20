**Language-Specific Requirements for Spanish:**
- Include both masculine and feminine forms where applicable
- Note any irregular forms or spelling changes
- Consider position (before/after noun) if relevant
- Include regional variations if significant

**Example of a Good Vocabulary Entry:**  
For the word `"nuevo"` (new):
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
  "notes": "Common adjective. Masculine 'nuevo', feminine 'nueva'. Usually placed after the noun."
}
```

**Bad Example (Incorrect Pronunciation Aid):**
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

**Additional Spanish-Specific Notes:**
- Include common apocope forms if applicable
- Note any stress/accent changes in different forms
- Include regional variations in usage or meaning
- Consider both attributive and predicative uses
- Note any changes in meaning based on position
- Include register information (formal/informal)
- Consider agreement patterns and exceptions 
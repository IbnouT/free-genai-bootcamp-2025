**Language-Specific Requirements for Arabic (v2.0):**
- **For all words:**
  - Include full diacritical marks (tashkeel)
  - Show root pattern and derivation
  - Note any dialectal variations
- **For verbs:**
  - Specify verb form (Form I-X)
  - Show past and present tense conjugations
  - Include verbal noun (masdar)
  - Note transitivity and object markers
- **For nouns:**
  - Show broken plural if applicable
  - Include gender and definiteness
  - Note any irregular forms
- **For adjectives:**
  - Include both masculine and feminine forms
  - Show agreement patterns
  - Note comparative/superlative forms

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
    },
    {
      "script": "كُتِبَ الكِتابُ بِاللُّغَةِ العَرَبِيَّةِ.",
      "meaning": "The book was written in Arabic."
    }
  ],
  "notes": "Form I verb (فَعَلَ). Root: ك-ت-ب (k-t-b). Present tense: يَكْتُبُ (yaktubu). Verbal noun: كِتابَة (kitaaba). Active participle: كاتِب (kaatib). Passive participle: مَكْتوب (maktuub). Common in both MSA and dialects. Related words: كِتاب (book), مَكْتَب (desk/office), مَكْتَبة (library). Passive voice commonly used."
}
```

**Bad Example (Multiple Issues):**
```json
{
  "script": "كتب",
  "transliteration": "kataba",
  "pronunciation_aid": [
    {
      "unit": "ك",
      "readings": ["ka"]
    }
  ],
  "meaning": "wrote",
  "part_of_speech": "verb",
  "usage_examples": [
    {
      "script": "الطالب كتب رسالة",
      "meaning": "The student wrote a letter."
    }
  ],
  "notes": "A verb meaning to write."
}
```

Explanation: The bad example has several issues:
1. Missing diacritical marks (tashkeel)
2. Incomplete pronunciation aid
3. No verb form specification
4. No tense variations
5. No related forms or derivatives
6. Missing case endings in example
7. Too brief notes
8. No passive voice example

**Additional Arabic-Specific Notes:**
- Include all necessary diacritical marks for precise pronunciation
- Show both formal (MSA) and common dialectal variations
- Note any irregular conjugation patterns
- Include common idiomatic expressions
- Show proper case endings in examples
- Note any changes in meaning with different prepositions
- Include passive voice where commonly used
- Show proper definiteness marking (with/without ال) 
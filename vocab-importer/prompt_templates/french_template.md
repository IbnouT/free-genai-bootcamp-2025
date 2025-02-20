**Language-Specific Requirements for French (v2.0):**
- **For all words:**
  - Break down into syllables
  - Use standard IPA notation
  - Mark stress patterns
  - Note liaison and elision rules
- **For adjectives:**
  - Show all forms (masculine/feminine, singular/plural)
  - Note position rules (before/after noun)
  - Include any irregular forms
  - Show elision and liaison effects
- **For nouns:**
  - Specify gender and number
  - Show article usage
  - Include common modifiers
- **For verbs:**
  - Show conjugation pattern
  - Note auxiliary verb (être/avoir)
  - Include common tenses

**Example of a Good Vocabulary Entry:**  
For the word `"intéressant"` (interesting):
```json
{
  "script": "intéressant",
  "transliteration": "intéressant",
  "pronunciation_aid": [
    {
      "unit": "in",
      "readings": ["ɛ̃"]
    },
    {
      "unit": "té",
      "readings": ["te"]
    },
    {
      "unit": "res",
      "readings": ["ʁɛ"]
    },
    {
      "unit": "sant",
      "readings": ["sɑ̃"]
    }
  ],
  "meaning": "interesting",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "C'est un livre intéressant.",
      "meaning": "It's an interesting book."
    },
    {
      "script": "Une histoire intéressante.",
      "meaning": "An interesting story."
    }
  ],
  "notes": "Forms: m.sg. intéressant, f.sg. intéressante, pl. intéressants/intéressantes. Position: after noun. Common expressions: très intéressant (very interesting), peu intéressant (not very interesting). Register: standard, used in both formal and informal contexts."
}
```

**Bad Example (Multiple Issues):**
```json
{
  "script": "heureux",
  "transliteration": "heureux",
  "pronunciation_aid": [
    {
      "unit": "heureux",
      "readings": ["øʁø"]  // Not properly segmented
    }
  ],
  "meaning": "happy",
  "part_of_speech": "adjective",
  "usage_examples": [
    {
      "script": "Il est heureux.",
      "meaning": "He is happy."
    }
  ],
  "notes": "An adjective meaning happy."  // Too brief
}
```

Explanation: The bad example has several issues:
1. Pronunciation not broken into syllables
2. No stress pattern indicated
3. Single usage example
4. Insufficient notes
5. No gender/number variations shown

**Additional French-Specific Notes:**
- Break words into natural syllables
- Show liaison with ‿ symbol (e.g., "les‿amis")
- Mark elision with apostrophe (e.g., "l'ami")
- Include both written and spoken forms
- Note any irregular pronunciations
- Show gender/number variations
- Include register information

**Pronunciation Aid Guidelines:**
1. **Syllable Division:**
   - Break at natural syllable boundaries
   - Keep one syllable per unit
   - Example: "maison" → mai/son

2. **IPA Usage:**
   - Use simple IPA symbols
   - Mark nasal vowels clearly
   - Show liaison effects
   - Example: "bon" → [bɔ̃]

3. **Common Patterns:**
   - Final consonants often silent
   - Liaison in plural forms
   - Elision before vowels
   - Gender changes affecting pronunciation

4. **Examples of Good Segmentation:**
   - "petit" → pe/tit → [pə/ti]
   - "maison" → mai/son → [mɛ/zɔ̃]
   - "intéressant" → in/té/res/sant → [ɛ̃/te/ʁɛ/sɑ̃]
   - "heureux" → heu/reux → [ø/ʁø] 
### ${language_name} Vocabulary Generation Prompt (v2.0)

**Task:**  
Generate ${num_words} vocabulary entries (${category}) in ${language_name} following the strict JSON format below. **Do not change any key names.** The keys must remain exactly as specified.

**Diversity Requirements:**
- Generate words across different semantic sub-categories of ${category}
${previously_used_words_section}

**Overall JSON Structure:**  
The final output must be a single JSON object with a top-level key `"vocab_examples"`. For example:

```json
{
  "vocab_examples": [
    {
      "language": "${language_code}",
      "group": "${category}",
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
  - Must contain the word in its native script/characters
  - **Do not leave this field empty**
  - Include all necessary diacritical marks or pronunciation guides
- **transliteration**: 
  - The romanized form of the word
  - Must follow standard romanization rules for the language
- **pronunciation_aid**: 
  - An array of objects. Each object must contain:
    - **unit**: A substring representing a natural phonetic grouping
      - **Must not be empty**
      - Must be a meaningful unit in the target language
    - **readings**: An array of strings representing the correct phonetic readings for that unit
      - Must use the language's standard phonetic notation
      - Must accurately reflect the unit's pronunciation in context
- **meaning**: 
  - The English meaning of the word
  - Include any significant variations or nuances
- **part_of_speech**: 
  - The grammatical category (e.g., "${category}")
  - Include any relevant subcategories
- **usage_examples**: 
  - An array of objects, each with:
    - **script**: A sentence using the word
    - **meaning**: The English translation of that sentence
  - Must demonstrate proper grammatical usage
  - Must show different contexts or forms where applicable
- **notes**: 
  - A string providing additional commentary on the word
  - Must include:
    - Common usage contexts
    - Register information (formal/informal)
    - Any irregular forms or special rules
    - Related words or compounds
  - **Must be meaningful and comprehensive**

${language_specific_instructions}

**Instructions for the "pronunciation_aid" Field:**
- Split the word into natural, logical phonetic units
- Do not simply split by individual letters unless that is the natural grouping
- Ensure each unit reflects how the word is pronounced in natural spoken ${language_name}
- All units and their corresponding readings must be non-empty and accurate
- Use standard phonetic notation for the language

**Instructions for the "usage_examples" Field:**
- Provide at least two usage examples per vocabulary entry
- Each example must include a complete sentence using the word and its English translation
- Show different grammatical patterns or forms where applicable
- Include both formal and informal usage where relevant

**Final Output Requirement:**
Generate a complete JSON object containing ${num_words} vocabulary entries for ${language_name} ${category} that strictly follow the structure and rules above. Ensure that the "notes" field is populated with meaningful commentary for each entry, and that no fields are left empty. 
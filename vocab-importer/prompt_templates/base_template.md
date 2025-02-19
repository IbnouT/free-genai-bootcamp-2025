### ${language_name} Vocabulary Generation Prompt

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
- **transliteration**: 
  - The romanized form of the word
- **pronunciation_aid**: 
  - An array of objects. Each object must contain:
    - **unit**: A substring representing a natural phonetic grouping
      - **Must not be empty**
    - **readings**: An array of strings representing the correct phonetic readings for that unit
  - **Important**: Ensure that the readings accurately reflect how the substring is pronounced in the context of the word
- **meaning**: 
  - The English meaning of the word
- **part_of_speech**: 
  - The grammatical category (e.g., "${category}")
- **usage_examples**: 
  - An array of objects, each with:
    - **script**: A sentence using the word
    - **meaning**: The English translation of that sentence
- **notes**: 
  - A string providing additional commentary on the word (usage context, nuances, common usage)
  - **Provide a meaningful note rather than leaving it empty**

${language_specific_instructions}

**Instructions for the "pronunciation_aid" Field:**
- Split the word into natural, logical phonetic units
- Do not simply split by individual letters unless that is the natural grouping
- Ensure each unit reflects how the word is pronounced in natural spoken ${language_name}
- All units and their corresponding readings must be non-empty and accurate

**Instructions for the "usage_examples" Field:**
- Provide at least two usage examples per vocabulary entry
- Each example must include a complete sentence using the word and its English translation

**Final Output Requirement:**
Generate a complete JSON object containing ${num_words} vocabulary entries for ${language_name} ${category} that strictly follow the structure and rules above. Ensure that the "notes" field is populated with meaningful commentary for each entry, and that no fields are left empty. 
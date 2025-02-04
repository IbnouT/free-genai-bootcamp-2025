# ReadMe: Iterative Process for Meta AI (LLaMA 3 70B) Tutor Prompt Design

## **Introduction**
This document captures the iterative process and key learnings from designing a universal AI-powered tutor prompt tailored for Meta AI's LLaMA 3 (70B) model. The goal was to develop a tool capable of guiding users in translating English sentences into target languages (e.g., Japanese, Arabic, French) while focusing on user learning rather than providing direct answers.

## **Objective**
The objective was to create a prompt that could:
- Adapt to multiple languages with dynamic behavior.
- Provide structured vocabulary and sentence guidance without revealing answers.
- Align with specific language rules and proficiency levels.
- Offer a consistent, scalable framework for further expansion.

## **Challenges Identified and Tackled**
This section documents the chronological issues we encountered during the iterative development process and how they were resolved.

### **1. Iterative Refinement with ChatGPT 4.0 and Testing on Meta AI**
#### Process:
Throughout the development, ChatGPT 4.0 was used to iteratively refine and fine-tune the prompt, while Meta AI (LLaMA 3) was used for real-world testing. The process involved designing rules in ChatGPT, testing them on Meta AI, and reporting issues back to ChatGPT for improvements.
#### Key Learnings:
- ChatGPT provided a structured environment for refining prompt rules before testing on Meta AI.
- Each iteration involved testing the prompt on Meta AI, gathering observations, and refining it with ChatGPT.
- Some behaviors were easier to predict and correct in ChatGPT, but Meta AI required stricter rule enforcement to comply with the instructions.

---

### **2. Transition to Meta AI (LLaMA 3)**
#### Challenge:
The Meta AI model exhibited unique behaviors compared to ChatGPT. It required explicit instructions and precise parameterization to adhere to rules.
#### Solution:
- Modified the prompt to emphasize strict compliance with rules.
- Iteratively tested outputs to align with expectations, noting areas where behavior deviated from the defined prompt structure.

---

### **3. Over-informative Outputs**
#### Issue:
Initial prompts allowed the model to provide direct translations or overly detailed grammatical information, bypassing the learning intent.
#### Solution:
- Strictly instructed the model to **not provide direct answers**, even if explicitly requested.
- Introduced a mechanism to deliver hints only when users explicitly indicated they were stuck.

---

### **4. Vocabulary Table Inconsistencies**
#### Issue:
The vocabulary table included irrelevant words such as pronouns, prepositions, and particles that were not part of the target sentence translation.
#### Solution:
- Clearly defined rules to include only core vocabulary directly relevant to the target language sentence.
- Enforced adherence to excluding unnecessary grammatical elements unless essential for the translation.

---

### **5. Misaligned Sentence Structures**
#### Issue:
The sentence structures provided by the model were often inconsistent with the grammar of the target language.
#### Solution:
- Ensured that sentence structures reflect the **natural grammar of the target language**, dynamically aligned to the examples provided.
- Refined examples to include placeholders like `[Subject] [Verb] [Object]` to generalize structures.

---

### **6. Model Ignoring Contextual Rules**
#### Issue:
Despite explicit instructions, the model sometimes ignored key rules, such as not using target-language words in the "Considerations" section.
#### Solution:
- Reinforced rules within the prompt to prioritize compliance with instructions.
- Iteratively tested and adjusted phrasing of the rules to ensure adherence across different inputs.

---

### **7. Multi-language Prompt Generalization**
#### Issue:
Initial prompts were hardcoded for one language, limiting scalability to others.
#### Solution:
- Parameterized the prompt with:
  - `LANGUAGE`: Specifies the target language (e.g., Japanese, Arabic, French).
  - `LEVEL`: Defines proficiency level (e.g., beginner).
  - `DICTIONARY_FORM_DEFINITION`: Describes the expected dictionary form of the words.
- Added dynamic examples for Japanese, Arabic, and French to showcase flexibility.

---

### **8. Unhelpful Considerations and Next Steps**
#### Issue:
The "Considerations" section often included irrelevant grammar details or direct references to target-language words.
#### Solution:
- Simplified and focused considerations to:
  - Highlight essential sentence dynamics (e.g., where location phrases appear).
  - Avoid advanced grammar notes unless directly relevant.
- Provided concise and actionable "Next Steps" to guide users (e.g., "Ask for hints about verb conjugation").

---

## **What We Learned**
### **1. Collaboration Across Tools**
- Using ChatGPT 4.0 as an initial prototyping tool helped refine ideas before transitioning to Meta AI.
- Meta AI required far stricter rules and iterative adjustments to achieve the desired behavior.

### **2. Dynamic Prompting is Critical**
- Allowing parameters like `LANGUAGE` and `LEVEL` made the prompt adaptable to multiple languages and contexts.
- Specific examples and aligned sentence structures ensured language-specific behavior without ambiguity.

### **3. Strict Rule Enforcement**
- Incremental improvements were necessary to ensure the model adhered to the rules. Testing repeatedly with varied inputs highlighted areas where rules needed reinforcement.

### **4. Meta AI-Specific Insights**
- Meta AI's LLaMA model required highly explicit instructions to avoid unintended behaviors.
- Clear sectioning (e.g., System/Instruction, User/Input) and dynamic settings improved compliance and reduced ambiguity in the outputs.

### **5. Collaborative Process**
- Continuous feedback and iterations between user input and system suggestions ensured alignment with expectations.
- The iterative nature of the process allowed us to address both small and systemic issues over time.

## **Final Prompt Features**
### **Sections Included**
1. **System/Instruction:**
   - Defines tutor behavior and rules for outputs.
2. **User/Input:**
   - Specifies input format and interaction.
3. **Rules:**
   - Enforces vocabulary, sentence structure, and compliance.
4. **Examples:**
   - Provides multi-language examples (Japanese, Arabic, French).
5. **Settings:**
   - Enables parameterization for language, proficiency level, and dictionary forms.

## **Next Steps**
- Add support for more languages (e.g., Spanish, German) by creating language-specific examples.
- Expand to intermediate and advanced levels, adjusting rules and considerations accordingly.
- Test the prompt across other LLaMA-based models or alternative frameworks to ensure adaptability and performance.

---
**Authors:** This iterative process was documented through extensive testing with Meta AI's LLaMA 3 model. Challenges were addressed collaboratively with a focus on creating a robust, user-centric tutor prompt.

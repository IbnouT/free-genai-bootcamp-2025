# Context Restoration Prompt

When restarting Cursor, use this prompt to restore the context:

```
I'm working on the Vocab Importer project. Please analyze these files in order to understand the current context and next steps:

1. vocab-importer/docs/context_restoration.md
2. vocab-importer/implementation-plan.md
3. vocab-importer/tech-specs/technical-specs.md
4. vocab-importer/docs/session_context.md
5. vocab-importer/docs/llm_iterations.md

We're currently:
1. Finishing Phase 3.1 (responsive layout implementation)
2. About to start Phase 3.3 (Review & Edit Interface)
3. Maintaining >90% test coverage
4. Following Streamlit-only implementation

Please help me continue the development from where we left off.
```

## Usage Instructions
1. Copy the entire prompt between the backticks
2. Paste it as your first message when restarting Cursor
3. The AI will analyze the files and restore the development context
4. You can then continue with development tasks

## Note
- The prompt is designed to give the AI the essential context quickly
- Files are listed in order of importance for context restoration
- Current phase and key requirements are explicitly stated
- This ensures consistent context across development sessions 
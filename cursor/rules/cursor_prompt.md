# Prompt for Cursor

**Context**: We have two specification documents (front-end and back-end) describing a language-learning portal using React + TypeScript + Vite (front-end) and FastAPI + SQLite (back-end). We want to implement the entire system in small, testable increments, with thorough unit tests for each step.

IMPORTANT: USE THE FOLDER `lang-portal` as the root folder 
**Your Tasks**:
1. **Analyze Our Specs**  
   - Read or parse the details from `FRONTEND_SPEC.md` and `BACKEND_SPEC.md` (in `docs/`), or from any relevant instructions you already have in your context.

2. **Generate a Requirements & Environment Setup**  
   - Create a Python virtual environment (`venv`) for the back-end and produce a `requirements.txt` (or `pyproject.toml`) that includes FastAPI, SQLAlchemy, Pytest, etc.  
   - For the front-end, create a `package.json` (or update existing) that includes React, TypeScript, Vite, Material UI, React Router, Axios, plus testing libraries (Jest or Vitest + React Testing Library).  
   - Provide short “Coding Standards” or “Best Practices” docs (PEP 8 for Python, Prettier/ESLint for JS/TS, etc.).

3. **Create a Stepwise Plan with Checkboxes**  
   - Outline each small feature/step in a list, using Markdown checkboxes, for example:
     ```
     - [ ] Step 1: Initialize repo, set up venv, etc.
     - [ ] Step 2: Implement X with its tests
     - [ ] Step 3: ...
     ```
   - Each time a step is completed and tested successfully, mark it `- [x] Step 1: ...`.

4. **Implement TDD**  
   - For each step, produce minimal code plus unit tests (Pytest for back-end, Jest/Vitest for front-end).
   - Wait for my validation (“OK, proceed.”) before marking it checked and moving on.

5. **Keep Specs in Mind**  
   - Follow the structure/endpoints in `BACKEND_SPEC.md` (FastAPI + SQLite).
   - Follow the folder layout, pages, theming details from `FRONTEND_SPEC.md` (React + TS + Vite + Material UI).

6. **Deliverables**:
   1. A multi-step plan, each step with a checkbox.
   2. Requirements files (`requirements.txt` for Python, `package.json` for front-end).
   3. A best-practices doc (markdown) for coding standards.
   4. Minimal or initial code scaffolding for each step, with test files included.

7. **Completion**  
   - Once all steps are checked and validated, we’ll have a fully tested, multi-language learning portal.

**Now**: Please begin by analyzing the specs, generating the environment config files, and giving me a clear checklist of steps with checkboxes. Then await my confirmation before proceeding with each step.

# Coding Standards

## Backend (Python)

1. **Code Style**
   - Follow PEP 8 conventions
   - Use 4 spaces for indentation
   - Maximum line length: 88 characters (Black formatter standard)
   - Use meaningful variable names in snake_case
   - Use type hints for function parameters and return values

2. **Testing**
   - Write tests for all endpoints and business logic
   - Use pytest fixtures for database setup
   - Aim for >80% test coverage
   - Test both success and error cases

3. **Documentation**
   - Document all public functions and classes using docstrings
   - Include type hints in function signatures
   - Comment complex logic or business rules

## Frontend (TypeScript/React)

1. **Code Style**
   - Use Prettier for consistent formatting
   - Use ESLint with recommended React/TypeScript rules
   - Use 2 spaces for indentation
   - Maximum line length: 80 characters
   - Use meaningful variable names in camelCase
   - Use PascalCase for component names

2. **React Best Practices**
   - Use functional components with hooks
   - Keep components small and focused
   - Use TypeScript interfaces for props
   - Avoid prop drilling (use Context when needed)
   - Extract reusable logic into custom hooks

3. **Testing**
   - Write tests for all components
   - Use React Testing Library for component tests
   - Test user interactions and rendering
   - Mock API calls in tests
   - Aim for >80% test coverage

4. **State Management**
   - Use React Query for server state
   - Use local state for UI-only state
   - Keep state as close as possible to where it's used

5. **File Organization**
   - One component per file
   - Group related components in feature folders
   - Use index.ts files for clean exports
   - Keep styles close to components 
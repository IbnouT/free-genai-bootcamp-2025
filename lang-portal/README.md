# Language Learning Portal

A modern, full-stack web application for language learning, featuring an interactive study system with multiple learning activities and progress tracking.

## Overview

The Language Learning Portal provides a structured environment for learning multiple languages through various study activities. It supports multiple languages (currently Japanese, French, Arabic, and Spanish active, with more planned) and offers different learning approaches tailored to each language's unique characteristics.

## Key Features

- **Multi-Language Support**
  - Active support for Japanese, French, Arabic, and Spanish
  - Language-specific learning activities
  - Customized study approaches for different writing systems

- **Study Activities**
  - Interactive flashcards for vocabulary practice
  - Typing practice with language-specific input support
  - Multiple choice quizzes for knowledge testing
  - Character writing practice (for languages like Japanese)
  - Pronunciation practice with voice recognition

- **Learning Organization**
  - Structured word groups by category
  - Progress tracking per language
  - Study session history
  - Performance statistics and analytics

- **Progress Dashboard**
  - Study streak tracking
  - Success rate monitoring
  - Active study groups overview
  - Monthly progress visualization

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.1
- **Server**: Uvicorn 0.27.0
- **Database**: SQLite with SQLAlchemy 2.0.25
- **Migrations**: Alembic 1.13.1
- **Validation**: Pydantic 2.6.1
- **Testing**: pytest 8.0.0 with pytest-cov 4.1.0

### Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **State Management**: React Context
- **Routing**: React Router
- **HTTP Client**: Axios
- **Development**: ESLint, Prettier

## Project Structure
```
lang-portal/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── core/              # Core configuration
│   │   ├── routers/           # API endpoints
│   │   ├── utils/             # Utility functions
│   │   ├── models/            # Database model definitions
│   │   ├── main.py           # Application entry point
│   │   ├── database.py       # Database configuration
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   └── seed.py          # Database seeding script
│   ├── tests/                 # Test suite
│   │   ├── routers/          # API endpoint tests
│   │   ├── conftest.py      # Test configuration
│   │   └── test_*.py        # Various test modules
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   ├── pytest.ini            # Pytest configuration
│   └── README.md             # Backend documentation
├── frontend/                  # React application
│   ├── src/
│   │   ├── api/              # API client services
│   │   ├── components/       # Reusable UI components
│   │   ├── context/          # React context providers
│   │   ├── images/           # Static images
│   │   ├── pages/            # Page components
│   │   ├── routes/           # Route definitions
│   │   ├── test/             # Test utilities
│   │   ├── theme/            # MUI theme customization
│   │   ├── types/            # TypeScript definitions
│   │   ├── utils/            # Utility functions
│   │   ├── App.tsx          # Root component
│   │   ├── Layout.tsx       # Main layout component
│   │   ├── routes.tsx       # Route configuration
│   │   └── main.tsx         # Application entry point
│   ├── public/                # Static assets
│   ├── package.json          # NPM dependencies
│   └── vite.config.ts        # Vite configuration
├── docs/                      # Project documentation
│   ├── implementation-plan.md # Development roadmap
│   └── coding-standards.md   # Code style guide
└── tech-specs/               # Technical specifications
    ├── backend-technical-specs.md
    ├── frontend-technical-specs.md
    └── data_model_mermaid_diagram.png
```

## Getting Started

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   python -m app.seed
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Development Status

- ✅ **Backend**: Complete implementation with 100% test coverage
- 🚧 **Frontend**: In active development
  - ✅ Language selection page
  - ✅ Basic layout components (navigation, topbar)
  - 🚧 dashboard and other features in progress

For detailed development progress and upcoming features, see the [Implementation Plan](docs/implementation-plan.md).

## Documentation

- Backend API: http://localhost:8000/docs (when running)
- Technical Specifications: `/tech-specs/`
- Implementation Plan: `/docs/implementation-plan.md` 
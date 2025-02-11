# Language Learning Portal

A full-stack application for language learning built with FastAPI and React.

## Directory Structure
```
lang-portal/
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── main.py       # FastAPI entry point
│   │   ├── db.py         # SQLite connection & session
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic models
│   │   └── routers/      # API endpoints
│   ├── tests/            # Backend tests
│   └── requirements.txt  
├── frontend/             # React + Vite application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   └── theme/        # MUI theme
│   └── package.json
└── docs/                 # Documentation
    └── coding-standards.md
``` 
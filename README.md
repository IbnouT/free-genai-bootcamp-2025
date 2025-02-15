# Language Learning Portal

A web application for learning multiple languages through interactive study activities.

## Project Structure

```
lang-portal/
├── backend/         # FastAPI backend
├── frontend/        # React frontend
└── tech-specs/      # Technical specifications
```

## Quick Start

1. Start Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. Start Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Documentation

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Technical Specifications](tech-specs/)

## Development

See individual README files in backend/ and frontend/ directories for detailed setup instructions.

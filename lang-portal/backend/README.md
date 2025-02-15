# Language Learning Portal - Backend

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment:
```bash
# Copy example env file
cp .env.example .env

# Edit .env file to set:
ENVIRONMENT=development
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

The server will start at http://localhost:8000

## API Endpoints

### Languages
- GET `/languages` - List all languages
- GET `/languages?active=true` - List active languages only

Example usage:
```bash
# Get all languages
curl 'http://localhost:8000/languages'

# Get active languages only
curl 'http://localhost:8000/languages?active=true'
```

### Words
- GET `/words` - List all words
- GET `/words?language_code=ja` - Filter words by language

### Admin
- POST `/admin/seed` - Reset and seed database with initial data

## Development

### Database
- SQLite database is created automatically on first run
- In development, database is auto-seeded with sample data
- Use admin/seed endpoint to reset database

### Testing
```bash
pytest
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 
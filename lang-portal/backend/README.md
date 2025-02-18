# Language Learning Portal - Backend

This is the FastAPI backend for the Language Learning Portal.

## Framework & Dependencies

- **Web Framework**: FastAPI 0.109.1 with Uvicorn 0.27.0
- **Database**: SQLite with SQLAlchemy 2.0.25 and Alembic 1.13.1
- **Data Validation**: Pydantic 2.6.1
- **Testing**: pytest 8.0.0 with FastAPI TestClient and pytest-cov 4.1.0

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database (see Database Management section below)

4. Start the development server:
```bash
uvicorn app.main:app --reload
```

## Database Management

### Complete Database Reset
If you need to completely reset the database and start fresh:

1. Stop any running FastAPI server

2. Delete existing database and migrations:
```bash
# Remove the SQLite database
rm -f app/app.db

# Remove all existing migration versions
rm -f alembic/versions/*.py
```

3. Create and apply new initial migration:
```bash
# Generate new initial migration
alembic revision --autogenerate -m "initial"

# Apply the migration
alembic upgrade head
```

4. Seed the database using the seed script:
```bash
# Make sure you're in the backend directory
cd lang-portal/backend

# Run the seed script
python -m app.seed

# Or to include test data (study sessions, reviews, etc.)
python -m app.seed --include-test-data
```

The seed script will:
- Add default languages (Japanese, French, Arabic, Spanish)
- Create sample words for each language
- Set up study activity types (Flashcards, Typing Practice, etc.)
- Create default word groups (Core Verbs, Common Phrases, etc.)
- Optionally create test study sessions and reviews if --include-test-data is used

### Common Database Operations

#### Creating New Migrations
When you make changes to the models:
```bash
alembic revision --autogenerate -m "description_of_changes"
alembic upgrade head
```

#### Viewing Migration History
```bash
# Show current migration version
alembic current

# Show migration history
alembic history
```

#### Rolling Back Migrations
```bash
# Roll back one migration
alembic downgrade -1

# Roll back to specific migration
alembic downgrade <migration_id>

# Roll back all migrations
alembic downgrade base
```

### Troubleshooting

1. **"Target database is not up to date" error**
   - This usually means there are pending migrations
   - Solution: Run `alembic upgrade head`

2. **"Can't locate revision" error**
   - This can happen when migration files are missing or corrupted
   - Solution: Follow the Complete Database Reset steps above

3. **Database locked error**
   - Make sure no other processes are using the database
   - Close any DB browser applications
   - Stop the FastAPI server if running

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── app/
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic models
│   ├── database.py       # Database configuration
│   ├── main.py          # FastAPI application
│   ├── seed.py          # Database seeding
│   └── routers/         # API endpoints
├── tests/               # Test files
├── alembic.ini          # Alembic configuration
└── requirements.txt     # Python dependencies
```

## API Documentation

When the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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

#### Database Migrations
When making changes to database schema:
```bash
# Reset database and run migrations (WARNING: This will delete all data!)
python -m app.utils.reset_and_migrate

# Create new migration
alembic revision --autogenerate -m "add promo_text to language"
```

### Testing

The project has 100% test coverage using:
- pytest with FastAPI TestClient
- pytest-cov for coverage reporting
- In-memory SQLite for isolated database testing

#### Running Tests
```bash
# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/routers/test_dashboard.py
```

#### Test Structure
```
tests/
├── conftest.py          # Shared fixtures
├── test_database.py     # Database configuration tests
├── test_dependencies.py # Dependency tests
├── test_main.py         # App configuration tests
├── test_models.py       # SQLAlchemy models tests
├── test_seed.py         # Database seeding tests
└── routers/            # API endpoint tests
    ├── test_activities.py
    ├── test_admin.py
    ├── test_dashboard.py
    ├── test_groups.py
    ├── test_languages.py
    ├── test_sessions.py
    └── test_words.py
```

Key features:
- Isolated test database per session
- Automatic cleanup after each test
- Environment control via monkeypatch
- Comprehensive fixtures in conftest.py

---------- coverage: platform darwin, python 3.11.7-final-0 
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
app/__init__.py                 0      0   100%
app/core/config.py              7      0   100%
app/database.py                18      0   100%
app/dependencies.py             4      0   100%
app/main.py                    47      0   100%
app/models.py                  67      0   100%
app/routers/activities.py      36      0   100%
app/routers/admin.py           10      0   100%
app/routers/dashboard.py       46      0   100%
app/routers/groups.py          49      0   100%
app/routers/languages.py       13      0   100%
app/routers/sessions.py        57      0   100%
app/routers/words.py           36      0   100%
app/schemas.py                137      0   100%
app/seed.py                   159      0   100%
app/utils/db_utils.py           5      0   100%
---------------------------------------------------------
TOTAL                         691      0   100%
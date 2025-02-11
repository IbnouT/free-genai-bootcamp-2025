from sqlalchemy import text
from app.database import get_db

def test_database_connection():
    db = next(get_db())
    try:
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        db.close() 
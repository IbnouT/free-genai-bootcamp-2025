from app.utils.db_utils import reset_database
from app.database import engine
from sqlalchemy import text

def test_reset_database():
    # Test that we can reset the database without errors
    reset_database()
    # Verify we can still connect after reset
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1 
from app.database import get_db_url
from app.utils.db_utils import reset_database
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command

def reset_and_migrate():
    """Reset database and run migrations"""
    # Create engine
    engine = create_engine(get_db_url())
    
    # Reset database
    print("Resetting database...")
    reset_database(engine)
    
    # Run migrations
    print("Running migrations...")
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")  # Mark current as head
    command.upgrade(alembic_cfg, "head") # Run migrations
    
    print("Database reset and migrated successfully!")

if __name__ == "__main__":
    reset_and_migrate() 
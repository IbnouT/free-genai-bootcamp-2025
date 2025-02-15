from fastapi import HTTPException, Depends
from app.database import get_db

def admin_only():
    """Dependency for admin-only routes"""
    # TODO: Add proper admin authentication
    # For now, allow all requests in development
    return True 
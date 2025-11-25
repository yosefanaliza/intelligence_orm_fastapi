"""
Database configuration and engine
"""
from sqlmodel import create_engine, SQLModel
from config import settings

# Create engine
engine = create_engine(settings.DATABASE_URI, echo=True)


def create_db_and_tables():
    """Create all tables defined in SQLModel models"""
    SQLModel.metadata.create_all(engine)


def get_engine():
    """
    Dependency function to get database engine for FastAPI
    Used for dependency injection in route handlers
    """
    return engine

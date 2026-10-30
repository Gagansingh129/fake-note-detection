"""
NoteGuard AI - Database Engine & Session Management
===================================================
Configures SQLite database connection using SQLAlchemy.
Architecture is fully compatible with future PostgreSQL migration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Create SQLite engine with multi-threading compatibility
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI dependency for yielding database session with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes tables in database."""
    from pathlib import Path
    if settings.DATABASE_URL.startswith("sqlite:///"):
        db_file = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
        db_file.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)

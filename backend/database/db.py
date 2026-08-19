"""
Engine + session setup for Kadam.

Usage:
    from database.db import get_db, init_db
    init_db()  # creates tables if they don't exist
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./kadam.db")

engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables. Safe to call repeatedly — no-ops if they exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency: yields a session, closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

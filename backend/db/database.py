"""
Database configuration and session management module.

This module handles SQLAlchemy setup, including database engine creation,
session factory configuration, and database utilities for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

# Create the database engine using the configured database URL
engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM model classes
Base = declarative_base()


def get_db():
    """
    Dependency function for database session management.
    
    Provides a SQLAlchemy database session for use in FastAPI route handlers.
    Automatically closes the session after the request is complete.
    
    Yields:
        Session: A SQLAlchemy database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables defined in the ORM models.
    
    Executes CREATE TABLE statements for all model classes that inherit
    from Base. Safe to call multiple times as it only creates tables that
    don't already exist.
    """
    Base.metadata.create_all(bind=engine)
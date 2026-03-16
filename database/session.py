"""This module configures the database connection and session management.

Provides the SQLAlchemy engine, session factory, and FastAPI dependency
for database access. Also handles initial table creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL, LOG_LEVEL

from database.base import Base
from models.candidate import Candidate
from models.experience import Experience
from models.language import Language
from models.qualification import Qualification
from models.qualification import QualificationField
from models.skill import Skill

engine = create_engine(DATABASE_URL, echo=(LOG_LEVEL == "DEBUG"))
SESSION_LOCAL = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that provides a database session.

    Yields:
        Database session for making queries.
    """
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()

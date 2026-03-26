"""This module configures the database connection and session management.

Provides the SQLAlchemy engine, session factory, and FastAPI dependency
for database access. Also handles initial table creation.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from database.base import Base
from models.candidate_profile import CandidateProfile
from models.experience import Experience
from models.language import Language
from models.qualification import Qualification
from models.qualification import QualificationField
from models.skill import Skill

engine = create_engine(settings.database_url, echo=(settings.log_level == "DEBUG"))


# Enable FK enforcement for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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

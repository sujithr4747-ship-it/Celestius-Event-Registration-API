
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file will be created in the project root.
DATABASE_URL = "sqlite:///./celestius.db"

# SQLite needs this setting for connections used across FastAPI threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Each request can use its own database session.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all database models.
Base = declarative_base()


def get_db():
    """Provide a database session and always close it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

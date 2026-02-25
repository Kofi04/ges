"""Configuration SQLAlchemy et gestion des sessions"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database import Base

# Créer le moteur de base de données
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

# Créer une fabrique de session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dépendance pour obtenir une session de base de données
    À utiliser avec FastAPI pour injecter une session dans les endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Modèles SQLAlchemy pour la base de données"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Etudiant(Base):
    """Modèle de table pour les étudiants"""
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    date_naissance = Column(Date, nullable=False)
    numero_etudiant = Column(String(20), unique=True, nullable=False, index=True)
    filiere = Column(String(100), nullable=False)
    moyenne = Column(Float, default=0.0)
    date_inscription = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Etudiant(id={self.id}, nom={self.nom}, prenom={self.prenom})>"

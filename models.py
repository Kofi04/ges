"""Modèles Pydantic pour la validation des données"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class EtudiantBase(BaseModel):
    """Modèle de base pour un étudiant"""
    nom: str = Field(..., min_length=1, max_length=100, description="Nom complet de l'étudiant")
    prenom: str = Field(..., min_length=1, max_length=100, description="Prénom de l'étudiant")
    email: EmailStr = Field(..., description="Adresse email unique")
    date_naissance: date = Field(..., description="Date de naissance")
    numero_etudiant: str = Field(..., min_length=5, max_length=20, description="Numéro étudiant unique")
    filiere: str = Field(..., min_length=1, max_length=100, description="Filière d'études")
    moyenne: Optional[float] = Field(0.0, ge=0, le=20, description="Moyenne générale (0-20)")

class EtudiantCreate(EtudiantBase):
    """Modèle pour créer un étudiant"""
    pass

class EtudiantUpdate(BaseModel):
    """Modèle pour mettre à jour un étudiant (tous les champs optionnels)"""
    nom: Optional[str] = Field(None, min_length=1, max_length=100)
    prenom: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    date_naissance: Optional[date] = None
    numero_etudiant: Optional[str] = Field(None, min_length=5, max_length=20)
    filiere: Optional[str] = Field(None, min_length=1, max_length=100)
    moyenne: Optional[float] = Field(None, ge=0, le=20)

class EtudiantReponse(EtudiantBase):
    """Modèle pour la réponse (inclut l'ID)"""
    id: int = Field(..., description="Identifiant unique de l'étudiant")
    
    class Config:
        from_attributes = True  # Permet de mapper les objets SQLAlchemy

class MessageReponse(BaseModel):
    """Modèle pour les messages de réponse simples"""
    message: str
    code: str = "success"

"""Configuration de l'application"""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./etudiants.db")

# Paramètres du serveur
DEBUG = os.getenv("DEBUG", "true").lower() in {"1", "true", "yes", "y"}
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

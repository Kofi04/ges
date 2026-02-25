"""
Application FastAPI pour gérer les étudiants
Auteur: Votre nom
Version: 1.0.0
"""

from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse  # pyright: ignore[reportMissingImports]
from routes_etudiants import router as etudiants_router
from db_config import init_db
import os

# Créer l'application FastAPI
app = FastAPI(
    title="Gestion des Étudiants API",
    description="API pour gérer les informations des étudiants",
    version="1.0.0",
    contact={
        "name": "Support",
        "email": "support@exemple.com"
    },
    license_info={
        "name": "MIT"
    }
)

# ==================== CONFIGURATION CORS ====================
# Permet à d'autres domaines d'accéder à votre API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accepte les requêtes de tous les domaines
    allow_credentials=True,
    allow_methods=["*"],  # Accepte tous les types de requêtes (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Accepte tous les en-têtes
)

# ==================== INCLURE LES ROUTES ====================
app.include_router(etudiants_router)

@app.on_event("startup")
def on_startup():
    init_db()

# ==================== FRONTEND (UI) ====================
@app.get("/", include_in_schema=False)
def ui():
    return FileResponse("index.html")

# ==================== ROUTE INFO API ====================
@app.get("/api", tags=["Info"])
def api_info():
    return {
        "message": "Bienvenue sur l'API de gestion des étudiants",
        "version": "1.0.0",
        "documentation": "/docs",
        "documentation_alternative": "/redoc",
    }

# ==================== ENDPOINT DE SANTÉ ====================
@app.get("/health", tags=["Info"])
def health_check():
    """
    Endpoint de santé - utilisé pour vérifier que l'API est opérationnelle
    """
    return {
        "status": "healthy",
        "service": "API Gestion Étudiants"
    }

# ==================== GESTION DES ERREURS ====================
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Gestionnaire d'erreurs global"""
    return {
        "erreur": str(exc),
        "type": type(exc).__name__
    }

if __name__ == "__main__":
    import uvicorn  # pyright: ignore[reportMissingImports]
    
    # Lancer le serveur
    uvicorn.run(
        app,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=True  # Rechargement automatique en cas de modifications
    )

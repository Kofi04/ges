"""Routes pour la gestion des étudiants"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import Etudiant
from models import EtudiantCreate, EtudiantUpdate, EtudiantReponse, MessageReponse
from db_config import get_db
from typing import List

router = APIRouter(
    prefix="/etudiants",
    tags=["Étudiants"],
    responses={404: {"description": "Étudiant non trouvé"}}
)

# ==================== CRÉER UN ÉTUDIANT ====================
@router.post("/", response_model=EtudiantReponse, status_code=201)
def creer_etudiant(etudiant: EtudiantCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel étudiant
    
    - **nom**: Nom complet (obligatoire)
    - **prenom**: Prénom (obligatoire)
    - **email**: Email unique (obligatoire)
    - **date_naissance**: Date de naissance (obligatoire)
    - **numero_etudiant**: Numéro étudiant unique (obligatoire)
    - **filiere**: Filière d'études (obligatoire)
    - **moyenne**: Moyenne générale optionnelle (0-20)
    """
    
    # Vérifier si l'email existe déjà
    db_etudiant = db.query(Etudiant).filter(Etudiant.email == etudiant.email).first()
    if db_etudiant:
        raise HTTPException(status_code=400, detail="Cet email existe déjà")
    
    # Vérifier si le numéro étudiant existe déjà
    db_etudiant = db.query(Etudiant).filter(Etudiant.numero_etudiant == etudiant.numero_etudiant).first()
    if db_etudiant:
        raise HTTPException(status_code=400, detail="Ce numéro étudiant existe déjà")
    
    # Créer le nouvel étudiant
    nouvel_etudiant = Etudiant(**etudiant.dict())
    db.add(nouvel_etudiant)
    db.commit()
    db.refresh(nouvel_etudiant)
    
    return nouvel_etudiant

# ==================== LISTER TOUS LES ÉTUDIANTS ====================
@router.get("/", response_model=List[EtudiantReponse])
def lister_etudiants(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(10, ge=1, le=100, description="Nombre d'éléments à retourner"),
    filiere: str = Query(None, description="Filtrer par filière"),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les étudiants avec pagination
    
    - **skip**: Nombre d'éléments à sauter (défaut: 0)
    - **limit**: Nombre d'éléments à retourner (défaut: 10, max: 100)
    - **filiere**: Filtrer par filière (optionnel)
    """
    
    query = db.query(Etudiant)
    
    # Appliquer le filtre de filière si fourni
    if filiere:
        query = query.filter(Etudiant.filiere == filiere)
    
    # Appliquer la pagination
    etudiants = query.offset(skip).limit(limit).all()
    
    return etudiants

# ==================== RÉCUPÉRER UN ÉTUDIANT PAR ID ====================
@router.get("/{etudiant_id}", response_model=EtudiantReponse)
def obtenir_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Récupère un étudiant spécifique par son ID
    
    - **etudiant_id**: ID de l'étudiant
    """
    
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    return etudiant

# ==================== METTRE À JOUR UN ÉTUDIANT ====================
@router.put("/{etudiant_id}", response_model=EtudiantReponse)
def modifier_etudiant(
    etudiant_id: int,
    etudiant_update: EtudiantUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour un étudiant existant (partiellement ou complètement)
    
    - **etudiant_id**: ID de l'étudiant à modifier
    - Les champs fournis seront mis à jour, les autres restent inchangés
    """
    
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    # Mettre à jour uniquement les champs fournis
    donnees_update = etudiant_update.dict(exclude_unset=True)
    
    # Vérifier l'unicité de l'email s'il est modifié
    if "email" in donnees_update:
        email_existant = db.query(Etudiant).filter(
            Etudiant.email == donnees_update["email"],
            Etudiant.id != etudiant_id
        ).first()
        if email_existant:
            raise HTTPException(status_code=400, detail="Cet email existe déjà")
    
    # Vérifier l'unicité du numéro étudiant s'il est modifié
    if "numero_etudiant" in donnees_update:
        numero_existant = db.query(Etudiant).filter(
            Etudiant.numero_etudiant == donnees_update["numero_etudiant"],
            Etudiant.id != etudiant_id
        ).first()
        if numero_existant:
            raise HTTPException(status_code=400, detail="Ce numéro étudiant existe déjà")
    
    for key, value in donnees_update.items():
        setattr(etudiant, key, value)
    
    db.commit()
    db.refresh(etudiant)
    
    return etudiant

# ==================== SUPPRIMER UN ÉTUDIANT ====================
@router.delete("/{etudiant_id}", response_model=MessageReponse)
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Supprime un étudiant de la base de données
    
    - **etudiant_id**: ID de l'étudiant à supprimer
    """
    
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    db.delete(etudiant)
    db.commit()
    
    return {"message": f"L'étudiant {etudiant.prenom} {etudiant.nom} a été supprimé avec succès", "code": "deleted"}

# ==================== STATISTIQUES ====================
@router.get("/stats/resume", response_model=dict)
def obtenir_statistiques(db: Session = Depends(get_db)):
    """
    Récupère des statistiques sur les étudiants
    """
    
    total_etudiants = db.query(Etudiant).count()
    
    # Moyenne des moyennes
    from sqlalchemy import func
    moyenne_globale = db.query(func.avg(Etudiant.moyenne)).scalar()
    moyenne_globale = round(moyenne_globale, 2) if moyenne_globale else 0
    
    # Meilleur étudiant
    meilleur = db.query(Etudiant).order_by(Etudiant.moyenne.desc()).first()
    
    # Nombre d'étudiants par filière
    filieres = db.query(Etudiant.filiere, func.count(Etudiant.id)).group_by(Etudiant.filiere).all()
    filieres_dict = {filiere: count for filiere, count in filieres}
    
    return {
        "total_etudiants": total_etudiants,
        "moyenne_globale": moyenne_globale,
        "meilleur_etudiant": {
            "nom": f"{meilleur.prenom} {meilleur.nom}",
            "moyenne": meilleur.moyenne
        } if meilleur else None,
        "etudiants_par_filiere": filieres_dict
    }

# ==================== RECHERCHE AVANCÉE ====================
@router.get("/search/par-nom", response_model=List[EtudiantReponse])
def rechercher_par_nom(
    query: str = Query(..., min_length=1, description="Terme de recherche"),
    db: Session = Depends(get_db)
):
    """
    Recherche un étudiant par son nom ou prénom
    
    - **query**: Terme de recherche (minimum 1 caractère)
    """
    
    etudiants = db.query(Etudiant).filter(
        (Etudiant.nom.ilike(f"%{query}%")) |
        (Etudiant.prenom.ilike(f"%{query}%"))
    ).all()
    
    if not etudiants:
        raise HTTPException(status_code=404, detail="Aucun étudiant trouvé")
    
    return etudiants

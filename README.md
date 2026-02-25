# 📚 Guide Complet - API Gestion des Étudiants

## 📁 Structure du Projet

```
mon_api_etudiants/
├── main.py                 # Point d'entrée principal
├── config.py              # Configuration de l'application
├── database.py            # Modèles SQLAlchemy
├── db_config.py          # Configuration de la base de données
├── models.py             # Modèles Pydantic
├── routes_etudiants.py   # Routes/endpoints
├── test_api.py           # Tests automatisés
├── requirements.txt      # Dépendances
└── etudiants.db         # Base de données SQLite (créée automatiquement)
```

## 🚀 Installation et Lancement

### Étape 1 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 2 : Lancer le serveur

```bash
uvicorn main:app --reload
```

Vous verrez:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Étape 3 : Accéder à la documentation

- **Documentation interactive (Swagger UI)** : http://127.0.0.1:8000/docs
- **Documentation alternative (ReDoc)** : http://127.0.0.1:8000/redoc

## 📡 Endpoints Disponibles

### 1. Information API
```
GET /              - Information générale
GET /health        - Vérifier la santé de l'API
```

### 2. Gestion des Étudiants

#### Créer un étudiant
```
POST /etudiants/

Body JSON:
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "date_naissance": "2003-05-15",
  "numero_etudiant": "ETU001",
  "filiere": "Informatique",
  "moyenne": 16.5
}

Réponse (201):
{
  "id": 1,
  "nom": "Dupont",
  "prenom": "Jean",
  ...
}
```

#### Lister tous les étudiants
```
GET /etudiants/

Paramètres optionnels:
- skip: nombre d'éléments à sauter (défaut: 0)
- limit: nombre d'éléments à retourner (défaut: 10, max: 100)
- filiere: filtrer par filière

Exemple: GET /etudiants/?skip=0&limit=5&filiere=Informatique
```

#### Obtenir un étudiant
```
GET /etudiants/{etudiant_id}

Exemple: GET /etudiants/1
```

#### Mettre à jour un étudiant
```
PUT /etudiants/{etudiant_id}

Body JSON (tous les champs optionnels):
{
  "moyenne": 17.5,
  "filiere": "Informatique - IA"
}

Exemple: PUT /etudiants/1
```

#### Supprimer un étudiant
```
DELETE /etudiants/{etudiant_id}

Exemple: DELETE /etudiants/1

Réponse:
{
  "message": "L'étudiant Jean Dupont a été supprimé avec succès",
  "code": "deleted"
}
```

#### Rechercher par nom
```
GET /etudiants/search/par-nom?query=Martin

Retourne tous les étudiants dont le nom ou prénom contient "Martin"
```

#### Obtenir les statistiques
```
GET /etudiants/stats/resume

Réponse:
{
  "total_etudiants": 5,
  "moyenne_globale": 16.2,
  "meilleur_etudiant": {
    "nom": "Paul Bernard",
    "moyenne": 18.0
  },
  "etudiants_par_filiere": {
    "Informatique": 3,
    "Mathématiques": 2
  }
}
```

## 🧪 Tester l'API

### Méthode 1 : Interface Web Swagger UI (Recommandée)

1. Allez sur http://127.0.0.1:8000/docs
2. Cliquez sur l'endpoint que vous voulez tester
3. Cliquez sur "Try it out"
4. Remplissez les paramètres
5. Cliquez sur "Execute"

### Méthode 2 : Script Python

```bash
python test_api.py
```

Ce script teste automatiquement tous les endpoints.

### Méthode 3 : Utiliser curl (Terminal)

```bash
# Créer un étudiant
curl -X POST http://127.0.0.1:8000/etudiants/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "date_naissance": "2003-05-15",
    "numero_etudiant": "ETU001",
    "filiere": "Informatique",
    "moyenne": 16.5
  }'

# Lister les étudiants
curl http://127.0.0.1:8000/etudiants/

# Obtenir un étudiant
curl http://127.0.0.1:8000/etudiants/1

# Mettre à jour
curl -X PUT http://127.0.0.1:8000/etudiants/1 \
  -H "Content-Type: application/json" \
  -d '{"moyenne": 17.5}'

# Supprimer
curl -X DELETE http://127.0.0.1:8000/etudiants/1
```

### Méthode 4 : Postman

1. Téléchargez Postman (https://www.postman.com)
2. Créez une nouvelle requête
3. Entrez l'URL: `http://127.0.0.1:8000/etudiants/`
4. Sélectionnez la méthode (GET, POST, PUT, DELETE)
5. Entrez les données JSON dans "Body"
6. Cliquez sur "Send"

## 📊 Exemples d'Utilisation en Python

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Créer un étudiant
etudiant = {
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "date_naissance": "2003-05-15",
    "numero_etudiant": "ETU001",
    "filiere": "Informatique",
    "moyenne": 16.5
}

response = requests.post(f"{BASE_URL}/etudiants/", json=etudiant)
print(response.json())

# 2. Lister les étudiants
response = requests.get(f"{BASE_URL}/etudiants/")
etudiants = response.json()
for etu in etudiants:
    print(f"{etu['prenom']} {etu['nom']}")

# 3. Obtenir un étudiant
response = requests.get(f"{BASE_URL}/etudiants/1")
etudiant = response.json()
print(etudiant)

# 4. Mettre à jour
response = requests.put(f"{BASE_URL}/etudiants/1", json={"moyenne": 18.0})
print(response.json())

# 5. Supprimer
response = requests.delete(f"{BASE_URL}/etudiants/1")
print(response.json())

# 6. Rechercher
response = requests.get(f"{BASE_URL}/etudiants/search/par-nom?query=Dupont")
print(response.json())

# 7. Statistiques
response = requests.get(f"{BASE_URL}/etudiants/stats/resume")
stats = response.json()
print(f"Nombre d'étudiants: {stats['total_etudiants']}")
print(f"Moyenne: {stats['moyenne_globale']}")
```

## 🔍 Détail des Modèles de Données

### Étudiant
```
{
  "id": 1,                              # Auto-généré
  "nom": "Dupont",                      # String (1-100 caractères)
  "prenom": "Jean",                     # String (1-100 caractères)
  "email": "jean.dupont@example.com",   # Email unique
  "date_naissance": "2003-05-15",       # Date (YYYY-MM-DD)
  "numero_etudiant": "ETU001",          # String unique (5-20 caractères)
  "filiere": "Informatique",            # String (1-100 caractères)
  "moyenne": 16.5,                      # Float (0-20)
  "date_inscription": "2024-01-15T...", # Automatique
  "date_modification": "2024-01-15T..." # Automatique
}
```

## ⚠️ Codes d'Erreur

| Code | Signification | Exemple |
|------|---------------|---------|
| 200 | OK - Requête réussie | GET, PUT réussis |
| 201 | Created - Création réussie | POST réussi |
| 400 | Bad Request - Données invalides | Email ou numéro en doublon |
| 404 | Not Found - Ressource inexistante | Étudiant n'existe pas |
| 422 | Unprocessable Entity - Validation échouée | Format email invalide |
| 500 | Server Error - Erreur serveur | Problème interne |

## 🎯 Cas d'Usage Courants

### Cas 1: Ajouter 3 étudiants et les lister
```python
etudiants_data = [
    {"nom": "Dupont", "prenom": "Jean", "email": "jean.dupont@example.com", ...},
    {"nom": "Martin", "prenom": "Sophie", "email": "sophie.martin@example.com", ...},
    {"nom": "Bernard", "prenom": "Paul", "email": "paul.bernard@example.com", ...}
]

for data in etudiants_data:
    requests.post(f"{BASE_URL}/etudiants/", json=data)

etudiants = requests.get(f"{BASE_URL}/etudiants/").json()
```

### Cas 2: Obtenir la moyenne d'une filière
```python
response = requests.get(f"{BASE_URL}/etudiants/?filiere=Informatique")
etudiants = response.json()
moyenne = sum(e['moyenne'] for e in etudiants) / len(etudiants)
print(f"Moyenne en Informatique: {moyenne}")
```

### Cas 3: Trouver le meilleur étudiant
```python
response = requests.get(f"{BASE_URL}/etudiants/stats/resume")
stats = response.json()
meilleur = stats['meilleur_etudiant']
print(f"{meilleur['nom']} ({meilleur['moyenne']})")
```

## 📝 Notes Importantes

1. **Base de données**: SQLite stockée dans `etudiants.db`
2. **Validation**: Pydantic valide automatiquement les données
3. **Email**: Doit être unique et valide
4. **Numéro étudiant**: Doit être unique
5. **Moyenne**: Entre 0 et 20
6. **CORS**: Activé pour tous les domaines

## 🐛 Dépannage

### Erreur: "Connection refused"
→ Vérifiez que le serveur est lancé: `uvicorn main:app --reload`

### Erreur: "Email exists"
→ L'email est déjà utilisé par un autre étudiant

### Erreur: "Student not found"
→ L'ID n'existe pas

### Port 8000 déjà utilisé
→ Lancez sur un autre port: `uvicorn main:app --port 8001 --reload`

## 📚 Ressources Supplémentaires

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

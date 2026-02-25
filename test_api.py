"""
Script de test pour tester l'API
À exécuter après avoir lancé le serveur
"""

import requests
from datetime import date

# URL de base de l'API
BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("=" * 60)
    print("TEST DE L'API - GESTION DES ÉTUDIANTS")
    print("=" * 60)
    
    # 1. Vérifier que l'API est en ligne
    print("\n1. Vérification de la santé de l'API...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    
    # 2. Obtenir les informations racine
    print("\n2. Informations de l'API...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    
    # 3. Créer un étudiant
    print("\n3. Création d'un étudiant...")
    etudiant1 = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com",
        "date_naissance": "2003-05-15",
        "numero_etudiant": "ETU001",
        "filiere": "Informatique",
        "moyenne": 16.5
    }
    response = requests.post(f"{BASE_URL}/etudiants/", json=etudiant1)
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    etudiant1_id = response.json()["id"]
    
    # 4. Créer un deuxième étudiant
    print("\n4. Création d'un deuxième étudiant...")
    etudiant2 = {
        "nom": "Martin",
        "prenom": "Sophie",
        "email": "sophie.martin@example.com",
        "date_naissance": "2002-08-22",
        "numero_etudiant": "ETU002",
        "filiere": "Informatique",
        "moyenne": 14.2
    }
    response = requests.post(f"{BASE_URL}/etudiants/", json=etudiant2)
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    etudiant2_id = response.json()["id"]
    
    # 5. Créer un troisième étudiant dans une autre filière
    print("\n5. Création d'un troisième étudiant...")
    etudiant3 = {
        "nom": "Bernard",
        "prenom": "Paul",
        "email": "paul.bernard@example.com",
        "date_naissance": "2001-12-10",
        "numero_etudiant": "ETU003",
        "filiere": "Mathématiques",
        "moyenne": 18.0
    }
    response = requests.post(f"{BASE_URL}/etudiants/", json=etudiant3)
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    
    # 6. Lister tous les étudiants
    print("\n6. Lister tous les étudiants...")
    response = requests.get(f"{BASE_URL}/etudiants/")
    print(f"Status: {response.status_code}")
    print(f"Nombre d'étudiants: {len(response.json())}")
    for etudiant in response.json():
        print(f"  - {etudiant['prenom']} {etudiant['nom']} ({etudiant['filiere']})")
    
    # 7. Obtenir un étudiant spécifique
    print(f"\n7. Obtenir l'étudiant avec l'ID {etudiant1_id}...")
    response = requests.get(f"{BASE_URL}/etudiants/{etudiant1_id}")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    
    # 8. Mettre à jour un étudiant
    print(f"\n8. Mise à jour de l'étudiant {etudiant1_id}...")
    etudiant_update = {
        "moyenne": 17.5,
        "filiere": "Informatique - Spécialité IA"
    }
    response = requests.put(f"{BASE_URL}/etudiants/{etudiant1_id}", json=etudiant_update)
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    
    # 9. Filtrer par filière
    print("\n9. Lister les étudiants en Informatique...")
    response = requests.get(f"{BASE_URL}/etudiants/?filiere=Informatique")
    print(f"Status: {response.status_code}")
    print(f"Nombre d'étudiants en Informatique: {len(response.json())}")
    for etudiant in response.json():
        print(f"  - {etudiant['prenom']} {etudiant['nom']} (Moyenne: {etudiant['moyenne']})")
    
    # 10. Rechercher par nom
    print("\n10. Recherche par nom (Martin)...")
    response = requests.get(f"{BASE_URL}/etudiants/search/par-nom?query=Martin")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        for etudiant in response.json():
            print(f"  - {etudiant['prenom']} {etudiant['nom']}")
    
    # 11. Obtenir les statistiques
    print("\n11. Statistiques sur les étudiants...")
    response = requests.get(f"{BASE_URL}/etudiants/stats/resume")
    print(f"Status: {response.status_code}")
    stats = response.json()
    print(f"  - Total d'étudiants: {stats['total_etudiants']}")
    print(f"  - Moyenne globale: {stats['moyenne_globale']}")
    print(f"  - Meilleur étudiant: {stats['meilleur_etudiant']}")
    print(f"  - Étudiants par filière: {stats['etudiants_par_filiere']}")
    
    # 12. Pagination
    print("\n12. Pagination (skip=0, limit=2)...")
    response = requests.get(f"{BASE_URL}/etudiants/?skip=0&limit=2")
    print(f"Status: {response.status_code}")
    print(f"Nombre d'étudiants retournés: {len(response.json())}")
    
    # 13. Supprimer un étudiant
    print(f"\n13. Suppression de l'étudiant {etudiant2_id}...")
    response = requests.delete(f"{BASE_URL}/etudiants/{etudiant2_id}")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {response.json()}")
    
    # 14. Vérifier la suppression
    print("\n14. Vérification - lister tous les étudiants restants...")
    response = requests.get(f"{BASE_URL}/etudiants/")
    print(f"Status: {response.status_code}")
    print(f"Nombre d'étudiants: {len(response.json())}")
    for etudiant in response.json():
        print(f"  - {etudiant['prenom']} {etudiant['nom']}")
    
    # 15. Tester les erreurs
    print("\n15. Test d'erreur - Étudiant inexistant...")
    response = requests.get(f"{BASE_URL}/etudiants/99999")
    print(f"Status: {response.status_code}")
    if response.status_code == 404:
        print(f"Erreur attendue: {response.json()['detail']}")
    
    print("\n" + "=" * 60)
    print("TESTS TERMINÉS !")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ ERREUR: Impossible de se connecter à l'API.")
        print("Assurez-vous que le serveur FastAPI est lancé avec:")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERREUR: {e}")

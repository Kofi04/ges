"""
Tests de l'API Gestion des Étudiants.
Les tests appellent l'API sur BASE_URL. Lance le serveur avant : uvicorn main:app --reload
"""

import os
import pytest
import requests
import uuid

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


def _api_reachable():
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


@pytest.fixture(scope="module")
def skip_if_server_down():
    if not _api_reachable():
        pytest.skip(
            "API non joignable. Lance le serveur : uvicorn main:app --reload",
            allow_module_level=True,
        )


def test_health(skip_if_server_down):
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_info(skip_if_server_down):
    response = requests.get(f"{BASE_URL}/api")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data and "version" in data


def test_root_serves_ui(skip_if_server_down):
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")


def test_etudiants_crud(skip_if_server_down):
    suffix = uuid.uuid4().hex[:8]
    etudiant = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": f"jean.dupont.{suffix}@example.com",
        "date_naissance": "2003-05-15",
        "numero_etudiant": f"ETU{suffix}",
        "filiere": "Informatique",
        "moyenne": 16.5,
    }
    r = requests.post(f"{BASE_URL}/etudiants/", json=etudiant)
    assert r.status_code == 201
    id1 = r.json()["id"]

    r = requests.get(f"{BASE_URL}/etudiants/")
    assert r.status_code == 200
    assert len(r.json()) >= 1

    r = requests.get(f"{BASE_URL}/etudiants/{id1}")
    assert r.status_code == 200
    assert r.json()["nom"] == "Dupont"

    r = requests.put(f"{BASE_URL}/etudiants/{id1}", json={"moyenne": 18.0})
    assert r.status_code == 200
    assert r.json()["moyenne"] == 18.0

    r = requests.get(f"{BASE_URL}/etudiants/stats/resume")
    assert r.status_code == 200
    assert "total_etudiants" in r.json()

    r = requests.delete(f"{BASE_URL}/etudiants/{id1}")
    assert r.status_code == 200


def test_etudiant_404(skip_if_server_down):
    response = requests.get(f"{BASE_URL}/etudiants/99999")
    assert response.status_code == 404

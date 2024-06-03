import os
import sys
import pytest
from fastapi.testclient import TestClient

# Adicionando o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_create_grafo():
    response = client.post("/grafos/", json={
        "nome": "Test Grafo",
        "nos": [
            {"nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["nome"] == "Test Grafo"

def test_get_grafo():
    response = client.post("/grafos/", json={
        "nome": "Test Grafo",
        "nos": [
            {"nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    })
    assert response.status_code == 200
    grafo_id = response.json()["id"]

    response = client.get(f"/grafos/{grafo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == grafo_id
    assert data["nome"] == "Test Grafo"

def test_get_all_routes():
    response = client.post("/grafos/", json={
        "nome": "Test Grafo",
        "nos": [
            {"nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    })
    assert response.status_code == 200
    grafo_id = response.json()["id"]
    no_1_id = response.json()["nos"][0]["id"]
    no_2_id = response.json()["nos"][1]["id"]

    response = client.get(f"/grafos/{grafo_id}/routes?start_node_id={no_1_id}&end_node_id={no_2_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_shortest_route():
    response = client.post("/grafos/", json={
        "nome": "Test Grafo",
        "nos": [
            {"nome": "No 1", "coordenada": [-73.935242, 40.73061]},
            {"nome": "No 2", "coordenada": [-73.975242, 40.75061]}
        ],
        "arestas": [
            {"no_origem_id": "No 1", "no_destino_id": "No 2", "linha": [
                [-73.935242, 40.73061],
                [-73.975242, 40.75061]
            ]}
        ]
    })
    assert response.status_code == 200
    grafo_id = response.json()["id"]
    no_1_id = response.json()["nos"][0]["id"]
    no_2_id = response.json()["nos"][1]["id"]

    response = client.get(f"/grafos/{grafo_id}/shortest_route?start_node_id={no_1_id}&end_node_id={no_2_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

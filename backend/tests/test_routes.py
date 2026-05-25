"""
[DOC-T02] tests/test_routes.py
--------------------------------
Testes de integração para os endpoints FastAPI.

Cobre:
- POST /api/otimizar com payload válido
- POST /api/otimizar com payload inválido (422)
- POST /api/otimizar com estoque zerado (400)
- GET /health retornando status ok
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Endpoint /health deve retornar status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_otimizar_payload_valido():
    """POST /api/otimizar com dados padrão deve retornar 200 e solução ótima."""
    payload = {"massa": 10.0, "queijo": 5.0, "molho": 4.0, "calabresa": 2.0}
    response = client.post("/api/otimizar", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "mucarela" in data
    assert "calabresa" in data
    assert "lucro" in data
    assert "consumo" in data
    assert data["lucro"] > 0


def test_otimizar_payload_invalido():
    """Payload com valor negativo deve retornar 422 (Unprocessable Entity)."""
    payload = {"massa": -1.0, "queijo": 5.0, "molho": 4.0, "calabresa": 2.0}
    response = client.post("/api/otimizar", json=payload)
    assert response.status_code == 422


def test_otimizar_estoque_zerado():
    """Estoque zerado deve retornar 400 com mensagem de erro."""
    payload = {"massa": 0.0, "queijo": 0.0, "molho": 0.0, "calabresa": 0.0}
    response = client.post("/api/otimizar", json=payload)
    assert response.status_code == 400


def test_otimizar_sem_payload():
    """Sem payload deve usar valores padrão e retornar 200."""
    response = client.post("/api/otimizar", json={})
    assert response.status_code == 200

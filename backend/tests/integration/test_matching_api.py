# backend/tests/integration/test_matching_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_run_matching_unauthorized():
    response = client.post("/api/v1/matching/run")
    assert response.status_code == 401

def test_run_matching_authorized(authenticated_client):
    response = authenticated_client.post("/api/v1/matching/run")
    assert response.status_code == 202
    assert 'task_id' in response.json()

async def test_match_endpoint(authenticated_client):
    response = await authenticated_client.get("/api/v1/properties/matches/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

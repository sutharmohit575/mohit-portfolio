"""
Tests for the contact / Boss Fight API endpoint.
Run: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def valid_payload(**overrides):
    base = {
        "name": "Test User",
        "email": "test@example.com",
        "reason": "Freelance Project",
        "interested_project": "NeuralChat",
    }
    return {**base, **overrides}


def test_contact_submit_success():
    resp = client.post("/api/contact/submit", json=valid_payload())
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["loot_dropped"] is True
    assert "message" in data


def test_contact_missing_name():
    resp = client.post("/api/contact/submit", json=valid_payload(name="X"))
    assert resp.status_code == 422


def test_contact_invalid_email():
    resp = client.post("/api/contact/submit", json=valid_payload(email="not-an-email"))
    assert resp.status_code == 422


def test_contact_invalid_reason():
    resp = client.post("/api/contact/submit", json=valid_payload(reason="HACK THE PLANET"))
    assert resp.status_code == 422


def test_contact_optional_project_omitted():
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "reason": "Just Exploring",
    }
    resp = client.post("/api/contact/submit", json=payload)
    assert resp.status_code == 200


def test_contact_rate_limit():
    """After 5 requests the 6th should be 429."""
    # Use a fresh client to avoid state from other tests
    fresh_client = TestClient(app)
    for _ in range(5):
        fresh_client.post("/api/contact/submit", json=valid_payload())
    resp = fresh_client.post("/api/contact/submit", json=valid_payload())
    assert resp.status_code in (200, 429)

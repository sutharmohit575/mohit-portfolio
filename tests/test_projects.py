"""
Tests for the projects API endpoints.
Run: pytest tests/ -v
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_projects():
    resp = client.get("/api/projects/")
    assert resp.status_code == 200
    data = resp.json()
    assert "projects" in data
    assert len(data["projects"]) == 4  # neuralchat, pixelmart, cryptovault, autoscribe


def test_get_project_neuralchat():
    resp = client.get("/api/projects/neuralchat")
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "neuralchat"
    assert "React" in data["tags"]


def test_get_project_autoscribe():
    resp = client.get("/api/projects/autoscribe")
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "autoscribe"
    assert "Python" in data["tags"]


def test_get_project_not_found():
    resp = client.get("/api/projects/doesnotexist")
    assert resp.status_code == 404


def test_project_has_required_fields():
    resp = client.get("/api/projects/jobai")
    assert resp.status_code == 200
    data = resp.json()
    for field in ("slug", "name", "description", "tags", "biome", "status"):
        assert field in data, f"Missing field: {field}"


def test_all_project_slugs_present():
    resp = client.get("/api/projects/")
    slugs = {p["slug"] for p in resp.json()["projects"]}
    assert slugs == {"neuralchat", "pixelmart", "jobai", "autoscribe"}

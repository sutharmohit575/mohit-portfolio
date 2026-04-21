"""
Tests for the achievements API endpoints.
Run: pytest tests/ -v
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_achievements():
    resp = client.get("/api/achievements/")
    assert resp.status_code == 200
    data = resp.json()
    assert "achievements" in data
    assert len(data["achievements"]) == 10


def test_all_achievement_ids_present():
    resp = client.get("/api/achievements/")
    ids = set(resp.json()["achievements"].keys())
    expected = {"curious", "hacker", "explorer", "gamer", "hunter",
                "boss", "matrix", "konami", "neofetch", "shutdown"}
    assert ids == expected


def test_unlock_valid_achievement():
    resp = client.post("/api/achievements/unlock", json={
        "achievement_id": "hacker",
        "session_id": "test-session-abc123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["achievement_id"] == "hacker"
    assert data["xp_reward"] == 1
    assert data["emoji"] == "💻"
    assert data["label"] == "Elite Hacker"


def test_unlock_boss_slayer():
    resp = client.post("/api/achievements/unlock", json={
        "achievement_id": "boss",
        "session_id": "test-session-xyz",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["xp_reward"] == 5
    assert data["emoji"] == "⚔"


def test_unlock_all_achievements():
    """Every achievement ID should unlock successfully."""
    ids = ["curious", "hacker", "explorer", "gamer", "hunter",
           "boss", "matrix", "konami", "neofetch", "shutdown"]
    for aid in ids:
        resp = client.post("/api/achievements/unlock", json={
            "achievement_id": aid,
            "session_id": "test-session",
        })
        assert resp.status_code == 200, f"Failed for: {aid}"


def test_unlock_invalid_achievement():
    resp = client.post("/api/achievements/unlock", json={
        "achievement_id": "invalid_achievement",
        "session_id": "test-session",
    })
    assert resp.status_code == 422

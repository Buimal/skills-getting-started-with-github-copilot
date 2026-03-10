import pytest
from fastapi.testclient import TestClient

# the conftest fixture will have already added src/ to sys.path
from app import app, activities  # noqa: E402

client = TestClient(app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove(client):
    activity = "Chess Club"
    email = "tester@example.com"

    # signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # verify added
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]

    # remove it
    resp3 = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )
    assert resp3.status_code == 200
    assert f"Removed {email}" in resp3.json()["message"]

    # verify gone
    resp4 = client.get("/activities")
    assert email not in resp4.json()[activity]["participants"]


def test_signup_duplicate(client):
    activity = "Programming Class"
    existing = "emma@mergington.edu"
    resp = client.post(
        f"/activities/{activity}/signup", params={"email": existing}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student is already signed up for this activity"


def test_remove_nonexistent(client):
    activity = "Gym Class"
    email = "not@here"
    resp = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not registered"

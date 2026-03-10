import pytest
from fastapi.testclient import TestClient

# the conftest fixture will have already added src/ to sys.path
from app import app, activities  # noqa: E402

client = TestClient(app)


def test_get_activities(client):
    # Arrange: nothing special, just the client fixture

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"

    # Act: sign up the user
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert signup succeeded
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Act: fetch activities to verify addition
    resp2 = client.get("/activities")

    # Assert participant present
    assert email in resp2.json()[activity]["participants"]

    # Act: remove the participant
    resp3 = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )

    # Assert removal succeeded
    assert resp3.status_code == 200
    assert f"Removed {email}" in resp3.json()["message"]

    # Act: fetch again
    resp4 = client.get("/activities")

    # Assert participant is gone
    assert email not in resp4.json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Programming Class"
    existing = "emma@mergington.edu"

    # Act
    resp = client.post(
        f"/activities/{activity}/signup", params={"email": existing}
    )

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student is already signed up for this activity"


def test_remove_nonexistent(client):
    # Arrange
    activity = "Gym Class"
    email = "not@here"

    # Act
    resp = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not registered"

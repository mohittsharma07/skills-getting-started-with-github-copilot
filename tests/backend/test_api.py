import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activity_state():
    activity = app_module.activities["Chess Club"]
    activity["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    yield
    activity["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


@pytest.fixture()
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_get_activities_returns_activity_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_updates_activity_participants(client):
    response = client.post("/activities/Chess Club/signup?email=test@example.com")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@example.com for Chess Club"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "test@example.com" in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_removes_email_from_activity(client):
    client.post("/activities/Chess Club/signup?email=test@example.com")

    response = client.delete("/activities/Chess Club/participants/test@example.com")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed test@example.com from Chess Club"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "test@example.com" not in activities_response.json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_registration(client):
    client.post("/activities/Chess Club/signup?email=test@example.com")

    response = client.post("/activities/Chess Club/signup?email=test@example.com")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

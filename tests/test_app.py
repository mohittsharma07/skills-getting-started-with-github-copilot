import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activity_state():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    yield
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


client = TestClient(app_module.app)


def test_signup_updates_activity_participants_immediately():
    response = client.post(
        "/activities/Chess Club/signup?email=test@example.com"
    )

    assert response.status_code == 200
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "test@example.com" in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_removes_email_from_activity():
    client.post("/activities/Chess Club/signup?email=test@example.com")

    response = client.delete("/activities/Chess Club/participants/test@example.com")

    assert response.status_code == 200
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "test@example.com" not in activities_response.json()["Chess Club"]["participants"]

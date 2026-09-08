from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_duplicate_signup_rejected():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]
    email = "duplicate.student@mergington.edu"

    try:
        first_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert first_response.status_code == 200

        second_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        assert second_response.status_code == 400
        assert "already signed up" in second_response.json()["detail"].lower()
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]
    email = "michael@mergington.edu"

    try:
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants

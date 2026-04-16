from urllib.parse import quote


def test_get_activities(client):
    # Arrange
    expected_activity_names = sorted(client.get("/activities").json().keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert sorted(data.keys()) == expected_activity_names
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_success(client):
    # Arrange
    activity = "Soccer Team"
    email = "newstudent@mergington.edu"
    encoded_activity = quote(activity, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={encoded_email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate_participant_error(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={encoded_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    participant = "daniel@mergington.edu"
    encoded_activity = quote(activity, safe="")
    encoded_participant = quote(participant, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participant?email={encoded_participant}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {participant} from {activity}"
    assert participant not in client.get("/activities").json()[activity]["participants"]


def test_remove_participant_not_found_error(client):
    # Arrange
    activity = "Soccer Team"
    participant = "missing@mergington.edu"
    encoded_activity = quote(activity, safe="")
    encoded_participant = quote(participant, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participant?email={encoded_participant}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

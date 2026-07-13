from src.app import activities


def test_signup_successfully_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    before_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == before_count + 1


def test_signup_returns_404_when_activity_missing(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_same_email_can_join_multiple_activities(client):
    # Arrange
    email = "multi.activity@mergington.edu"
    first_activity = "Chess Club"
    second_activity = "Basketball Team"

    # Act
    first_response = client.post(f"/activities/{first_activity}/signup", params={"email": email})
    second_response = client.post(f"/activities/{second_activity}/signup", params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert email in activities[first_activity]["participants"]
    assert email in activities[second_activity]["participants"]

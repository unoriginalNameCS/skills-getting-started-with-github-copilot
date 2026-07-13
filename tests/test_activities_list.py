def test_get_activities_returns_all_activities(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_get_activities_has_expected_schema(client):
    # Arrange
    endpoint = "/activities"
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    payload = response.json()

    for activity_name, details in payload.items():
        assert expected_keys.issubset(details.keys()), f"Missing keys for {activity_name}"
        assert isinstance(details["description"], str)
        assert isinstance(details["schedule"], str)
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange: (No setup needed, uses in-memory DB)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

# Test POST /activities/{activity_name}/signup

def test_signup_for_activity():
    # Arrange
    activity = "Basketball"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up: Remove test user
    client.delete(f"/activities/{activity}/unregister?email={email}")

# Test duplicate signup error

def test_signup_duplicate():
    # Arrange
    activity = "Basketball"
    email = "alex@mergington.edu"  # Already registered
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Test DELETE /activities/{activity_name}/unregister

def test_unregister_from_activity():
    # Arrange
    activity = "Tennis Club"
    email = "unregtest@mergington.edu"
    # Register first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

# Test unregister non-existent participant

def test_unregister_nonexistent():
    # Arrange
    activity = "Tennis Club"
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

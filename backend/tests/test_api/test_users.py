from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    """Test creating a new user."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_duplicate_user(client: TestClient) -> None:
    """Test that creating a duplicate user fails."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword123",
    }

    # Create first user
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201

    # Try to create duplicate
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_user(client: TestClient) -> None:
    """Test getting a user by ID."""
    # Create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "getuser@example.com",
            "password": "testpassword123",
        },
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "getuser@example.com"


def test_get_nonexistent_user(client: TestClient) -> None:
    """Test that getting a nonexistent user returns 404."""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404


def test_list_users(client: TestClient) -> None:
    """Test listing users."""
    # Create multiple users
    for i in range(3):
        client.post(
            "/api/v1/users/",
            json={
                "email": f"user{i}@example.com",
                "password": "testpassword123",
            },
        )

    # List users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_update_user(client: TestClient) -> None:
    """Test updating a user."""
    # Create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "update@example.com",
            "password": "testpassword123",
            "full_name": "Original Name",
        },
    )
    user_id = create_response.json()["id"]

    # Update user
    response = client.put(
        f"/api/v1/users/{user_id}",
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["email"] == "update@example.com"


def test_delete_user(client: TestClient) -> None:
    """Test deleting a user."""
    # Create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "delete@example.com",
            "password": "testpassword123",
        },
    )
    user_id = create_response.json()["id"]

    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

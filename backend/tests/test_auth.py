def login(client):
    return client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )


def test_login_success(client, active_user):
    response = login(client)
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_failures(client, active_user):
    missing = client.post(
        "/api/auth/login",
        json={"username": "missing", "password": "admin123"},
    )
    wrong = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert missing.status_code == 401
    assert wrong.status_code == 401


def test_me_success(client, active_user):
    token = login(client).json()["access_token"]
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "admin"


def test_me_rejects_missing_or_invalid_token(client):
    assert client.get("/api/auth/me").status_code == 401
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401

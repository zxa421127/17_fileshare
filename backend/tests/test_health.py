def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "service": "PM Knowledge Portal",
        "version": "1.1",
    }


def test_auth_status(client):
    response = client.get("/api/auth/status")
    assert response.status_code == 200
    data = response.json()
    assert data["auth"] == "ready"
    assert "password" in data["methods"]

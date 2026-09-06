from fastapi.testclient import TestClient


def test_create_user(client):

    r = client.post(
        "/api/users",
        json={
            "username":"teacher01",
            "password":"123456",
            "email":"teacher@test.com"
        }
    )

    assert r.status_code == 200


def test_list_users(client):

    r = client.get(
        "/api/users"
    )

    assert r.status_code == 200

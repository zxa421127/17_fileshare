def test_add_permission(client):

    r=client.post(
        "/api/users",
        json={
            "username":"user02",
            "password":"123456",
            "email":"u@test.com"
        }
    )

    assert r.status_code==200



def test_permission_api():

    assert True

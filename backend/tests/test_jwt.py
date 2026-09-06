from app.auth.jwt import create_token, decode_token


def test_create_and_decode_token():
    token = create_token(123)
    payload = decode_token(token)

    assert isinstance(token, str)
    assert payload["sub"] == "123"
    assert "exp" in payload


def test_invalid_token_rejected():
    try:
        decode_token("not-a-valid-token")
        assert False, "decode_token should reject invalid tokens"
    except ValueError:
        assert True

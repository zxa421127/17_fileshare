import pytest

from app.auth.jwt import create_token, decode_token


def test_create_and_decode_token():
    token = create_token(123)
    payload = decode_token(token)

    assert isinstance(token, str)
    assert payload["sub"] == "123"
    assert "exp" in payload


def test_invalid_token_rejected():
    with pytest.raises(ValueError):
        decode_token("not-a-valid-token")


def test_expired_token_rejected():
    token = create_token(123, expires_minutes=-1)
    with pytest.raises(ValueError):
        decode_token(token)

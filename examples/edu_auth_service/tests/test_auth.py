import time
import pytest

from app.config import Settings
from app.auth.token import TokenService, TokenError, create_access_token, create_refresh_token, verify_jwt, refresh_token
from app.auth.password import hash_password, verify_password
from app.middleware.auth_required import auth_required


def test_access_token_contains_subject():
    settings = Settings(jwt_secret="x", access_minutes=15, refresh_days=7, password_salt="s", login_rate_limit_per_minute=5)
    token = create_access_token("user_1", settings)
    assert token["sub"] == "user_1"
    assert token["type"] == "access"


def test_invalid_token_without_subject_is_rejected():
    with pytest.raises(ValueError):
        verify_jwt({"exp": int(time.time()) + 60})


def test_expired_access_token_is_rejected():
    token = {
        "sub": "user_1",
        "type": "access",
        "iat": int(time.time()) - 100,
        "exp": int(time.time()) - 1,
    }
    with pytest.raises(ValueError):
        verify_jwt(token)


def test_refresh_token_issues_new_access_token():
    settings = Settings(jwt_secret="x", access_minutes=15, refresh_days=7, password_salt="s", login_rate_limit_per_minute=5)
    refresh_payload = create_refresh_token("user_1", settings)
    access = refresh_token(refresh_payload, settings)
    assert access["type"] == "access"
    assert access["sub"] == "user_1"


def test_password_hash_and_verify():
    password_hash = hash_password("secret")
    assert verify_password("secret", password_hash)
    assert not verify_password("wrong", password_hash)


def test_auth_required_accepts_access_token():
    request = {
        "token": {
            "sub": "user_1",
            "type": "access",
            "iat": int(time.time()),
            "exp": int(time.time()) + 60,
        }
    }
    out = auth_required(request)
    assert out["user_id"] == "user_1"

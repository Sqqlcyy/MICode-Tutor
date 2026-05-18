from app.config import Settings


def test_settings_from_env_has_defaults(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    settings = Settings.from_env()
    assert settings.jwt_secret == "dev-secret"
    assert settings.access_minutes == 15
    assert settings.refresh_days == 7


def test_settings_token_config():
    settings = Settings(jwt_secret="x", access_minutes=10, refresh_days=3, password_salt="s", login_rate_limit_per_minute=5)
    cfg = settings.token_config()
    assert cfg["jwt_secret"] == "x"
    assert cfg["access_minutes"] == 10
    assert cfg["refresh_days"] == 3

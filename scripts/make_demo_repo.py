from pathlib import Path
import textwrap

ROOT = Path("examples/edu_auth_service")


def write(path: str, content: str):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def many_helpers(prefix: str, n: int = 60):
    blocks = []
    for i in range(n):
        blocks.append(f'''
def {prefix}_helper_{i}(value: str) -> str:
    """Normalize and validate {prefix} helper case {i}."""
    if value is None:
        raise ValueError("{prefix} value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("{prefix} value cannot be empty")
    return f"{prefix}:{i}:{{value}}"
''')
    return "\n".join(blocks)


def main():
    write("README.md", """
# Edu Auth Service

A realistic educational authentication service used by MICode Tutor.

This repo demonstrates:

- JWT-like access token creation and verification
- refresh token flow
- password hashing
- authentication middleware
- rate limiting
- session store
- configuration loading
- test generation targets
- safe second-development tasks

Demo questions:

1. Where is JWT authentication verified?
2. Explain this repo to a beginner and give a learning path.
3. Write tests for expired refresh tokens.
4. Plan how to add rate limiting to login.
5. Where is configuration loaded?
""")

    write("app/__init__.py", "")
    write("app/auth/__init__.py", "")
    write("app/middleware/__init__.py", "")
    write("app/db/__init__.py", "")
    write("app/security/__init__.py", "")
    write("tests/__init__.py", "")

    write("app/config.py", """
import os
from dataclasses import dataclass


@dataclass
class Settings:
    \"\"\"Application settings loaded from environment variables.\"\"\"

    jwt_secret: str
    access_minutes: int
    refresh_days: int
    password_salt: str
    login_rate_limit_per_minute: int

    @classmethod
    def from_env(cls) -> "Settings":
        \"\"\"Load settings from environment variables.\"\"\"
        return cls(
            jwt_secret=os.getenv("JWT_SECRET", "dev-secret"),
            access_minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", "15")),
            refresh_days=int(os.getenv("REFRESH_TOKEN_DAYS", "7")),
            password_salt=os.getenv("PASSWORD_SALT", "dev-salt"),
            login_rate_limit_per_minute=int(os.getenv("LOGIN_RATE_LIMIT_PER_MINUTE", "5")),
        )

    def token_config(self) -> dict:
        \"\"\"Return token-related configuration.\"\"\"
        return {
            "jwt_secret": self.jwt_secret,
            "access_minutes": self.access_minutes,
            "refresh_days": self.refresh_days,
        }

    def security_config(self) -> dict:
        \"\"\"Return security-related configuration.\"\"\"
        return {
            "password_salt": self.password_salt,
            "login_rate_limit_per_minute": self.login_rate_limit_per_minute,
        }
""")

    write("app/auth/token.py", f"""
import time
import base64
import json
from app.config import Settings


class TokenError(ValueError):
    \"\"\"Raised when token validation fails.\"\"\"


class TokenService:
    \"\"\"Create, verify, and refresh JWT-like tokens for the demo service.\"\"\"

    def __init__(self, settings: Settings):
        self.settings = settings

    def create_access_token(self, user_id: str) -> dict:
        \"\"\"Create a short-lived access token payload.\"\"\"
        now = int(time.time())
        return {{
            "sub": user_id,
            "type": "access",
            "iat": now,
            "exp": now + self.settings.access_minutes * 60,
        }}

    def create_refresh_token(self, user_id: str) -> dict:
        \"\"\"Create a long-lived refresh token payload.\"\"\"
        now = int(time.time())
        return {{
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + self.settings.refresh_days * 24 * 3600,
        }}

    def verify_jwt(self, token_payload: dict) -> dict:
        \"\"\"Validate a JWT-like token payload and return decoded claims.

        This is the central authentication verification point.
        It checks token presence, subject, expiration, and token type.
        \"\"\"
        if not token_payload:
            raise TokenError("Missing token")
        if "sub" not in token_payload:
            raise TokenError("Missing subject")
        if "exp" not in token_payload:
            raise TokenError("Missing expiration")

        now = int(time.time())
        if token_payload["exp"] < now:
            raise TokenError("Token expired")

        return token_payload

    def refresh_token(self, refresh_payload: dict) -> dict:
        \"\"\"Validate a refresh token and issue a new access token.\"\"\"
        claims = self.verify_jwt(refresh_payload)
        if claims.get("type") != "refresh":
            raise TokenError("Not a refresh token")
        return self.create_access_token(claims["sub"])

    def encode_payload(self, payload: dict) -> str:
        \"\"\"Encode a token payload for transport in this demo service.\"\"\"
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii")

    def decode_payload(self, token: str) -> dict:
        \"\"\"Decode a token string into a dictionary payload.\"\"\"
        try:
            raw = base64.urlsafe_b64decode(token.encode("ascii"))
            return json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise TokenError("Invalid token encoding") from exc


def create_access_token(user_id: str, settings: Settings) -> dict:
    \"\"\"Create a short-lived access token payload.\"\"\"
    return TokenService(settings).create_access_token(user_id)


def create_refresh_token(user_id: str, settings: Settings) -> dict:
    \"\"\"Create a long-lived refresh token payload.\"\"\"
    return TokenService(settings).create_refresh_token(user_id)


def verify_jwt(token_payload: dict) -> dict:
    \"\"\"Validate a JWT-like token payload using demo default settings.\"\"\"
    settings = Settings.from_env()
    return TokenService(settings).verify_jwt(token_payload)


def refresh_token(refresh_payload: dict, settings: Settings) -> dict:
    \"\"\"Validate a refresh token and issue a new access token.\"\"\"
    return TokenService(settings).refresh_token(refresh_payload)


{many_helpers("token", 80)}
""")

    write("app/auth/password.py", f"""
import hashlib
import hmac
from app.config import Settings


class PasswordService:
    \"\"\"Hash and verify passwords with a configurable salt.\"\"\"

    def __init__(self, settings: Settings):
        self.settings = settings

    def hash_password(self, password: str) -> str:
        \"\"\"Hash a password for storage.\"\"\"
        if not password:
            raise ValueError("Password cannot be empty")
        raw = f"{{self.settings.password_salt}}:{{password}}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def verify_password(self, password: str, password_hash: str) -> bool:
        \"\"\"Verify a password against a stored hash.\"\"\"
        candidate = self.hash_password(password)
        return hmac.compare_digest(candidate, password_hash)


def hash_password(password: str) -> str:
    \"\"\"Hash a password using default settings.\"\"\"
    return PasswordService(Settings.from_env()).hash_password(password)


def verify_password(password: str, password_hash: str) -> bool:
    \"\"\"Verify a password against a stored hash using default settings.\"\"\"
    return PasswordService(Settings.from_env()).verify_password(password, password_hash)


{many_helpers("password", 50)}
""")

    write("app/auth/routes.py", f"""
from app.config import Settings
from app.auth.password import verify_password
from app.auth.token import TokenService
from app.security.rate_limit import RateLimiter


class AuthRoutes:
    \"\"\"Route handlers for login and refresh flows.\"\"\"

    def __init__(self, settings: Settings, user_store: dict):
        self.settings = settings
        self.user_store = user_store
        self.tokens = TokenService(settings)
        self.rate_limiter = RateLimiter(limit_per_minute=settings.login_rate_limit_per_minute)

    def login(self, username: str, password: str, client_id: str = "default") -> dict:
        \"\"\"Login a user and return access and refresh tokens.\"\"\"
        self.rate_limiter.check(client_id)

        user = self.user_store.get(username)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user["password_hash"]):
            raise ValueError("Invalid credentials")

        return {{
            "access_token": self.tokens.create_access_token(user["id"]),
            "refresh_token": self.tokens.create_refresh_token(user["id"]),
        }}

    def refresh(self, refresh_payload: dict) -> dict:
        \"\"\"Refresh an access token using a refresh token.\"\"\"
        return {{
            "access_token": self.tokens.refresh_token(refresh_payload)
        }}


def login(username: str, password: str, user_store: dict, settings: Settings) -> dict:
    \"\"\"Functional login wrapper used by app/main.py.\"\"\"
    return AuthRoutes(settings, user_store).login(username, password)


def refresh(refresh_payload: dict, settings: Settings) -> dict:
    \"\"\"Functional refresh wrapper used by app/main.py.\"\"\"
    return AuthRoutes(settings, {{}}).refresh(refresh_payload)


{many_helpers("routes", 45)}
""")

    write("app/middleware/auth_required.py", f"""
from app.auth.token import TokenService
from app.config import Settings


class AuthMiddleware:
    \"\"\"Authentication middleware that protects incoming requests.\"\"\"

    def __init__(self, settings: Settings):
        self.tokens = TokenService(settings)

    def auth_required(self, request: dict) -> dict:
        \"\"\"Require a valid access token before allowing a request.

        This middleware calls TokenService.verify_jwt and then checks that
        the token type is access.
        \"\"\"
        token_payload = request.get("token")
        claims = self.tokens.verify_jwt(token_payload)

        if claims.get("type") != "access":
            raise ValueError("Access token required")

        request["user_id"] = claims["sub"]
        return request


def auth_required(request: dict) -> dict:
    \"\"\"Require a valid access token using default settings.\"\"\"
    return AuthMiddleware(Settings.from_env()).auth_required(request)


{many_helpers("middleware", 50)}
""")

    write("app/security/rate_limit.py", f"""
import time
from collections import defaultdict, deque


class RateLimitExceeded(ValueError):
    \"\"\"Raised when a client exceeds the allowed request rate.\"\"\"


class RateLimiter:
    \"\"\"Simple in-memory rate limiter for login attempts.\"\"\"

    def __init__(self, limit_per_minute: int):
        self.limit_per_minute = limit_per_minute
        self.events = defaultdict(deque)

    def check(self, client_id: str) -> None:
        \"\"\"Check whether a client is allowed to perform another login attempt.\"\"\"
        now = time.time()
        window_start = now - 60
        q = self.events[client_id]

        while q and q[0] < window_start:
            q.popleft()

        if len(q) >= self.limit_per_minute:
            raise RateLimitExceeded("Too many login attempts")

        q.append(now)

    def reset(self, client_id: str) -> None:
        \"\"\"Reset rate limit state for a client.\"\"\"
        self.events.pop(client_id, None)


{many_helpers("rate_limit", 50)}
""")

    write("app/db/users.py", f"""
from app.auth.password import hash_password


class UserRepository:
    \"\"\"In-memory user repository for demo authentication.\"\"\"

    def __init__(self):
        self.users = {{}}

    def create_user(self, username: str, password: str) -> dict:
        \"\"\"Create a user and store it in memory.\"\"\"
        user = {{
            "id": f"user_{{username}}",
            "username": username,
            "password_hash": hash_password(password),
        }}
        self.users[username] = user
        return user

    def get_user(self, username: str) -> dict | None:
        \"\"\"Return a user by username.\"\"\"
        return self.users.get(username)

    def as_store(self) -> dict:
        \"\"\"Return the raw user store dictionary.\"\"\"
        return self.users


def create_demo_user(username: str, password: str) -> dict:
    \"\"\"Create a demo user record.\"\"\"
    return {{
        "id": f"user_{{username}}",
        "username": username,
        "password_hash": hash_password(password),
    }}


def build_user_store() -> dict:
    \"\"\"Build an in-memory user store for the demo.\"\"\"
    user = create_demo_user("alice", "correct-horse-battery-staple")
    return {{
        "alice": user
    }}


{many_helpers("users", 50)}
""")

    write("app/main.py", """
from app.config import Settings
from app.auth.routes import login, refresh
from app.middleware.auth_required import auth_required
from app.db.users import build_user_store


def create_app():
    \"\"\"Create the application and register auth routes.\"\"\"
    settings = Settings.from_env()
    user_store = build_user_store()

    app = {
        "settings": settings,
        "user_store": user_store,
        "routes": {
            "/auth/login": lambda username, password: login(username, password, user_store, settings),
            "/auth/refresh": lambda payload: refresh(payload, settings),
        },
        "middleware": [auth_required],
    }
    return app


def health_check() -> dict:
    \"\"\"Return service health information.\"\"\"
    return {"status": "ok", "service": "edu_auth_service"}
""")

    write("tests/test_auth.py", """
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
""")

    write("tests/test_config.py", """
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
""")

    print(f"Generated demo repo at {ROOT.resolve()}")
    total_lines = 0
    for p in ROOT.rglob("*"):
        if p.is_file():
            total_lines += len(p.read_text(encoding="utf-8").splitlines())
    print(f"Total lines: {total_lines}")


if __name__ == "__main__":
    main()

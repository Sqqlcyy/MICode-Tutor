# MICode Context Pack

Task: Where is JWT verified?

## Repo
- Name: edu_auth_service
- Languages: md, python
- Files: 17
- Symbols: 380

## Relevant Results
1. **app/auth/token.py::TokenService**
   - Type: symbol
   - Location: `app/auth/token.py:11-74`
   - Score: 2.067
   - Summary: Create, verify, and refresh JWT-like tokens for the demo service.
2. **app/auth/token.py::TokenService.verify_jwt**
   - Type: symbol
   - Location: `app/auth/token.py:37-54`
   - Score: 2.067
   - Summary: Validate a JWT-like token payload and return decoded claims.
3. **app/auth/token.py::verify_jwt**
   - Type: symbol
   - Location: `app/auth/token.py:87-90`
   - Score: 2.067
   - Summary: Validate a JWT-like token payload using demo default settings.
4. **app/config.py::Settings**
   - Type: symbol
   - Location: `app/config.py:6-39`
   - Score: 1.000
   - Summary: Application settings loaded from environment variables.
5. **app/config.py::Settings.from_env**
   - Type: symbol
   - Location: `app/config.py:16-24`
   - Score: 1.000
   - Summary: Load settings from environment variables.

## Evidence Snippets
### app/auth/token.py::TokenService
Location: `app/auth/token.py:11-74`
```python
class TokenService:
    """Create, verify, and refresh JWT-like tokens for the demo service."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def create_access_token(self, user_id: str) -> dict:
        """Create a short-lived access token payload."""
        now = int(time.time())
        return {
            "sub": user_id,
            "type": "access",
            "iat": now,
            "exp": now + self.settings.access_minutes * 60,
        }

    def create_refresh_token(self, user_id: str) -> dict:
        """Create a long-lived refresh token payload."""
        now = int(time.time())
        return {
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + self.settings.refresh_days * 24 * 3600,
        }

    def verify_jwt(self, token_payload: dict) -> dict:
        """Validate a JWT-like token payload and return decoded claims.

        This is the central authentication verification point.
        It checks token presence, subject, expiration, and token type.
        """
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
        """Validate a refresh token and issue a new access token."""
        claims = self.verify_jwt(refresh_payload)
        if claims.get("type") != "refresh":
            raise TokenError("Not a refresh token")
        return self.create_access_token(claims["sub"])

    def encode_payload(self, payload: dict) -> str:
        """Encode a token payload for transport in this demo service."""
        raw = json.dumps(payload, sort_keys=True).encode(
```

## Instructions for Gemma 4
- Answer only using the MICode Context Pack above.
- Cite file paths, symbol names, and line ranges when available.
- If the context is insufficient, say what is missing.
- Prefer clear explanations for students and practical next steps for developers.
- Do not claim you inspected files that are not in this context.
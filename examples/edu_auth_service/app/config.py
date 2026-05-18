import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    jwt_secret: str
    access_minutes: int
    refresh_days: int
    password_salt: str
    login_rate_limit_per_minute: int

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        return cls(
            jwt_secret=os.getenv("JWT_SECRET", "dev-secret"),
            access_minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", "15")),
            refresh_days=int(os.getenv("REFRESH_TOKEN_DAYS", "7")),
            password_salt=os.getenv("PASSWORD_SALT", "dev-salt"),
            login_rate_limit_per_minute=int(os.getenv("LOGIN_RATE_LIMIT_PER_MINUTE", "5")),
        )

    def token_config(self) -> dict:
        """Return token-related configuration."""
        return {
            "jwt_secret": self.jwt_secret,
            "access_minutes": self.access_minutes,
            "refresh_days": self.refresh_days,
        }

    def security_config(self) -> dict:
        """Return security-related configuration."""
        return {
            "password_salt": self.password_salt,
            "login_rate_limit_per_minute": self.login_rate_limit_per_minute,
        }

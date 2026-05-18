from app.config import Settings
from app.auth.routes import login, refresh
from app.middleware.auth_required import auth_required
from app.db.users import build_user_store


def create_app():
    """Create the application and register auth routes."""
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
    """Return service health information."""
    return {"status": "ok", "service": "edu_auth_service"}

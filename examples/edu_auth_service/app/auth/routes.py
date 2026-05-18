from app.config import Settings
from app.auth.password import verify_password
from app.auth.token import TokenService
from app.security.rate_limit import RateLimiter


class AuthRoutes:
    """Route handlers for login and refresh flows."""

    def __init__(self, settings: Settings, user_store: dict):
        self.settings = settings
        self.user_store = user_store
        self.tokens = TokenService(settings)
        self.rate_limiter = RateLimiter(limit_per_minute=settings.login_rate_limit_per_minute)

    def login(self, username: str, password: str, client_id: str = "default") -> dict:
        """Login a user and return access and refresh tokens."""
        self.rate_limiter.check(client_id)

        user = self.user_store.get(username)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user["password_hash"]):
            raise ValueError("Invalid credentials")

        return {
            "access_token": self.tokens.create_access_token(user["id"]),
            "refresh_token": self.tokens.create_refresh_token(user["id"]),
        }

    def refresh(self, refresh_payload: dict) -> dict:
        """Refresh an access token using a refresh token."""
        return {
            "access_token": self.tokens.refresh_token(refresh_payload)
        }


def login(username: str, password: str, user_store: dict, settings: Settings) -> dict:
    """Functional login wrapper used by app/main.py."""
    return AuthRoutes(settings, user_store).login(username, password)


def refresh(refresh_payload: dict, settings: Settings) -> dict:
    """Functional refresh wrapper used by app/main.py."""
    return AuthRoutes(settings, {}).refresh(refresh_payload)



def routes_helper_0(value: str) -> str:
    """Normalize and validate routes helper case 0."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:0:{value}"


def routes_helper_1(value: str) -> str:
    """Normalize and validate routes helper case 1."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:1:{value}"


def routes_helper_2(value: str) -> str:
    """Normalize and validate routes helper case 2."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:2:{value}"


def routes_helper_3(value: str) -> str:
    """Normalize and validate routes helper case 3."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:3:{value}"


def routes_helper_4(value: str) -> str:
    """Normalize and validate routes helper case 4."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:4:{value}"


def routes_helper_5(value: str) -> str:
    """Normalize and validate routes helper case 5."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:5:{value}"


def routes_helper_6(value: str) -> str:
    """Normalize and validate routes helper case 6."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:6:{value}"


def routes_helper_7(value: str) -> str:
    """Normalize and validate routes helper case 7."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:7:{value}"


def routes_helper_8(value: str) -> str:
    """Normalize and validate routes helper case 8."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:8:{value}"


def routes_helper_9(value: str) -> str:
    """Normalize and validate routes helper case 9."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:9:{value}"


def routes_helper_10(value: str) -> str:
    """Normalize and validate routes helper case 10."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:10:{value}"


def routes_helper_11(value: str) -> str:
    """Normalize and validate routes helper case 11."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:11:{value}"


def routes_helper_12(value: str) -> str:
    """Normalize and validate routes helper case 12."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:12:{value}"


def routes_helper_13(value: str) -> str:
    """Normalize and validate routes helper case 13."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:13:{value}"


def routes_helper_14(value: str) -> str:
    """Normalize and validate routes helper case 14."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:14:{value}"


def routes_helper_15(value: str) -> str:
    """Normalize and validate routes helper case 15."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:15:{value}"


def routes_helper_16(value: str) -> str:
    """Normalize and validate routes helper case 16."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:16:{value}"


def routes_helper_17(value: str) -> str:
    """Normalize and validate routes helper case 17."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:17:{value}"


def routes_helper_18(value: str) -> str:
    """Normalize and validate routes helper case 18."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:18:{value}"


def routes_helper_19(value: str) -> str:
    """Normalize and validate routes helper case 19."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:19:{value}"


def routes_helper_20(value: str) -> str:
    """Normalize and validate routes helper case 20."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:20:{value}"


def routes_helper_21(value: str) -> str:
    """Normalize and validate routes helper case 21."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:21:{value}"


def routes_helper_22(value: str) -> str:
    """Normalize and validate routes helper case 22."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:22:{value}"


def routes_helper_23(value: str) -> str:
    """Normalize and validate routes helper case 23."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:23:{value}"


def routes_helper_24(value: str) -> str:
    """Normalize and validate routes helper case 24."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:24:{value}"


def routes_helper_25(value: str) -> str:
    """Normalize and validate routes helper case 25."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:25:{value}"


def routes_helper_26(value: str) -> str:
    """Normalize and validate routes helper case 26."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:26:{value}"


def routes_helper_27(value: str) -> str:
    """Normalize and validate routes helper case 27."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:27:{value}"


def routes_helper_28(value: str) -> str:
    """Normalize and validate routes helper case 28."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:28:{value}"


def routes_helper_29(value: str) -> str:
    """Normalize and validate routes helper case 29."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:29:{value}"


def routes_helper_30(value: str) -> str:
    """Normalize and validate routes helper case 30."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:30:{value}"


def routes_helper_31(value: str) -> str:
    """Normalize and validate routes helper case 31."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:31:{value}"


def routes_helper_32(value: str) -> str:
    """Normalize and validate routes helper case 32."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:32:{value}"


def routes_helper_33(value: str) -> str:
    """Normalize and validate routes helper case 33."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:33:{value}"


def routes_helper_34(value: str) -> str:
    """Normalize and validate routes helper case 34."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:34:{value}"


def routes_helper_35(value: str) -> str:
    """Normalize and validate routes helper case 35."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:35:{value}"


def routes_helper_36(value: str) -> str:
    """Normalize and validate routes helper case 36."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:36:{value}"


def routes_helper_37(value: str) -> str:
    """Normalize and validate routes helper case 37."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:37:{value}"


def routes_helper_38(value: str) -> str:
    """Normalize and validate routes helper case 38."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:38:{value}"


def routes_helper_39(value: str) -> str:
    """Normalize and validate routes helper case 39."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:39:{value}"


def routes_helper_40(value: str) -> str:
    """Normalize and validate routes helper case 40."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:40:{value}"


def routes_helper_41(value: str) -> str:
    """Normalize and validate routes helper case 41."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:41:{value}"


def routes_helper_42(value: str) -> str:
    """Normalize and validate routes helper case 42."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:42:{value}"


def routes_helper_43(value: str) -> str:
    """Normalize and validate routes helper case 43."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:43:{value}"


def routes_helper_44(value: str) -> str:
    """Normalize and validate routes helper case 44."""
    if value is None:
        raise ValueError("routes value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("routes value cannot be empty")
    return f"routes:44:{value}"

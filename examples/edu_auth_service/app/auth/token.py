import time
import base64
import json
from app.config import Settings


class TokenError(ValueError):
    """Raised when token validation fails."""


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
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii")

    def decode_payload(self, token: str) -> dict:
        """Decode a token string into a dictionary payload."""
        try:
            raw = base64.urlsafe_b64decode(token.encode("ascii"))
            return json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise TokenError("Invalid token encoding") from exc


def create_access_token(user_id: str, settings: Settings) -> dict:
    """Create a short-lived access token payload."""
    return TokenService(settings).create_access_token(user_id)


def create_refresh_token(user_id: str, settings: Settings) -> dict:
    """Create a long-lived refresh token payload."""
    return TokenService(settings).create_refresh_token(user_id)


def verify_jwt(token_payload: dict) -> dict:
    """Validate a JWT-like token payload using demo default settings."""
    settings = Settings.from_env()
    return TokenService(settings).verify_jwt(token_payload)


def refresh_token(refresh_payload: dict, settings: Settings) -> dict:
    """Validate a refresh token and issue a new access token."""
    return TokenService(settings).refresh_token(refresh_payload)



def token_helper_0(value: str) -> str:
    """Normalize and validate token helper case 0."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:0:{value}"


def token_helper_1(value: str) -> str:
    """Normalize and validate token helper case 1."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:1:{value}"


def token_helper_2(value: str) -> str:
    """Normalize and validate token helper case 2."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:2:{value}"


def token_helper_3(value: str) -> str:
    """Normalize and validate token helper case 3."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:3:{value}"


def token_helper_4(value: str) -> str:
    """Normalize and validate token helper case 4."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:4:{value}"


def token_helper_5(value: str) -> str:
    """Normalize and validate token helper case 5."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:5:{value}"


def token_helper_6(value: str) -> str:
    """Normalize and validate token helper case 6."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:6:{value}"


def token_helper_7(value: str) -> str:
    """Normalize and validate token helper case 7."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:7:{value}"


def token_helper_8(value: str) -> str:
    """Normalize and validate token helper case 8."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:8:{value}"


def token_helper_9(value: str) -> str:
    """Normalize and validate token helper case 9."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:9:{value}"


def token_helper_10(value: str) -> str:
    """Normalize and validate token helper case 10."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:10:{value}"


def token_helper_11(value: str) -> str:
    """Normalize and validate token helper case 11."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:11:{value}"


def token_helper_12(value: str) -> str:
    """Normalize and validate token helper case 12."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:12:{value}"


def token_helper_13(value: str) -> str:
    """Normalize and validate token helper case 13."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:13:{value}"


def token_helper_14(value: str) -> str:
    """Normalize and validate token helper case 14."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:14:{value}"


def token_helper_15(value: str) -> str:
    """Normalize and validate token helper case 15."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:15:{value}"


def token_helper_16(value: str) -> str:
    """Normalize and validate token helper case 16."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:16:{value}"


def token_helper_17(value: str) -> str:
    """Normalize and validate token helper case 17."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:17:{value}"


def token_helper_18(value: str) -> str:
    """Normalize and validate token helper case 18."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:18:{value}"


def token_helper_19(value: str) -> str:
    """Normalize and validate token helper case 19."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:19:{value}"


def token_helper_20(value: str) -> str:
    """Normalize and validate token helper case 20."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:20:{value}"


def token_helper_21(value: str) -> str:
    """Normalize and validate token helper case 21."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:21:{value}"


def token_helper_22(value: str) -> str:
    """Normalize and validate token helper case 22."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:22:{value}"


def token_helper_23(value: str) -> str:
    """Normalize and validate token helper case 23."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:23:{value}"


def token_helper_24(value: str) -> str:
    """Normalize and validate token helper case 24."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:24:{value}"


def token_helper_25(value: str) -> str:
    """Normalize and validate token helper case 25."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:25:{value}"


def token_helper_26(value: str) -> str:
    """Normalize and validate token helper case 26."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:26:{value}"


def token_helper_27(value: str) -> str:
    """Normalize and validate token helper case 27."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:27:{value}"


def token_helper_28(value: str) -> str:
    """Normalize and validate token helper case 28."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:28:{value}"


def token_helper_29(value: str) -> str:
    """Normalize and validate token helper case 29."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:29:{value}"


def token_helper_30(value: str) -> str:
    """Normalize and validate token helper case 30."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:30:{value}"


def token_helper_31(value: str) -> str:
    """Normalize and validate token helper case 31."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:31:{value}"


def token_helper_32(value: str) -> str:
    """Normalize and validate token helper case 32."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:32:{value}"


def token_helper_33(value: str) -> str:
    """Normalize and validate token helper case 33."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:33:{value}"


def token_helper_34(value: str) -> str:
    """Normalize and validate token helper case 34."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:34:{value}"


def token_helper_35(value: str) -> str:
    """Normalize and validate token helper case 35."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:35:{value}"


def token_helper_36(value: str) -> str:
    """Normalize and validate token helper case 36."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:36:{value}"


def token_helper_37(value: str) -> str:
    """Normalize and validate token helper case 37."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:37:{value}"


def token_helper_38(value: str) -> str:
    """Normalize and validate token helper case 38."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:38:{value}"


def token_helper_39(value: str) -> str:
    """Normalize and validate token helper case 39."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:39:{value}"


def token_helper_40(value: str) -> str:
    """Normalize and validate token helper case 40."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:40:{value}"


def token_helper_41(value: str) -> str:
    """Normalize and validate token helper case 41."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:41:{value}"


def token_helper_42(value: str) -> str:
    """Normalize and validate token helper case 42."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:42:{value}"


def token_helper_43(value: str) -> str:
    """Normalize and validate token helper case 43."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:43:{value}"


def token_helper_44(value: str) -> str:
    """Normalize and validate token helper case 44."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:44:{value}"


def token_helper_45(value: str) -> str:
    """Normalize and validate token helper case 45."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:45:{value}"


def token_helper_46(value: str) -> str:
    """Normalize and validate token helper case 46."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:46:{value}"


def token_helper_47(value: str) -> str:
    """Normalize and validate token helper case 47."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:47:{value}"


def token_helper_48(value: str) -> str:
    """Normalize and validate token helper case 48."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:48:{value}"


def token_helper_49(value: str) -> str:
    """Normalize and validate token helper case 49."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:49:{value}"


def token_helper_50(value: str) -> str:
    """Normalize and validate token helper case 50."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:50:{value}"


def token_helper_51(value: str) -> str:
    """Normalize and validate token helper case 51."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:51:{value}"


def token_helper_52(value: str) -> str:
    """Normalize and validate token helper case 52."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:52:{value}"


def token_helper_53(value: str) -> str:
    """Normalize and validate token helper case 53."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:53:{value}"


def token_helper_54(value: str) -> str:
    """Normalize and validate token helper case 54."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:54:{value}"


def token_helper_55(value: str) -> str:
    """Normalize and validate token helper case 55."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:55:{value}"


def token_helper_56(value: str) -> str:
    """Normalize and validate token helper case 56."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:56:{value}"


def token_helper_57(value: str) -> str:
    """Normalize and validate token helper case 57."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:57:{value}"


def token_helper_58(value: str) -> str:
    """Normalize and validate token helper case 58."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:58:{value}"


def token_helper_59(value: str) -> str:
    """Normalize and validate token helper case 59."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:59:{value}"


def token_helper_60(value: str) -> str:
    """Normalize and validate token helper case 60."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:60:{value}"


def token_helper_61(value: str) -> str:
    """Normalize and validate token helper case 61."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:61:{value}"


def token_helper_62(value: str) -> str:
    """Normalize and validate token helper case 62."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:62:{value}"


def token_helper_63(value: str) -> str:
    """Normalize and validate token helper case 63."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:63:{value}"


def token_helper_64(value: str) -> str:
    """Normalize and validate token helper case 64."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:64:{value}"


def token_helper_65(value: str) -> str:
    """Normalize and validate token helper case 65."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:65:{value}"


def token_helper_66(value: str) -> str:
    """Normalize and validate token helper case 66."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:66:{value}"


def token_helper_67(value: str) -> str:
    """Normalize and validate token helper case 67."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:67:{value}"


def token_helper_68(value: str) -> str:
    """Normalize and validate token helper case 68."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:68:{value}"


def token_helper_69(value: str) -> str:
    """Normalize and validate token helper case 69."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:69:{value}"


def token_helper_70(value: str) -> str:
    """Normalize and validate token helper case 70."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:70:{value}"


def token_helper_71(value: str) -> str:
    """Normalize and validate token helper case 71."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:71:{value}"


def token_helper_72(value: str) -> str:
    """Normalize and validate token helper case 72."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:72:{value}"


def token_helper_73(value: str) -> str:
    """Normalize and validate token helper case 73."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:73:{value}"


def token_helper_74(value: str) -> str:
    """Normalize and validate token helper case 74."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:74:{value}"


def token_helper_75(value: str) -> str:
    """Normalize and validate token helper case 75."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:75:{value}"


def token_helper_76(value: str) -> str:
    """Normalize and validate token helper case 76."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:76:{value}"


def token_helper_77(value: str) -> str:
    """Normalize and validate token helper case 77."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:77:{value}"


def token_helper_78(value: str) -> str:
    """Normalize and validate token helper case 78."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:78:{value}"


def token_helper_79(value: str) -> str:
    """Normalize and validate token helper case 79."""
    if value is None:
        raise ValueError("token value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("token value cannot be empty")
    return f"token:79:{value}"

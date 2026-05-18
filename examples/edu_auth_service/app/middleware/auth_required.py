from app.auth.token import TokenService
from app.config import Settings


class AuthMiddleware:
    """Authentication middleware that protects incoming requests."""

    def __init__(self, settings: Settings):
        self.tokens = TokenService(settings)

    def auth_required(self, request: dict) -> dict:
        """Require a valid access token before allowing a request.

        This middleware calls TokenService.verify_jwt and then checks that
        the token type is access.
        """
        token_payload = request.get("token")
        claims = self.tokens.verify_jwt(token_payload)

        if claims.get("type") != "access":
            raise ValueError("Access token required")

        request["user_id"] = claims["sub"]
        return request


def auth_required(request: dict) -> dict:
    """Require a valid access token using default settings."""
    return AuthMiddleware(Settings.from_env()).auth_required(request)



def middleware_helper_0(value: str) -> str:
    """Normalize and validate middleware helper case 0."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:0:{value}"


def middleware_helper_1(value: str) -> str:
    """Normalize and validate middleware helper case 1."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:1:{value}"


def middleware_helper_2(value: str) -> str:
    """Normalize and validate middleware helper case 2."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:2:{value}"


def middleware_helper_3(value: str) -> str:
    """Normalize and validate middleware helper case 3."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:3:{value}"


def middleware_helper_4(value: str) -> str:
    """Normalize and validate middleware helper case 4."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:4:{value}"


def middleware_helper_5(value: str) -> str:
    """Normalize and validate middleware helper case 5."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:5:{value}"


def middleware_helper_6(value: str) -> str:
    """Normalize and validate middleware helper case 6."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:6:{value}"


def middleware_helper_7(value: str) -> str:
    """Normalize and validate middleware helper case 7."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:7:{value}"


def middleware_helper_8(value: str) -> str:
    """Normalize and validate middleware helper case 8."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:8:{value}"


def middleware_helper_9(value: str) -> str:
    """Normalize and validate middleware helper case 9."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:9:{value}"


def middleware_helper_10(value: str) -> str:
    """Normalize and validate middleware helper case 10."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:10:{value}"


def middleware_helper_11(value: str) -> str:
    """Normalize and validate middleware helper case 11."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:11:{value}"


def middleware_helper_12(value: str) -> str:
    """Normalize and validate middleware helper case 12."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:12:{value}"


def middleware_helper_13(value: str) -> str:
    """Normalize and validate middleware helper case 13."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:13:{value}"


def middleware_helper_14(value: str) -> str:
    """Normalize and validate middleware helper case 14."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:14:{value}"


def middleware_helper_15(value: str) -> str:
    """Normalize and validate middleware helper case 15."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:15:{value}"


def middleware_helper_16(value: str) -> str:
    """Normalize and validate middleware helper case 16."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:16:{value}"


def middleware_helper_17(value: str) -> str:
    """Normalize and validate middleware helper case 17."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:17:{value}"


def middleware_helper_18(value: str) -> str:
    """Normalize and validate middleware helper case 18."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:18:{value}"


def middleware_helper_19(value: str) -> str:
    """Normalize and validate middleware helper case 19."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:19:{value}"


def middleware_helper_20(value: str) -> str:
    """Normalize and validate middleware helper case 20."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:20:{value}"


def middleware_helper_21(value: str) -> str:
    """Normalize and validate middleware helper case 21."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:21:{value}"


def middleware_helper_22(value: str) -> str:
    """Normalize and validate middleware helper case 22."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:22:{value}"


def middleware_helper_23(value: str) -> str:
    """Normalize and validate middleware helper case 23."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:23:{value}"


def middleware_helper_24(value: str) -> str:
    """Normalize and validate middleware helper case 24."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:24:{value}"


def middleware_helper_25(value: str) -> str:
    """Normalize and validate middleware helper case 25."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:25:{value}"


def middleware_helper_26(value: str) -> str:
    """Normalize and validate middleware helper case 26."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:26:{value}"


def middleware_helper_27(value: str) -> str:
    """Normalize and validate middleware helper case 27."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:27:{value}"


def middleware_helper_28(value: str) -> str:
    """Normalize and validate middleware helper case 28."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:28:{value}"


def middleware_helper_29(value: str) -> str:
    """Normalize and validate middleware helper case 29."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:29:{value}"


def middleware_helper_30(value: str) -> str:
    """Normalize and validate middleware helper case 30."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:30:{value}"


def middleware_helper_31(value: str) -> str:
    """Normalize and validate middleware helper case 31."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:31:{value}"


def middleware_helper_32(value: str) -> str:
    """Normalize and validate middleware helper case 32."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:32:{value}"


def middleware_helper_33(value: str) -> str:
    """Normalize and validate middleware helper case 33."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:33:{value}"


def middleware_helper_34(value: str) -> str:
    """Normalize and validate middleware helper case 34."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:34:{value}"


def middleware_helper_35(value: str) -> str:
    """Normalize and validate middleware helper case 35."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:35:{value}"


def middleware_helper_36(value: str) -> str:
    """Normalize and validate middleware helper case 36."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:36:{value}"


def middleware_helper_37(value: str) -> str:
    """Normalize and validate middleware helper case 37."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:37:{value}"


def middleware_helper_38(value: str) -> str:
    """Normalize and validate middleware helper case 38."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:38:{value}"


def middleware_helper_39(value: str) -> str:
    """Normalize and validate middleware helper case 39."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:39:{value}"


def middleware_helper_40(value: str) -> str:
    """Normalize and validate middleware helper case 40."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:40:{value}"


def middleware_helper_41(value: str) -> str:
    """Normalize and validate middleware helper case 41."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:41:{value}"


def middleware_helper_42(value: str) -> str:
    """Normalize and validate middleware helper case 42."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:42:{value}"


def middleware_helper_43(value: str) -> str:
    """Normalize and validate middleware helper case 43."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:43:{value}"


def middleware_helper_44(value: str) -> str:
    """Normalize and validate middleware helper case 44."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:44:{value}"


def middleware_helper_45(value: str) -> str:
    """Normalize and validate middleware helper case 45."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:45:{value}"


def middleware_helper_46(value: str) -> str:
    """Normalize and validate middleware helper case 46."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:46:{value}"


def middleware_helper_47(value: str) -> str:
    """Normalize and validate middleware helper case 47."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:47:{value}"


def middleware_helper_48(value: str) -> str:
    """Normalize and validate middleware helper case 48."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:48:{value}"


def middleware_helper_49(value: str) -> str:
    """Normalize and validate middleware helper case 49."""
    if value is None:
        raise ValueError("middleware value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("middleware value cannot be empty")
    return f"middleware:49:{value}"

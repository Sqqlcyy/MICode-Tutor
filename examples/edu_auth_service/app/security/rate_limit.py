import time
from collections import defaultdict, deque


class RateLimitExceeded(ValueError):
    """Raised when a client exceeds the allowed request rate."""


class RateLimiter:
    """Simple in-memory rate limiter for login attempts."""

    def __init__(self, limit_per_minute: int):
        self.limit_per_minute = limit_per_minute
        self.events = defaultdict(deque)

    def check(self, client_id: str) -> None:
        """Check whether a client is allowed to perform another login attempt."""
        now = time.time()
        window_start = now - 60
        q = self.events[client_id]

        while q and q[0] < window_start:
            q.popleft()

        if len(q) >= self.limit_per_minute:
            raise RateLimitExceeded("Too many login attempts")

        q.append(now)

    def reset(self, client_id: str) -> None:
        """Reset rate limit state for a client."""
        self.events.pop(client_id, None)



def rate_limit_helper_0(value: str) -> str:
    """Normalize and validate rate_limit helper case 0."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:0:{value}"


def rate_limit_helper_1(value: str) -> str:
    """Normalize and validate rate_limit helper case 1."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:1:{value}"


def rate_limit_helper_2(value: str) -> str:
    """Normalize and validate rate_limit helper case 2."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:2:{value}"


def rate_limit_helper_3(value: str) -> str:
    """Normalize and validate rate_limit helper case 3."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:3:{value}"


def rate_limit_helper_4(value: str) -> str:
    """Normalize and validate rate_limit helper case 4."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:4:{value}"


def rate_limit_helper_5(value: str) -> str:
    """Normalize and validate rate_limit helper case 5."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:5:{value}"


def rate_limit_helper_6(value: str) -> str:
    """Normalize and validate rate_limit helper case 6."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:6:{value}"


def rate_limit_helper_7(value: str) -> str:
    """Normalize and validate rate_limit helper case 7."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:7:{value}"


def rate_limit_helper_8(value: str) -> str:
    """Normalize and validate rate_limit helper case 8."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:8:{value}"


def rate_limit_helper_9(value: str) -> str:
    """Normalize and validate rate_limit helper case 9."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:9:{value}"


def rate_limit_helper_10(value: str) -> str:
    """Normalize and validate rate_limit helper case 10."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:10:{value}"


def rate_limit_helper_11(value: str) -> str:
    """Normalize and validate rate_limit helper case 11."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:11:{value}"


def rate_limit_helper_12(value: str) -> str:
    """Normalize and validate rate_limit helper case 12."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:12:{value}"


def rate_limit_helper_13(value: str) -> str:
    """Normalize and validate rate_limit helper case 13."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:13:{value}"


def rate_limit_helper_14(value: str) -> str:
    """Normalize and validate rate_limit helper case 14."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:14:{value}"


def rate_limit_helper_15(value: str) -> str:
    """Normalize and validate rate_limit helper case 15."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:15:{value}"


def rate_limit_helper_16(value: str) -> str:
    """Normalize and validate rate_limit helper case 16."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:16:{value}"


def rate_limit_helper_17(value: str) -> str:
    """Normalize and validate rate_limit helper case 17."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:17:{value}"


def rate_limit_helper_18(value: str) -> str:
    """Normalize and validate rate_limit helper case 18."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:18:{value}"


def rate_limit_helper_19(value: str) -> str:
    """Normalize and validate rate_limit helper case 19."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:19:{value}"


def rate_limit_helper_20(value: str) -> str:
    """Normalize and validate rate_limit helper case 20."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:20:{value}"


def rate_limit_helper_21(value: str) -> str:
    """Normalize and validate rate_limit helper case 21."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:21:{value}"


def rate_limit_helper_22(value: str) -> str:
    """Normalize and validate rate_limit helper case 22."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:22:{value}"


def rate_limit_helper_23(value: str) -> str:
    """Normalize and validate rate_limit helper case 23."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:23:{value}"


def rate_limit_helper_24(value: str) -> str:
    """Normalize and validate rate_limit helper case 24."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:24:{value}"


def rate_limit_helper_25(value: str) -> str:
    """Normalize and validate rate_limit helper case 25."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:25:{value}"


def rate_limit_helper_26(value: str) -> str:
    """Normalize and validate rate_limit helper case 26."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:26:{value}"


def rate_limit_helper_27(value: str) -> str:
    """Normalize and validate rate_limit helper case 27."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:27:{value}"


def rate_limit_helper_28(value: str) -> str:
    """Normalize and validate rate_limit helper case 28."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:28:{value}"


def rate_limit_helper_29(value: str) -> str:
    """Normalize and validate rate_limit helper case 29."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:29:{value}"


def rate_limit_helper_30(value: str) -> str:
    """Normalize and validate rate_limit helper case 30."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:30:{value}"


def rate_limit_helper_31(value: str) -> str:
    """Normalize and validate rate_limit helper case 31."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:31:{value}"


def rate_limit_helper_32(value: str) -> str:
    """Normalize and validate rate_limit helper case 32."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:32:{value}"


def rate_limit_helper_33(value: str) -> str:
    """Normalize and validate rate_limit helper case 33."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:33:{value}"


def rate_limit_helper_34(value: str) -> str:
    """Normalize and validate rate_limit helper case 34."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:34:{value}"


def rate_limit_helper_35(value: str) -> str:
    """Normalize and validate rate_limit helper case 35."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:35:{value}"


def rate_limit_helper_36(value: str) -> str:
    """Normalize and validate rate_limit helper case 36."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:36:{value}"


def rate_limit_helper_37(value: str) -> str:
    """Normalize and validate rate_limit helper case 37."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:37:{value}"


def rate_limit_helper_38(value: str) -> str:
    """Normalize and validate rate_limit helper case 38."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:38:{value}"


def rate_limit_helper_39(value: str) -> str:
    """Normalize and validate rate_limit helper case 39."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:39:{value}"


def rate_limit_helper_40(value: str) -> str:
    """Normalize and validate rate_limit helper case 40."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:40:{value}"


def rate_limit_helper_41(value: str) -> str:
    """Normalize and validate rate_limit helper case 41."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:41:{value}"


def rate_limit_helper_42(value: str) -> str:
    """Normalize and validate rate_limit helper case 42."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:42:{value}"


def rate_limit_helper_43(value: str) -> str:
    """Normalize and validate rate_limit helper case 43."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:43:{value}"


def rate_limit_helper_44(value: str) -> str:
    """Normalize and validate rate_limit helper case 44."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:44:{value}"


def rate_limit_helper_45(value: str) -> str:
    """Normalize and validate rate_limit helper case 45."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:45:{value}"


def rate_limit_helper_46(value: str) -> str:
    """Normalize and validate rate_limit helper case 46."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:46:{value}"


def rate_limit_helper_47(value: str) -> str:
    """Normalize and validate rate_limit helper case 47."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:47:{value}"


def rate_limit_helper_48(value: str) -> str:
    """Normalize and validate rate_limit helper case 48."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:48:{value}"


def rate_limit_helper_49(value: str) -> str:
    """Normalize and validate rate_limit helper case 49."""
    if value is None:
        raise ValueError("rate_limit value cannot be None")
    value = value.strip()
    if not value:
        raise ValueError("rate_limit value cannot be empty")
    return f"rate_limit:49:{value}"

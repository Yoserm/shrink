import secrets
from urllib.parse import urlparse

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_code(length: int = 7) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def validate_url(raw: str) -> str:
    p = urlparse(raw)

    if p.scheme not in ("http", "https"):
        raise ValueError(f"unsupported scheme: {p.scheme!r}")

    if not p.netloc:
        raise ValueError("missing host")

    return raw
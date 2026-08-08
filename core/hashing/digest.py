import hashlib


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sha512(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()
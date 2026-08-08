from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

from core.exceptions import CipherError

_hasher = PasswordHasher()


class PasswordVerificationError(CipherError):
    """Raised when a password does not match its stored hash."""


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password must not be empty.")
    return _hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return _hasher.verify(hashed, password)
    except VerifyMismatchError:
        return False
    except InvalidHash:
        raise PasswordVerificationError("Provided hash is not a valid Argon2 hash.")
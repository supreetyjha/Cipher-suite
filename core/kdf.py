import os
import base64
from argon2.low_level import hash_secret_raw, Type

from core.exceptions import InvalidKeyError


def derive_key(passphrase: str, salt: bytes | None = None) -> dict:
    if not passphrase:
        raise InvalidKeyError("Passphrase must not be empty.")

    if salt is None:
        salt = os.urandom(16)

    key = hash_secret_raw(
        secret=passphrase.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )

    return {
        "key": base64.b64encode(key).decode(),
        "salt": base64.b64encode(salt).decode(),
    }
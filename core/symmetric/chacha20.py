import os
import base64
from Crypto.Cipher import ChaCha20

from core.exceptions import InvalidKeyError

KEY_SIZE = 32
NONCE_SIZE = 12


def generate_key() -> str:
    return base64.b64encode(os.urandom(KEY_SIZE)).decode()


def _validate_key(key_b64: str) -> bytes:
    try:
        key = base64.b64decode(key_b64)
    except Exception:
        raise InvalidKeyError("Key must be valid base64.")
    if len(key) != KEY_SIZE:
        raise InvalidKeyError(f"Key must decode to {KEY_SIZE} bytes.")
    return key


def encrypt(plaintext: str, key_b64: str) -> dict:
    key = _validate_key(key_b64)
    nonce = os.urandom(NONCE_SIZE)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(plaintext.encode())
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
    }


def decrypt(ciphertext_b64: str, key_b64: str, nonce_b64: str) -> str:
    key = _validate_key(key_b64)
    try:
        nonce = base64.b64decode(nonce_b64)
        ciphertext = base64.b64decode(ciphertext_b64)
        cipher = ChaCha20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()
    except Exception as e:
        raise InvalidKeyError(f"Decryption failed: {str(e)}")
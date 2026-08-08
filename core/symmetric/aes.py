import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from core.exceptions import InvalidKeyError, UnsupportedModeError, DecryptionError

VALID_MODES = {"ECB", "CBC", "CFB", "OFB", "GCM"}
KEY_SIZE = 32  # AES-256


def generate_key() -> str:
    return base64.b64encode(os.urandom(KEY_SIZE)).decode()


def _validate_key(key_b64: str) -> bytes:
    try:
        key = base64.b64decode(key_b64)
    except Exception:
        raise InvalidKeyError("Key must be valid base64.")
    if len(key) != KEY_SIZE:
        raise InvalidKeyError(f"Key must decode to {KEY_SIZE} bytes (AES-256).")
    return key


def encrypt(plaintext: str, key_b64: str, mode: str) -> dict:
    mode = mode.upper()
    if mode not in VALID_MODES:
        raise UnsupportedModeError(f"Unsupported AES mode: {mode}")

    key = _validate_key(key_b64)
    data = plaintext.encode()

    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return {"ciphertext": base64.b64encode(ciphertext).decode(), "iv": None, "tag": None}

    elif mode == "CBC":
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return {"ciphertext": base64.b64encode(ciphertext).decode(), "iv": base64.b64encode(iv).decode(), "tag": None}

    elif mode == "CFB":
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(data)
        return {"ciphertext": base64.b64encode(ciphertext).decode(), "iv": base64.b64encode(iv).decode(), "tag": None}

    elif mode == "OFB":
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_OFB, iv)
        ciphertext = cipher.encrypt(data)
        return {"ciphertext": base64.b64encode(ciphertext).decode(), "iv": base64.b64encode(iv).decode(), "tag": None}

    elif mode == "GCM":
        nonce = os.urandom(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(nonce).decode(),
            "tag": base64.b64encode(tag).decode(),
        }


def decrypt(ciphertext_b64: str, key_b64: str, mode: str, iv_b64: str | None = None, tag_b64: str | None = None) -> str:
    mode = mode.upper()
    if mode not in VALID_MODES:
        raise UnsupportedModeError(f"Unsupported AES mode: {mode}")

    key = _validate_key(key_b64)

    try:
        ciphertext = base64.b64decode(ciphertext_b64)

        if mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        elif mode == "CBC":
            if not iv_b64:
                raise DecryptionError("IV is required for CBC mode.")
            iv = base64.b64decode(iv_b64)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        elif mode == "CFB":
            if not iv_b64:
                raise DecryptionError("IV is required for CFB mode.")
            iv = base64.b64decode(iv_b64)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            plaintext = cipher.decrypt(ciphertext)

        elif mode == "OFB":
            if not iv_b64:
                raise DecryptionError("IV is required for OFB mode.")
            iv = base64.b64decode(iv_b64)
            cipher = AES.new(key, AES.MODE_OFB, iv)
            plaintext = cipher.decrypt(ciphertext)

        elif mode == "GCM":
            if not iv_b64 or not tag_b64:
                raise DecryptionError("Nonce and tag are required for GCM mode.")
            nonce = base64.b64decode(iv_b64)
            tag = base64.b64decode(tag_b64)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext.decode()

    except (ValueError, KeyError) as e:
        raise DecryptionError(f"Decryption failed: {str(e)}")
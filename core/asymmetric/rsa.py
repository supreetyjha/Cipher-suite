import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from core.exceptions import InvalidKeyError, DecryptionError


def generate_keypair() -> dict:
    key = RSA.generate(2048)
    private_pem = key.export_key().decode()
    public_pem = key.publickey().export_key().decode()
    return {"private_key": private_pem, "public_key": public_pem}


def _load_public_key(pem: str):
    try:
        return RSA.import_key(pem)
    except Exception:
        raise InvalidKeyError("Invalid public key format.")


def _load_private_key(pem: str):
    try:
        return RSA.import_key(pem)
    except Exception:
        raise InvalidKeyError("Invalid private key format.")


def encrypt(plaintext: str, public_key_pem: str) -> str:
    key = _load_public_key(public_key_pem)
    cipher = PKCS1_OAEP.new(key)
    # RSA-2048 with OAEP can only encrypt small payloads (~190 bytes) — expected limitation
    try:
        ciphertext = cipher.encrypt(plaintext.encode())
    except ValueError as e:
        raise InvalidKeyError(f"Message too long for RSA encryption: {str(e)}")
    return base64.b64encode(ciphertext).decode()


def decrypt(ciphertext_b64: str, private_key_pem: str) -> str:
    key = _load_private_key(private_key_pem)
    cipher = PKCS1_OAEP.new(key)
    try:
        ciphertext = base64.b64decode(ciphertext_b64)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode()
    except (ValueError, TypeError) as e:
        raise DecryptionError(f"RSA decryption failed: {str(e)}")


def sign(message: str, private_key_pem: str) -> str:
    key = _load_private_key(private_key_pem)
    h = SHA256.new(message.encode())
    signature = pkcs1_15.new(key).sign(h)
    return base64.b64encode(signature).decode()


def verify(message: str, signature_b64: str, public_key_pem: str) -> bool:
    key = _load_public_key(public_key_pem)
    h = SHA256.new(message.encode())
    try:
        signature = base64.b64decode(signature_b64)
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
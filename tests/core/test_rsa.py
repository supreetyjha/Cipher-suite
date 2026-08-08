import pytest
from core.asymmetric import rsa
from core.exceptions import DecryptionError


def test_generate_keypair():
    keys = rsa.generate_keypair()
    assert "PRIVATE KEY" in keys["private_key"]
    assert "PUBLIC KEY" in keys["public_key"]


def test_encrypt_decrypt_roundtrip():
    keys = rsa.generate_keypair()
    plaintext = "Attack at dawn"
    ciphertext = rsa.encrypt(plaintext, keys["public_key"])
    decrypted = rsa.decrypt(ciphertext, keys["private_key"])
    assert decrypted == plaintext


def test_sign_and_verify():
    keys = rsa.generate_keypair()
    message = "This message is authentic"
    signature = rsa.sign(message, keys["private_key"])
    assert rsa.verify(message, signature, keys["public_key"])


def test_tampered_message_fails_verification():
    keys = rsa.generate_keypair()
    signature = rsa.sign("original message", keys["private_key"])
    assert not rsa.verify("tampered message", signature, keys["public_key"])


def test_wrong_private_key_fails_decryption():
    keys1 = rsa.generate_keypair()
    keys2 = rsa.generate_keypair()
    ciphertext = rsa.encrypt("secret", keys1["public_key"])
    with pytest.raises(DecryptionError):
        rsa.decrypt(ciphertext, keys2["private_key"])
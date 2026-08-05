import pytest
from core.classical import vigenere
from core.exceptions import InvalidKeyError


def test_encrypt_decrypt_roundtrip():
    text, key = "Attack at dawn", "LEMON"
    encrypted = vigenere.encrypt(text, key)
    assert vigenere.decrypt(encrypted, key) == text


def test_invalid_key_raises():
    with pytest.raises(InvalidKeyError):
        vigenere.encrypt("hello", "")
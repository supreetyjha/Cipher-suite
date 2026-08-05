import pytest
from core.classical import caesar
from core.exceptions import InvalidKeyError


def test_encrypt_basic():
    assert caesar.encrypt("abc", 1) == "bcd"


def test_decrypt_reverses_encrypt():
    text, shift = "Hello, World!", 7
    assert caesar.decrypt(caesar.encrypt(text, shift), shift) == text


def test_invalid_shift_raises():
    with pytest.raises(InvalidKeyError):
        caesar.encrypt("abc", 30)
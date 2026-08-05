import pytest
from core.classical import rail_fence
from core.exceptions import InvalidKeyError


def test_encrypt_decrypt_roundtrip():
    text, rails = "WEAREDISCOVEREDFLEEATONCE", 3
    encrypted = rail_fence.encrypt(text, rails)
    assert rail_fence.decrypt(encrypted, rails) == text


def test_invalid_rails_raises():
    with pytest.raises(InvalidKeyError):
        rail_fence.encrypt("hello", 1)
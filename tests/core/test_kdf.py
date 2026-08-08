import pytest
from core.kdf import derive_key
from core.exceptions import InvalidKeyError


def test_derive_key_returns_key_and_salt():
    result = derive_key("my passphrase")
    assert "key" in result
    assert "salt" in result


def test_same_salt_produces_same_key():
    import base64
    salt = base64.b64decode(derive_key("test")["salt"])
    r1 = derive_key("my passphrase", salt=salt)
    r2 = derive_key("my passphrase", salt=salt)
    assert r1["key"] == r2["key"]


def test_empty_passphrase_raises():
    with pytest.raises(InvalidKeyError):
        derive_key("")
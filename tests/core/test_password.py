import pytest
from core.hashing import password
from core.hashing.password import PasswordVerificationError


def test_hash_and_verify():
    hashed = password.hash_password("correct-horse-battery-staple")
    assert password.verify_password("correct-horse-battery-staple", hashed)


def test_wrong_password_fails_verification():
    hashed = password.hash_password("correct-horse-battery-staple")
    assert not password.verify_password("wrong-password", hashed)


def test_two_hashes_of_same_password_differ():
    # proves salting is happening — same input, different output each time
    h1 = password.hash_password("same-password")
    h2 = password.hash_password("same-password")
    assert h1 != h2


def test_invalid_hash_raises():
    with pytest.raises(PasswordVerificationError):
        password.verify_password("anything", "not-a-real-argon2-hash")
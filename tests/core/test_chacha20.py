import pytest
from core.symmetric import chacha20
from core.exceptions import InvalidKeyError


def test_encrypt_decrypt_roundtrip():
    key = chacha20.generate_key()
    plaintext = "The quick brown fox jumps over the lazy dog."
    encrypted = chacha20.encrypt(plaintext, key)
    decrypted = chacha20.decrypt(encrypted["ciphertext"], key, encrypted["nonce"])
    assert decrypted == plaintext


def test_invalid_key_length_raises():
    with pytest.raises(InvalidKeyError):
        chacha20.encrypt("hello", "short-key")


def test_wrong_key_fails_decryption():
    key1 = chacha20.generate_key()
    key2 = chacha20.generate_key()
    encrypted = chacha20.encrypt("secret", key1)

    # Decrypting with the wrong key produces garbage — either it fails to decode
    # as valid UTF-8 (raises), or it decodes but doesn't match the original.
    # Either outcome proves the wrong key does not recover the plaintext.
    try:
        result = chacha20.decrypt(encrypted["ciphertext"], key2, encrypted["nonce"])
        assert result != "secret"
    except InvalidKeyError:
        pass  # also an acceptable outcome — garbage bytes weren't valid UTF-8
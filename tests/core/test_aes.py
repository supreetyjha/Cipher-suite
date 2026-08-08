import pytest
from core.symmetric import aes
from core.exceptions import InvalidKeyError, DecryptionError


@pytest.mark.parametrize("mode", ["ECB", "CBC", "CFB", "OFB", "GCM"])
def test_encrypt_decrypt_roundtrip(mode):
    key = aes.generate_key()
    plaintext = "Attack at dawn, the eagle has landed."

    encrypted = aes.encrypt(plaintext, key, mode)
    decrypted = aes.decrypt(
        encrypted["ciphertext"], key, mode,
        iv_b64=encrypted["iv"], tag_b64=encrypted["tag"],
    )

    assert decrypted == plaintext


def test_invalid_key_length_raises():
    with pytest.raises(InvalidKeyError):
        aes.encrypt("hello", "short-key", "CBC")


def test_gcm_wrong_tag_fails_verification():
    key = aes.generate_key()
    encrypted = aes.encrypt("secret message", key, "GCM")
    with pytest.raises(DecryptionError):
        aes.decrypt(encrypted["ciphertext"], key, "GCM", iv_b64=encrypted["iv"], tag_b64=aes.generate_key())


def test_ecb_same_plaintext_same_ciphertext_pattern():
    # This is the actual security weakness of ECB — worth having a test that documents it
    key = aes.generate_key()
    block = "AAAAAAAAAAAAAAAA"  # exactly 16 bytes, repeated
    result = aes.encrypt(block + block, key, "ECB")
    import base64
    ct = base64.b64decode(result["ciphertext"])
    # First and second 16-byte blocks should be identical — this is the leak
    assert ct[:16] == ct[16:32]
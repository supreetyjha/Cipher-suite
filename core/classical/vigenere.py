from core.exceptions import InvalidKeyError

ALPHABET_SIZE = 26


def encrypt(plaintext: str, key: str) -> str:
    _validate_key(key)
    return _process(plaintext, key, encrypt_mode=True)


def decrypt(ciphertext: str, key: str) -> str:
    _validate_key(key)
    return _process(ciphertext, key, encrypt_mode=False)


def _validate_key(key: str) -> None:
    if not key or not key.isalpha():
        raise InvalidKeyError("Key must be a non-empty alphabetic string.")


def _process(text: str, key: str, encrypt_mode: bool) -> str:
    key = key.upper()
    result = []
    key_index = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            if not encrypt_mode:
                shift = -shift
            result.append(chr((ord(char) - base + shift) % ALPHABET_SIZE + base))
            key_index += 1
        else:
            result.append(char)

    return "".join(result)
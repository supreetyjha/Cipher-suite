from core.exceptions import InvalidKeyError

ALPHABET_SIZE = 26


def encrypt(plaintext: str, shift: int) -> str:
    if not 0 <= shift <= 25:
        raise InvalidKeyError("Shift must be between 0 and 25.")
    return _shift_text(plaintext, shift)


def decrypt(ciphertext: str, shift: int) -> str:
    if not 0 <= shift <= 25:
        raise InvalidKeyError("Shift must be between 0 and 25.")
    return _shift_text(ciphertext, -shift)


def _shift_text(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % ALPHABET_SIZE + base))
        else:
            result.append(char)
    return "".join(result)
class CipherError(Exception):
    """Base exception for all cipher-suite errors."""


class InvalidKeyError(CipherError):
    """Raised when a key is malformed, wrong length, or invalid for the cipher."""


class UnsupportedModeError(CipherError):
    """Raised when an unsupported cipher mode is requested."""


class DecryptionError(CipherError):
    """Raised when decryption fails (bad padding, auth tag mismatch, etc.)."""
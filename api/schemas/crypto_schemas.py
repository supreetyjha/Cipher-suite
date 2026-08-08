from pydantic import BaseModel, Field



class CaesarRequest(BaseModel):
    text: str = Field(..., min_length=1)
    shift: int = Field(..., ge=0, le=25)


class CaesarResponse(BaseModel):
    result: str


class VigenereRequest(BaseModel):
    text: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)


class VigenereResponse(BaseModel):
    result: str


class PlayfairRequest(BaseModel):
    text: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)


class PlayfairResponse(BaseModel):
    result: str


class RailFenceRequest(BaseModel):
    text: str = Field(..., min_length=1)
    rails: int = Field(..., ge=2, le=20)


class RailFenceResponse(BaseModel):
    result: str


class FrequencyRequest(BaseModel):
    text: str = Field(..., min_length=1)


class FrequencyResponse(BaseModel):
    frequencies: dict[str, float]


class BruteForceRequest(BaseModel):
    text: str = Field(..., min_length=1)


class BruteForceResponse(BaseModel):
    attempts: list[dict]

class HashPasswordRequest(BaseModel):
    password: str = Field(..., min_length=1)


class HashPasswordResponse(BaseModel):
    hashed: str


class VerifyPasswordRequest(BaseModel):
    password: str = Field(..., min_length=1)
    hashed: str = Field(..., min_length=1)


class VerifyPasswordResponse(BaseModel):
    valid: bool


class DigestRequest(BaseModel):
    text: str = Field(..., min_length=1)
    algorithm: str = Field(default="sha256", pattern="^(sha256|sha512)$")


class DigestResponse(BaseModel):
    hash: str


class KDFRequest(BaseModel):
    passphrase: str = Field(..., min_length=1)


class KDFResponse(BaseModel):
    key: str
    salt: str

class AESKeyResponse(BaseModel):
    key: str


class AESEncryptRequest(BaseModel):
    text: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)
    mode: str = Field(..., pattern="^(ECB|CBC|CFB|OFB|GCM)$")


class AESEncryptResponse(BaseModel):
    ciphertext: str
    iv: str | None = None
    tag: str | None = None


class AESDecryptRequest(BaseModel):
    ciphertext: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)
    mode: str = Field(..., pattern="^(ECB|CBC|CFB|OFB|GCM)$")
    iv: str | None = None
    tag: str | None = None


class AESDecryptResponse(BaseModel):
    plaintext: str

class ChaCha20KeyResponse(BaseModel):
    key: str


class ChaCha20EncryptRequest(BaseModel):
    text: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)


class ChaCha20EncryptResponse(BaseModel):
    ciphertext: str
    nonce: str


class ChaCha20DecryptRequest(BaseModel):
    ciphertext: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)
    nonce: str = Field(..., min_length=1)


class ChaCha20DecryptResponse(BaseModel):
    plaintext: str

class RSAKeypairResponse(BaseModel):
    private_key: str
    public_key: str


class RSAEncryptRequest(BaseModel):
    text: str = Field(..., min_length=1)
    public_key: str = Field(..., min_length=1)


class RSAEncryptResponse(BaseModel):
    ciphertext: str


class RSADecryptRequest(BaseModel):
    ciphertext: str = Field(..., min_length=1)
    private_key: str = Field(..., min_length=1)


class RSADecryptResponse(BaseModel):
    plaintext: str


class RSASignRequest(BaseModel):
    message: str = Field(..., min_length=1)
    private_key: str = Field(..., min_length=1)


class RSASignResponse(BaseModel):
    signature: str


class RSAVerifyRequest(BaseModel):
    message: str = Field(..., min_length=1)
    signature: str = Field(..., min_length=1)
    public_key: str = Field(..., min_length=1)


class RSAVerifyResponse(BaseModel):
    valid: bool
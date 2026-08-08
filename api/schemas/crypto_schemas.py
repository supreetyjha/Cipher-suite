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
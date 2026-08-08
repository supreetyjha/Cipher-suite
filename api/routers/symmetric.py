from fastapi import APIRouter, HTTPException
from core.symmetric import aes
from core.exceptions import InvalidKeyError, UnsupportedModeError, DecryptionError
from api.schemas.crypto_schemas import (
    AESKeyResponse, AESEncryptRequest, AESEncryptResponse,
    AESDecryptRequest, AESDecryptResponse,
)

router = APIRouter()


@router.get("/aes/generate-key", response_model=AESKeyResponse)
def generate_aes_key():
    return AESKeyResponse(key=aes.generate_key())


@router.post("/aes/encrypt", response_model=AESEncryptResponse)
def aes_encrypt(payload: AESEncryptRequest):
    try:
        result = aes.encrypt(payload.text, payload.key, payload.mode)
        return AESEncryptResponse(**result)
    except (InvalidKeyError, UnsupportedModeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/aes/decrypt", response_model=AESDecryptResponse)
def aes_decrypt(payload: AESDecryptRequest):
    try:
        plaintext = aes.decrypt(payload.ciphertext, payload.key, payload.mode, payload.iv, payload.tag)
        return AESDecryptResponse(plaintext=plaintext)
    except (InvalidKeyError, UnsupportedModeError, DecryptionError) as e:
        raise HTTPException(status_code=400, detail=str(e))
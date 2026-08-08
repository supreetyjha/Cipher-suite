from fastapi import APIRouter, HTTPException
from core.symmetric import aes, chacha20
from core.exceptions import InvalidKeyError, UnsupportedModeError, DecryptionError
from api.schemas.crypto_schemas import (
    AESKeyResponse, AESEncryptRequest, AESEncryptResponse,
    AESDecryptRequest, AESDecryptResponse,
    ChaCha20KeyResponse, ChaCha20EncryptRequest, ChaCha20EncryptResponse,
    ChaCha20DecryptRequest, ChaCha20DecryptResponse,
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


@router.get("/chacha20/generate-key", response_model=ChaCha20KeyResponse)
def generate_chacha20_key():
    return ChaCha20KeyResponse(key=chacha20.generate_key())


@router.post("/chacha20/encrypt", response_model=ChaCha20EncryptResponse)
def chacha20_encrypt(payload: ChaCha20EncryptRequest):
    try:
        result = chacha20.encrypt(payload.text, payload.key)
        return ChaCha20EncryptResponse(**result)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/chacha20/decrypt", response_model=ChaCha20DecryptResponse)
def chacha20_decrypt(payload: ChaCha20DecryptRequest):
    try:
        plaintext = chacha20.decrypt(payload.ciphertext, payload.key, payload.nonce)
        return ChaCha20DecryptResponse(plaintext=plaintext)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
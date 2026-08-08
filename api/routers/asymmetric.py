from fastapi import APIRouter, HTTPException
from core.asymmetric import rsa
from core.exceptions import InvalidKeyError, DecryptionError
from api.schemas.crypto_schemas import (
    RSAKeypairResponse, RSAEncryptRequest, RSAEncryptResponse,
    RSADecryptRequest, RSADecryptResponse,
    RSASignRequest, RSASignResponse,
    RSAVerifyRequest, RSAVerifyResponse,
)

router = APIRouter()


@router.get("/rsa/generate-keypair", response_model=RSAKeypairResponse)
def generate_rsa_keypair():
    return RSAKeypairResponse(**rsa.generate_keypair())


@router.post("/rsa/encrypt", response_model=RSAEncryptResponse)
def rsa_encrypt(payload: RSAEncryptRequest):
    try:
        ciphertext = rsa.encrypt(payload.text, payload.public_key)
        return RSAEncryptResponse(ciphertext=ciphertext)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rsa/decrypt", response_model=RSADecryptResponse)
def rsa_decrypt(payload: RSADecryptRequest):
    try:
        plaintext = rsa.decrypt(payload.ciphertext, payload.private_key)
        return RSADecryptResponse(plaintext=plaintext)
    except (InvalidKeyError, DecryptionError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rsa/sign", response_model=RSASignResponse)
def rsa_sign(payload: RSASignRequest):
    try:
        signature = rsa.sign(payload.message, payload.private_key)
        return RSASignResponse(signature=signature)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rsa/verify", response_model=RSAVerifyResponse)
def rsa_verify(payload: RSAVerifyRequest):
    try:
        valid = rsa.verify(payload.message, payload.signature, payload.public_key)
        return RSAVerifyResponse(valid=valid)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
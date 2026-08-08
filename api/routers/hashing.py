from fastapi import APIRouter, HTTPException
from core.hashing import password, digest
from core.hashing.password import PasswordVerificationError
from core.kdf import derive_key
from api.schemas.crypto_schemas import (
    HashPasswordRequest, HashPasswordResponse,
    VerifyPasswordRequest, VerifyPasswordResponse,
    DigestRequest, DigestResponse,
    KDFRequest, KDFResponse,
)

router = APIRouter()


@router.post("/password/hash", response_model=HashPasswordResponse)
def hash_password(payload: HashPasswordRequest):
    return HashPasswordResponse(hashed=password.hash_password(payload.password))


@router.post("/password/verify", response_model=VerifyPasswordResponse)
def verify_password(payload: VerifyPasswordRequest):
    try:
        valid = password.verify_password(payload.password, payload.hashed)
        return VerifyPasswordResponse(valid=valid)
    except PasswordVerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/digest", response_model=DigestResponse)
def compute_digest(payload: DigestRequest):
    if payload.algorithm == "sha512":
        return DigestResponse(hash=digest.sha512(payload.text))
    return DigestResponse(hash=digest.sha256(payload.text))


@router.post("/kdf", response_model=KDFResponse)
def key_derivation(payload: KDFRequest):
    result = derive_key(payload.passphrase)
    return KDFResponse(**result)
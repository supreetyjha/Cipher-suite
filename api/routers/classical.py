from fastapi import APIRouter, HTTPException
from core.classical import caesar, vigenere, playfair, rail_fence
from core.exceptions import InvalidKeyError
from api.schemas.crypto_schemas import (
    CaesarRequest, CaesarResponse,
    VigenereRequest, VigenereResponse,
    PlayfairRequest, PlayfairResponse,
    RailFenceRequest, RailFenceResponse,
)

router = APIRouter()


@router.post("/caesar/encrypt", response_model=CaesarResponse)
def caesar_encrypt(payload: CaesarRequest):
    try:
        return CaesarResponse(result=caesar.encrypt(payload.text, payload.shift))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/caesar/decrypt", response_model=CaesarResponse)
def caesar_decrypt(payload: CaesarRequest):
    try:
        return CaesarResponse(result=caesar.decrypt(payload.text, payload.shift))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vigenere/encrypt", response_model=VigenereResponse)
def vigenere_encrypt(payload: VigenereRequest):
    try:
        return VigenereResponse(result=vigenere.encrypt(payload.text, payload.key))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vigenere/decrypt", response_model=VigenereResponse)
def vigenere_decrypt(payload: VigenereRequest):
    try:
        return VigenereResponse(result=vigenere.decrypt(payload.text, payload.key))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/playfair/encrypt", response_model=PlayfairResponse)
def playfair_encrypt(payload: PlayfairRequest):
    try:
        return PlayfairResponse(result=playfair.encrypt(payload.text, payload.key))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/playfair/decrypt", response_model=PlayfairResponse)
def playfair_decrypt(payload: PlayfairRequest):
    try:
        return PlayfairResponse(result=playfair.decrypt(payload.text, payload.key))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/railfence/encrypt", response_model=RailFenceResponse)
def railfence_encrypt(payload: RailFenceRequest):
    try:
        return RailFenceResponse(result=rail_fence.encrypt(payload.text, payload.rails))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/railfence/decrypt", response_model=RailFenceResponse)
def railfence_decrypt(payload: RailFenceRequest):
    try:
        return RailFenceResponse(result=rail_fence.decrypt(payload.text, payload.rails))
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
from fastapi import APIRouter, HTTPException
from core.classical import caesar
from core.exceptions import InvalidKeyError
from api.schemas.crypto_schemas import CaesarRequest, CaesarResponse

router = APIRouter()


@router.post("/caesar/encrypt", response_model=CaesarResponse)
def caesar_encrypt(payload: CaesarRequest):
    try:
        result = caesar.encrypt(payload.text, payload.shift)
        return CaesarResponse(result=result)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/caesar/decrypt", response_model=CaesarResponse)
def caesar_decrypt(payload: CaesarRequest):
    try:
        result = caesar.decrypt(payload.text, payload.shift)
        return CaesarResponse(result=result)
    except InvalidKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
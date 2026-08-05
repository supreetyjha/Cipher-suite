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
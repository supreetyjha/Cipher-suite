from pydantic import BaseModel, Field


class CaesarRequest(BaseModel):
    text: str = Field(..., min_length=1)
    shift: int = Field(..., ge=0, le=25)


class CaesarResponse(BaseModel):
    result: str
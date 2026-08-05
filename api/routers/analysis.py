from fastapi import APIRouter
from core.analysis import frequency, brute_force
from api.schemas.crypto_schemas import (
    FrequencyRequest, FrequencyResponse,
    BruteForceRequest, BruteForceResponse,
)

router = APIRouter()


@router.post("/frequency", response_model=FrequencyResponse)
def frequency_analysis(payload: FrequencyRequest):
    return FrequencyResponse(frequencies=frequency.analyze(payload.text))


@router.post("/bruteforce/caesar", response_model=BruteForceResponse)
def bruteforce_caesar(payload: BruteForceRequest):
    return BruteForceResponse(attempts=brute_force.crack_caesar(payload.text))
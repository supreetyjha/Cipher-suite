from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import classical, symmetric, asymmetric, hashing, analysis

app = FastAPI(title="Cipher Suite API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your deployed frontend URL before shipping
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classical.router, prefix="/classical", tags=["Classical Ciphers"])
app.include_router(symmetric.router, prefix="/symmetric", tags=["Symmetric Encryption"])
app.include_router(asymmetric.router, prefix="/asymmetric", tags=["Asymmetric Encryption"])
app.include_router(hashing.router, prefix="/hashing", tags=["Hashing"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis Tools"])
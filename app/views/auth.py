
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.auth import (
    authenticate,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/login")
async def login(payload: LoginRequest) -> TokenPair:
    if not authenticate(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    return TokenPair(
        access_token=create_access_token(payload.username),
        refresh_token=create_refresh_token(payload.username),
    )


@router.post("/refresh")
async def refresh(payload: RefreshRequest) -> TokenPair:
    subject = decode_refresh_token(payload.refresh_token)
    return TokenPair(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )

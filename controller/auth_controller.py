from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.users import (
    AuthResponse,
    GoogleLoginRequest,
    MobileOtpRequest,
    RefreshTokenRequest,
    Tokens,
    UserPublic,
    VerifyOtpRequest,
)
from service import auth_service


router = APIRouter(prefix="/auth", tags=["Auth"])

bearer_scheme = HTTPBearer(auto_error=False)


@router.post("/otp/request", status_code=204)
async def request_otp(body: MobileOtpRequest):
    try:
        await auth_service.create_and_send_otp(body.mobileNumber)
        return None
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/otp/verify", response_model=AuthResponse)
async def verify_otp(body: VerifyOtpRequest):
    try:
        user, tokens = await auth_service.verify_otp_and_login(body.mobileNumber, body.code, body.name)
        return {
            "user": auth_service.public_user(user),
            "tokens": tokens,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/google", response_model=AuthResponse)
async def google_login(body: GoogleLoginRequest):
    try:
        user, tokens = await auth_service.verify_google_id_token_and_login(body.idToken)
        return {
            "user": auth_service.public_user(user),
            "tokens": tokens,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/refresh", response_model=Tokens)
async def refresh_tokens(body: RefreshTokenRequest):
    try:
        payload = auth_service.verify_and_decode(body.refreshToken, expected_type="refresh")
        user_id = payload.get("sub")
        tokens = auth_service.generate_tokens(user_id)
        return tokens
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.get("/me", response_model=UserPublic)
async def me(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    try:
        payload = auth_service.verify_and_decode(credentials.credentials, expected_type="access")
        user_id = payload.get("sub")
        user = await auth_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return auth_service.public_user(user)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid access token")



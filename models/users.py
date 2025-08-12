from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class MobileOtpRequest(BaseModel):
    mobileNumber: str = Field(..., description="User mobile number in international or local format as string")


class VerifyOtpRequest(BaseModel):
    mobileNumber: str
    code: str
    name: Optional[str] = None


class GoogleLoginRequest(BaseModel):
    idToken: str = Field(..., description="Google ID token obtained from client-side Google Sign-In")


class RefreshTokenRequest(BaseModel):
    refreshToken: str


class UserPublic(BaseModel):
    id: str
    email: Optional[str] = None
    mobileNumber: Optional[str] = None
    name: Optional[str] = None
    photo: Optional[str] = None


class Tokens(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str = "Bearer"
    expiresIn: int


class AuthResponse(BaseModel):
    user: UserPublic
    tokens: Tokens



from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

import jwt
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel
from bson import ObjectId

from db.db_connection import get_collection


class JwtConfig(BaseModel):
    secret_key: str
    issuer: str
    audience: str
    access_ttl_minutes: int = 30
    refresh_ttl_days: int = 30


def get_jwt_config() -> JwtConfig:
    return JwtConfig(
        secret_key=os.getenv("JWT_SECRET", "dev-secret-change"),
        issuer=os.getenv("JWT_ISSUER", "news-app"),
        audience=os.getenv("JWT_AUDIENCE", "news-app-clients"),
        access_ttl_minutes=int(os.getenv("JWT_ACCESS_TTL_MINUTES", "30")),
        refresh_ttl_days=int(os.getenv("JWT_REFRESH_TTL_DAYS", "30")),
    )


def _jwt_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def generate_tokens(user_id: str) -> Dict[str, Any]:
    cfg = get_jwt_config()
    now = _jwt_now()
    access_exp = now + timedelta(minutes=cfg.access_ttl_minutes)
    refresh_exp = now + timedelta(days=cfg.refresh_ttl_days)

    access_payload = {
        "sub": user_id,
        "iss": cfg.issuer,
        "aud": cfg.audience,
        "iat": int(now.timestamp()),
        "exp": int(access_exp.timestamp()),
        "type": "access",
    }
    refresh_payload = {
        "sub": user_id,
        "iss": cfg.issuer,
        "aud": cfg.audience,
        "iat": int(now.timestamp()),
        "exp": int(refresh_exp.timestamp()),
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, cfg.secret_key, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, cfg.secret_key, algorithm="HS256")
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "tokenType": "Bearer",
        "expiresIn": cfg.access_ttl_minutes * 60,
    }


def verify_and_decode(token: str, expected_type: Optional[str] = None) -> Dict[str, Any]:
    cfg = get_jwt_config()
    payload = jwt.decode(
        token,
        cfg.secret_key,
        algorithms=["HS256"],
        audience=cfg.audience,
        issuer=cfg.issuer,
    )
    if expected_type and payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("Unexpected token type")
    return payload


async def find_or_create_user_by_google(google_payload: Dict[str, Any]) -> Dict[str, Any]:
    users = get_collection("users")
    email = google_payload.get("email")
    name = google_payload.get("name") or google_payload.get("given_name")
    picture = google_payload.get("picture")

    existing = await users.find_one({"email": email})
    if existing:
        return existing

    doc = {
        "email": email,
        "name": name,
        "photo": picture,
        "createdAt": _jwt_now(),
        "updatedAt": _jwt_now(),
        "authProviders": ["google"],
    }
    res = await users.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc


async def verify_google_id_token_and_login(id_token_str: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise ValueError("GOOGLE_CLIENT_ID env is required for Google Sign-In")
    request = google_requests.Request()
    payload = google_id_token.verify_oauth2_token(id_token_str, request, audience=client_id)
    # email_verified can be useful
    if not payload.get("email"):
        raise ValueError("Google token does not contain email")
    user = await find_or_create_user_by_google(payload)
    tokens = generate_tokens(str(user["_id"]))
    return user, tokens


async def create_and_send_otp(mobile_number: str) -> None:
    """
    Creates a 6-digit OTP and stores with TTL. In production, integrate with an SMS gateway.
    """
    from random import randint
    otps = get_collection("otps")

    code = f"{randint(100000, 999999)}"
    ttl_seconds = int(os.getenv("OTP_TTL_SECONDS", "300"))
    expires_at = _jwt_now() + timedelta(seconds=ttl_seconds)

    # Upsert latest OTP for this number
    await otps.update_one(
        {"mobileNumber": mobile_number},
        {
            "$set": {
                "mobileNumber": mobile_number,
                "code": code,
                "expiresAt": expires_at,
                "createdAt": _jwt_now(),
            }
        },
        upsert=True,
    )

    # Placeholder for SMS integration
    # In development, we log the code so it's testable via server logs
    print(f"[OTP] {mobile_number} -> {code} (expires in {ttl_seconds}s)")


async def verify_otp_and_login(mobile_number: str, code: str, name: Optional[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    otps = get_collection("otps")
    users = get_collection("users")

    otp_doc = await otps.find_one({"mobileNumber": mobile_number})
    if not otp_doc:
        raise ValueError("OTP not requested or has expired")
    if otp_doc.get("code") != code:
        raise ValueError("Invalid OTP code")
    if otp_doc.get("expiresAt") and otp_doc["expiresAt"] < _jwt_now():
        raise ValueError("OTP expired")

    # Find or create user by mobile
    existing = await users.find_one({"mobileNumber": mobile_number})
    if existing:
        user = existing
    else:
        doc = {
            "mobileNumber": mobile_number,
            "name": name,
            "createdAt": _jwt_now(),
            "updatedAt": _jwt_now(),
            "authProviders": ["otp"],
        }
        res = await users.insert_one(doc)
        doc["_id"] = res.inserted_id
        user = doc

    tokens = generate_tokens(str(user["_id"]))
    # Optionally, invalidate OTP after successful use to prevent reuse
    await otps.delete_one({"mobileNumber": mobile_number})
    return user, tokens


def public_user(user_doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(user_doc.get("_id")),
        "email": user_doc.get("email"),
        "mobileNumber": user_doc.get("mobileNumber"),
        "name": user_doc.get("name"),
        "photo": user_doc.get("photo"),
    }


async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    users = get_collection("users")
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        return None
    user = await users.find_one({"_id": obj_id})
    return user



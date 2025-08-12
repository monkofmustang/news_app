from __future__ import annotations

import os
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

load_dotenv()

_MONGO_URI: str = os.getenv("DB_CONNECTION", "mongodb://localhost:27017")
_DB_NAME: str = os.getenv("DB_NAME", "news")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(_MONGO_URI)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        _db = get_client()[_DB_NAME]
    return _db


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return get_database()[collection_name]


async def init_indexes() -> None:
    """
    Ensure required MongoDB indexes exist (idempotent).
    - users: unique indexes on email and mobileNumber (sparse since either can be null)
    - otps: TTL index on expiresAt
    """
    db = get_database()

    users = db["users"]
    # Unique on email if present
    await users.create_index("email", unique=True, sparse=True, name="uniq_email")
    # Unique on mobileNumber if present
    await users.create_index("mobileNumber", unique=True, sparse=True, name="uniq_mobile")

    otps = db["otps"]
    # TTL: expire documents when expiresAt has passed
    # expireAfterSeconds=0 means expire as soon as the time in the field is older than now
    await otps.create_index("expiresAt", expireAfterSeconds=0, name="ttl_expires_at")


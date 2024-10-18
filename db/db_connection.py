from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(
    os.getenv("DB_CONNECTION")
)
db = client["news"]


def get_collection(collection_name: str):
    return db[collection_name]

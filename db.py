# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

_MONGO_URL = os.environ["MONGODB_URL"]
_DB_NAME = os.environ["DB_NAME"]

_client = AsyncIOMotorClient(_MONGO_URL)
db = _client[_DB_NAME]

def close_db():
    _client.close()

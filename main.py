from fastapi import FastAPI
from routes import router
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from db import close_db

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(title="User Service")

app.include_router(router, prefix="/users")

@app.on_event("shutdown")
async def shutdown_db_client():
    close_db()

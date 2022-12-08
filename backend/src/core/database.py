from src.core.config import settings
import certifi
import asyncio
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING,tlsCAFile=certifi.where())
db = client.unveil
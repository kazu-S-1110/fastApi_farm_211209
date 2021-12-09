import collections
from decouple import config
import motor.motor_asyncio

MONGO_API_KEY = config("MONGO_API_KEY")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collection_todo = database.todo
collection_user = database.user


async def db_create_todo(data: dict) -> dict:
    todo = await collection_todo.insert_one(data)

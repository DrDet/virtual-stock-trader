import auth.database as db

from auth.endpoints._crypto_context import get_password_hash
from common.user_data import UserInDB


async def register(username: str, password: str):
    user = UserInDB(username=username, hashed_password=get_password_hash(password))
    return await db.create_user(user)

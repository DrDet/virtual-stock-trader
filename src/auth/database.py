import databases
import sqlalchemy
from sqlalchemy.dialects.mysql import insert
from fastapi import HTTPException

from common.user_data import UserInDB

__database = None
__users = None


async def prepare_database(db_connect_url):
    global __database, __users

    __database = databases.Database(db_connect_url)
    metadata = sqlalchemy.MetaData()
    engine = sqlalchemy.create_engine(
        db_connect_url
    )
    __users = sqlalchemy.Table("Users", metadata, autoload_with=engine)

    await __database.connect()


async def finalize_database():
    global __database

    await __database.disconnect()


async def create_user(user: UserInDB):
    global __database, __users
    try:
        req = insert(__users).values(username=user.username, hashed_password=user.hashed_password)
        resp = await __database.fetch_one(req)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    return resp


async def get_user(username: str):
    global __database, __users
    try:
        req = __users.select(whereclause=__users.c.username == username)
        resp = await __database.fetch_one(req)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    if resp is None:
        raise HTTPException(status_code=404, detail=f"Can't find user with name {username}")
    return UserInDB(username=resp.username, hashed_password=resp.hashed_password)

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import auth.database as db
from auth.endpoints._crypto_context import SECRET_KEY, ALGORITHM
from auth.token_data import TokenData

async def get_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_user_by_token(token: str):
    return await get_user(token)
    return await db.get_user(token)

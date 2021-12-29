import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from common.user_data import UserInDB

AUTHORIZATION_SERVICE_URL = 'http://localhost:8001'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_authorized_user(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient(timeout=httpx.Timeout(2, connect=10)) as client:
        resp = await client.get(f'{AUTHORIZATION_SERVICE_URL}/get_user_by_token', params = {'token': token})
    if resp.status_code == httpx.codes.OK:
        return UserInDB(**resp.json())
    if resp.status_code == httpx.codes.UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    raise HTTPException(
        status_code=resp.status,
        detail=f"Can't get current user, got: {resp.text}"
    )

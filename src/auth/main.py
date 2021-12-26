from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from auth.data import *
from auth.endpoints.login import login_for_access_token
from auth.endpoints.get_user_by_token import get_user_by_token, get_user


app = FastAPI()

@app.post("/token", response_model=Token)
async def act_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(form_data)

@app.get("/get_user_by_token")
async def act_get_user_by_token(token: str):
    return await get_user_by_token(token)


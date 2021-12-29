from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

import auth.database as db
from auth.token_data import Token
from auth.endpoints.login import login_for_access_token
from auth.endpoints.get_user_by_token import get_user_by_token, get_user
from auth.endpoints.register import register


app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.prepare_database("mysql+pymysql://vstrader_users_client@localhost:3306/vstrader_users")


@app.on_event("shutdown")
async def shutdown():
    await db.finalize_database()


@app.post("/token", response_model=Token)
async def act_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(form_data)

@app.get("/get_user_by_token")
async def act_get_user_by_token(token: str):
    return await get_user_by_token(token)

@app.post("/register")
async def act_register(username: str, password: str):
    return await register(username, password)

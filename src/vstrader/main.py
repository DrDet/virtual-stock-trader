from fastapi import FastAPI, Depends

from common.auth_checker import get_authorized_user
from common.user_data import User
import vstrader.database as db
from vstrader.endpoints import *
from vstrader.gql.endpoints import graphql_app

app = FastAPI()


@app.on_event("startup")
async def startup():
    db.prepare_database("mysql+pymysql://vstrader_portfolios_client@localhost:3306/vstrader_portfolios")
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/portfolio")
async def act_get_portfolio(user: User = Depends(get_authorized_user)):
    res = await db.database.fetch_all(db.portfolios.select())
    return await get_portfolio(user.username)


@app.get("/portfolio/deposit")
async def act_deposit(units_cnt: float, user: User = Depends(get_authorized_user)):
    return await deposit(user.username, units_cnt)


@app.get("/stocks")
async def act_get_stock_info(ticker: str):
    return await get_stock_info(ticker)


@app.post("/trading/{operation_type}")
async def act_perform_trading(operation_type: OperationType, trade_offer: TradeOffer, user: User = Depends(get_authorized_user)):
    return await perform_trading(user.username, operation_type, trade_offer)

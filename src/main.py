from fastapi import FastAPI

import vstrader.database as db
from vstrader.endpoints import *
from vstrader.gql.endpoints import graphql_app

app = FastAPI()


@app.on_event("startup")
async def startup():
    db.prepare_database("mysql+pymysql://vstrader_client@localhost:3306/vstrader")
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/portfolio/deposit")
async def act_deposit(user_id: int, units_cnt: float):
    return await deposit(user_id, units_cnt)


@app.get("/portfolio")
async def act_get_portfolio(user_id: int):
    res = await db.database.fetch_all(db.portfolios.select())
    return await get_portfolio(user_id)


@app.get("/stocks")
async def act_get_stock_info(ticker: str):
    return await get_stock_info(ticker)


@app.post("/trading/{operation_type}")
async def act_perform_trading(user_id: int, operation_type: OperationType, trade_offer: TradeOffer):
    return await perform_trading(user_id, operation_type, trade_offer)

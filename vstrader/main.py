from fastapi import FastAPI

from vstrader.endpoints import *
from vstrader.gql.endpoints import graphql_app
from vstrader.database import *

app = FastAPI()

prepare_database("mysql+pymysql://vstrader_client@localhost:3306/vstrader")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/portfolio/deposit")
async def act_deposit(user_id: int, units_cnt: float):
    return await deposit(user_id, units_cnt)


@app.get("/portfolio")
async def act_get_portfolio(user_id: int):
    res = await database.fetch_all(portfolios.select())
    print(res[0].balance)
    return await get_portfolio(user_id)


@app.get("/stocks")
async def act_get_stock_info(ticker: str):
    return await get_stock_info(ticker)


@app.post("/trading/{operation_type}")
async def act_perform_trading(user_id: int, operation_type: OperationType, trade_offer: TradeOffer):
    return await perform_trading(user_id, operation_type, trade_offer)

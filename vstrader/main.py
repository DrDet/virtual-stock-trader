from fastapi import FastAPI

from vstrader.endpoints import *

app = FastAPI()


@app.get("/portfolio")
async def act_get_portfolio():
    return await get_portfolio()


@app.get("/stocks")
async def act_get_stock_info(ticker: str):
    return await get_stock_info(ticker)


@app.post("/trading/{operation_type}")
async def act_perform_trading(operation_type: OperationType, trade_offer: TradeOffer):
    return await perform_trading(operation_type, trade_offer)
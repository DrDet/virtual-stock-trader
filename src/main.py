from fastapi import FastAPI, HTTPException
from enum import Enum

from data import *
import portfolio_manager
import moex_client

app = FastAPI()
fake_user_id = 42


@app.get("/portfolio")
async def get_portfolio():
    return await portfolio_manager.load_portfolio(fake_user_id)


@app.get("/stocks")
async def get_stock_info(ticker: str):
    stock_info = await moex_client.load_stock_info(ticker)
    if stock_info is None:
        raise HTTPException(status_code=404, detail=f"Can't find stock with ticker {ticker}")
    return stock_info


class OperationType(str, Enum):
    BUY = 'buy'
    SELL = 'sell'


@app.post("/trading/{operation_type}")
async def perform_trading(operation_type: OperationType, trade_offer: TradeOffer):
    stock_info = await moex_client.load_stock_info(trade_offer.ticker)
    if stock_info is None:
        raise HTTPException(status_code=404, detail=f"Can't find stock with ticker {trade_offer.ticker}")

    if operation_type == OperationType.BUY:
        return await portfolio_manager.trading_buy(fake_user_id, trade_offer, stock_info)
    else:
        return await portfolio_manager.trading_sell(fake_user_id, trade_offer, stock_info)

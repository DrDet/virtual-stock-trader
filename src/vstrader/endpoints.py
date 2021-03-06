from fastapi import HTTPException

from vstrader import portfolio_manager
from vstrader import moex_client
from vstrader.data import *


async def deposit(username: str, units_cnt: float):
    await portfolio_manager.deposit(username, units_cnt)
    return await portfolio_manager.load_portfolio(username)


async def get_portfolio(username: str):
    return await portfolio_manager.load_portfolio(username)


async def get_stock_info(ticker: str):
    stock_info = await moex_client.load_stock_info(ticker)
    if stock_info is None:
        raise HTTPException(status_code=404, detail=f"Can't find stock with ticker {ticker}")
    return stock_info


async def perform_trading(username: str, operation_type: OperationType, trade_offer: TradeOffer):
    stock_info = await moex_client.load_stock_info(trade_offer.ticker)
    if stock_info is None:
        raise HTTPException(status_code=404, detail=f"Can't find stock with ticker {trade_offer.ticker}")

    if operation_type == OperationType.BUY:
        return await portfolio_manager.trading_buy(username, trade_offer, stock_info)
    else:
        return await portfolio_manager.trading_sell(username, trade_offer, stock_info)

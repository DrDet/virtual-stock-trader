from fastapi import HTTPException

from vstrader import portfolio_manager
from vstrader import moex_client
from vstrader.data import *

fake_user_id = 42


async def get_portfolio():
    return await portfolio_manager.load_portfolio(fake_user_id)


async def get_stock_info(ticker: str):
    stock_info = await moex_client.load_stock_info(ticker)
    if stock_info is None:
        raise HTTPException(status_code=404, detail=f"Can't find stock with ticker {ticker}")
    return stock_info


async def perform_trading(operation_type: OperationType, trade_offer: TradeOffer):
    stock_info = await moex_client.load_stock_info(trade_offer.ticker)
    if stock_info is None:
        raise HTTPException(status_code=404, detail=f"Can't find stock with ticker {trade_offer.ticker}")

    if operation_type == OperationType.BUY:
        return await portfolio_manager.trading_buy(fake_user_id, trade_offer, stock_info)
    else:
        return await portfolio_manager.trading_sell(fake_user_id, trade_offer, stock_info)

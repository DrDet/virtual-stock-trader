from fastapi import HTTPException

from vstrader.data import *
from vstrader import moex_client


async def load_portfolio(user_id: int):
    return Portfolio(balance_rub=10000, positions={
        'SBER': StockPosition(stock_info=await moex_client.load_stock_info('SBER'), average_price=200, count=5),
        'GAZP': StockPosition(stock_info=await moex_client.load_stock_info('GAZP'), average_price=250, count=10),
        'YNDX': StockPosition(stock_info=await moex_client.load_stock_info('YNDX'), average_price=4000, count=10),
    })


async def trading_buy(user_id: int, trade_offer: TradeOffer, stock_info: StockInfo):
    portfolio = await load_portfolio(user_id)
    if portfolio.balance_rub < stock_info.price * trade_offer.count:
        raise HTTPException(status_code=422, detail=f"Can't buy {trade_offer.ticker}: not enough money")
    if trade_offer.price < stock_info.price:
        raise HTTPException(status_code=422,
                            detail=f"Can't buy {trade_offer.ticker}:"
                                   f" asked price {trade_offer.price} < current asset price {stock_info.price}")
    portfolio.update_buy(stock_info, trade_offer)
    return portfolio


async def trading_sell(user_id: int, trade_offer: TradeOffer, stock_info: StockInfo):
    portfolio = await load_portfolio(user_id)
    stock_position = portfolio.positions.get(trade_offer.ticker)
    if stock_position is None:
        raise HTTPException(status_code=422,
                            detail=f"Can't sell {trade_offer.ticker}: you don't have open positions at the asset")
    if trade_offer.count > stock_position.count:
        raise HTTPException(status_code=422,
                            detail=f"Can't sell {trade_offer.ticker}: you don't have enough assets in portfolio")
    if trade_offer.price > stock_info.price:
        raise HTTPException(status_code=422,
                            detail=f"Can't sell {trade_offer.ticker}:"
                                   f"asked price {trade_offer.price} > current asset price {stock_info.price}")

    portfolio.update_sell(trade_offer)
    return portfolio

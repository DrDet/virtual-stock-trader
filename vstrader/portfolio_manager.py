from fastapi import HTTPException
from sqlalchemy.dialects.mysql import insert

from vstrader.data import *
from vstrader import moex_client
import vstrader.database as db


async def load_portfolio(user_id: int):
    get_portfolio_balance_req = db.portfolios.select(whereclause=db.portfolios.c.portfolio_id == user_id)
    get_portfolio_balance_resp = await db.database.fetch_one(get_portfolio_balance_req)
    if get_portfolio_balance_resp is None:
        raise HTTPException(status_code=404, detail=f"Can't find user with id {user_id}")
    balance_rub = get_portfolio_balance_resp.balance

    get_stock_positions_req = db.stock_positions.select(whereclause=db.stock_positions.c.portfolio_id == user_id)
    get_stock_positions_resp = await db.database.fetch_all(get_stock_positions_req)
    positions = {}
    for row in get_stock_positions_resp:
        ticker = row.ticker
        stock_info = await moex_client.load_stock_info(ticker)
        positions[ticker] = StockPosition(stock_info=stock_info, average_price=row.average_price, count=row.count)

    return Portfolio(balance_rub=balance_rub, positions=positions)


async def _update_balance(user_id: int, new_balance: float):
    update_balance_req = db.portfolios.update(whereclause=db.portfolios.c.portfolio_id == user_id).values(balance=new_balance)
    await db.database.fetch_one(update_balance_req)


async def _update_stock_position(user_id: int, stock_position: StockPosition):
    update_stock_pos_req = insert(db.stock_positions) \
        .values(portfolio_id=user_id, ticker=stock_position.stock_info.ticker, count=stock_position.count, average_price=stock_position.average_price) \
        .on_duplicate_key_update(count=stock_position.count, average_price=stock_position.average_price)
    await db.database.fetch_one(update_stock_pos_req)


async def deposit(user_id: int, units_cnt: float):
    deposit_req = insert(db.portfolios) \
        .values(portfolio_id=user_id, balance=units_cnt) \
        .on_duplicate_key_update(balance=db.portfolios.c.balance + units_cnt)
    await db.database.fetch_one(deposit_req)


async def trading_buy(user_id: int, trade_offer: TradeOffer, stock_info: StockInfo):
    portfolio = await load_portfolio(user_id)
    if portfolio.balance_rub < stock_info.price * trade_offer.count:
        raise HTTPException(status_code=422, detail=f"Can't buy {trade_offer.ticker}: not enough money")
    if trade_offer.price < stock_info.price:
        raise HTTPException(status_code=422,
                            detail=f"Can't buy {trade_offer.ticker}:"
                                   f" asked price {trade_offer.price} < current asset price {stock_info.price}")
    portfolio.update_buy(stock_info, trade_offer)
    await _update_balance(user_id, portfolio.balance_rub)
    await _update_stock_position(user_id, portfolio.positions[stock_info.ticker])
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
    await _update_balance(user_id, portfolio.balance_rub)
    await _update_stock_position(user_id, portfolio.positions[stock_info.ticker])
    return portfolio

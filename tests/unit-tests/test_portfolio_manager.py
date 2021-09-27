import pytest
from fastapi import HTTPException
from unittest.mock import patch

from vstrader import portfolio_manager
from vstrader.data import *

fake_user_id = 42


@pytest.fixture
def stock_info():
    return StockInfo(ticker='TEST', price=10)


@pytest.fixture
def stock_positions(stock_info):
    return {'TEST': StockPosition(stock_info=stock_info, average_price=10, count=10)}


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_buy_basic(mocked_load_portfolio, stock_info, stock_positions):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=100, positions={})

    portfolio = await portfolio_manager.trading_buy(fake_user_id, TradeOffer(ticker='TEST', price=10, count=10),
                                                    stock_info)
    assert portfolio.balance_rub == 0
    assert portfolio.positions == stock_positions


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_buy_not_enough_money(mocked_load_portfolio, stock_info):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=100, positions={})

    with pytest.raises(HTTPException) as exc:
        await portfolio_manager.trading_buy(fake_user_id, TradeOffer(ticker='TEST', price=10, count=11), stock_info)
    assert exc.value.status_code == 422
    assert 'not enough money' in exc.value.detail


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_buy_invalid_offer(mocked_load_portfolio, stock_info):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=100, positions={})

    with pytest.raises(HTTPException) as exc:
        await portfolio_manager.trading_buy(fake_user_id, TradeOffer(ticker='TEST', price=9, count=10), stock_info)
    assert exc.value.status_code == 422


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_sell_basic(mocked_load_portfolio, stock_info, stock_positions):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=0, positions=stock_positions)

    offer = TradeOffer(ticker='TEST', price=10, count=10)
    portfolio = await portfolio_manager.trading_sell(fake_user_id, offer, stock_info)
    assert portfolio.balance_rub == offer.total_price
    assert portfolio.positions == {'TEST': StockPosition(stock_info=stock_info, average_price=10, count=0)}


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_sell_no_positions(mocked_load_portfolio, stock_info, stock_positions):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=0, positions=stock_positions)

    with pytest.raises(HTTPException) as exc:
        await portfolio_manager.trading_sell(fake_user_id, TradeOffer(ticker='QWER', price=10, count=10), stock_info)
    assert exc.value.status_code == 422
    assert "you don't have open positions at the asset" in exc.value.detail


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_sell_not_enough_positions(mocked_load_portfolio, stock_info, stock_positions):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=0, positions=stock_positions)

    with pytest.raises(HTTPException) as exc:
        await portfolio_manager.trading_sell(fake_user_id, TradeOffer(ticker='TEST', price=10, count=11), stock_info)
    assert exc.value.status_code == 422
    assert "you don't have enough assets in portfolio" in exc.value.detail


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_sell_invalid_offer(mocked_load_portfolio, stock_info, stock_positions):
    mocked_load_portfolio.return_value = Portfolio(balance_rub=0, positions=stock_positions)

    with pytest.raises(HTTPException) as exc:
        await portfolio_manager.trading_sell(fake_user_id, TradeOffer(ticker='TEST', price=11, count=10), stock_info)
    assert exc.value.status_code == 422

import pytest
from unittest.mock import patch

from vstrader.endpoints import *
from vstrader import moex_client


@pytest.mark.asyncio
async def test_get_portfolio():
    portfolio = await get_portfolio()
    for ticker, pos in portfolio.positions.items():
        assert pos.count >= 0
        assert pos.stock_info.price > 0


@pytest.mark.asyncio
async def test_get_stock_info_basic():
    stock_info = await get_stock_info('SBER')
    assert stock_info.ticker == 'SBER'
    assert stock_info.price > 0


@pytest.mark.asyncio
async def test_get_stock_info_invalid_ticker():
    with pytest.raises(HTTPException) as exc:
        await get_stock_info('hello')
    assert exc.value.status_code == 404
    assert "Can't find stock with ticker" in exc.value.detail


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_perform_trading_buy_basic(mocked_load_portfolio):
    start_balance = 100000000
    mocked_load_portfolio.return_value = Portfolio(balance_rub=start_balance, positions={})
    stock_info = await moex_client.load_stock_info('SBER')
    offer = TradeOffer(ticker=stock_info.ticker, price=stock_info.price * 1.1, count=10)
    portfolio = await perform_trading(OperationType.BUY, offer)
    assert portfolio.balance_rub == start_balance - offer.total_price
    assert stock_info.ticker in portfolio.positions
    assert portfolio.positions[stock_info.ticker].count >= 10


@pytest.mark.asyncio
@patch.object(portfolio_manager, 'load_portfolio')
async def test_perform_trading_sell_basic(mocked_load_portfolio):
    stock_info = await moex_client.load_stock_info('SBER')
    start_count = 10
    mocked_load_portfolio.return_value = \
        Portfolio(balance_rub=0,
                  positions={stock_info.ticker: StockPosition(stock_info=stock_info,
                                                              average_price=stock_info.price,
                                                              count=start_count)})
    offer = TradeOffer(ticker=stock_info.ticker, price=stock_info.price * 0.9, count=6)
    portfolio = await perform_trading(OperationType.SELL, offer)
    assert portfolio.balance_rub == offer.total_price
    assert portfolio.positions[stock_info.ticker].count == start_count - offer.count


@pytest.mark.asyncio
async def test_perform_trading_invalid_ticker():
    with pytest.raises(HTTPException) as exc:
        await perform_trading(OperationType.BUY, TradeOffer(ticker='hello', price=10, count=10))
    assert exc.value.status_code == 404
    assert "Can't find stock with ticker" in exc.value.detail

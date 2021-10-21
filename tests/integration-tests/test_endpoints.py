import pytest
from unittest.mock import patch

from vstrader.endpoints import *
from vstrader import moex_client
from vstrader import database

from pytest_mysql import factories

mysql_my_proc = factories.mysql_proc()
mysql_my = factories.mysql('mysql_my_proc')


@pytest.fixture(scope='function')
async def setup_db(mysql, mysql_proc):
    cursor = mysql.cursor()

    cursor.execute(
        '''
        CREATE TABLE Portfolios
        (
            portfolio_id BIGINT NOT NULL,
            balance DOUBLE NOT NULL,
            PRIMARY KEY (portfolio_id)
        );
        CREATE TABLE StockPositions
        (
            portfolio_id BIGINT NOT NULL,
            ticker VARCHAR(20) NOT NULL,
            count INT NOT NULL,
            average_price DOUBLE NOT NULL,
            PRIMARY KEY (portfolio_id, ticker)
        );
        '''
    )
    cursor.fetchall()
    cursor.close()

    database.prepare_database(f"mysql+pymysql://root@localhost:{mysql_proc.port}/test")
    await database.database.connect()
    yield
    await database.database.disconnect()


@pytest.mark.asyncio
async def test_get_portfolio(setup_db):
    await deposit(1, 1000)
    portfolio = await get_portfolio(1)
    assert portfolio.balance_rub == 1000


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
async def test_perform_trading_buy_basic(setup_db):
    start_balance = 100000000
    await deposit(1, start_balance)
    stock_info = await moex_client.load_stock_info('SBER')
    offer = TradeOffer(ticker=stock_info.ticker, price=stock_info.price * 1.1, count=10)
    portfolio = await perform_trading(1, OperationType.BUY, offer)
    assert portfolio.balance_rub == start_balance - offer.total_price
    assert stock_info.ticker in portfolio.positions
    assert portfolio.positions[stock_info.ticker].count >= 10


@pytest.mark.asyncio
async def test_perform_trading_sell_basic(setup_db):
    stock_info = await moex_client.load_stock_info('SBER')
    start_balance = 1000000
    await deposit(1, start_balance)

    offer = TradeOffer(ticker=stock_info.ticker, price=stock_info.price * 1.1, count=15)
    await perform_trading(1, OperationType.BUY, offer)

    offer = TradeOffer(ticker=stock_info.ticker, price=stock_info.price * 0.9, count=10)
    portfolio = await perform_trading(1, OperationType.SELL, offer)

    assert portfolio.balance_rub != start_balance
    assert portfolio.positions[stock_info.ticker].count == 5


@pytest.mark.asyncio
async def test_perform_trading_invalid_ticker(setup_db):
    with pytest.raises(HTTPException) as exc:
        await perform_trading(1, OperationType.BUY, TradeOffer(ticker='hello', price=10, count=10))
    assert exc.value.status_code == 404
    assert "Can't find stock with ticker" in exc.value.detail

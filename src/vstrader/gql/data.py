import strawberry
from typing import List

from vstrader import data


@strawberry.type
class StockInfo:
    ticker: str
    price: float

    def __init__(self, stock_info: data.StockInfo):
        self.ticker = stock_info.ticker
        self.price = stock_info.price


@strawberry.type
class StockPosition:
    stock_info: StockInfo
    average_price: float
    count: int

    def __init__(self, stock_pos: data.StockPosition):
        self.stock_info = StockInfo(stock_pos.stock_info)
        self.average_price = stock_pos.average_price
        self.count = stock_pos.count


@strawberry.type
class Portfolio:
    balance: float
    positions: List[StockPosition]

    def __init__(self, portfolio: data.Portfolio):
        self.balance = portfolio.balance_rub
        self.positions = list(portfolio.positions.values())

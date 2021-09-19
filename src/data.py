from pydantic import BaseModel
from typing import Dict


class StockInfo(BaseModel):
    ticker: str
    price: float


class TradeOffer(BaseModel):
    ticker: str
    price: float
    count: int

    @property
    def total_price(self):
        return self.price * self.count


class StockPosition(BaseModel):
    stock_info: StockInfo
    average_price: float
    count: int

    @property
    def total_price(self):
        return self.average_price * self.count

    def update_buy(self, trade_offer: TradeOffer):
        self.count += trade_offer.count
        self.average_price = (self.total_price + trade_offer.total_price) / self.count

    def update_sell(self, trade_offer: TradeOffer):
        self.count -= trade_offer.count


class Portfolio(BaseModel):
    balance_rub: float
    positions: Dict[str, StockPosition]

    def update_buy(self, stock_info: StockInfo, trade_offer: TradeOffer):
        position = self.positions.setdefault(trade_offer.ticker, StockPosition(stock_info=stock_info,
                                                                               average_price=0,
                                                                               count=0))
        self.balance_rub -= trade_offer.total_price
        position.update_buy(trade_offer)

    def update_sell(self, trade_offer: TradeOffer):
        position = self.positions.get(trade_offer.ticker)
        position.update_sell(trade_offer)
        self.balance_rub += trade_offer.total_price

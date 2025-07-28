"""
Observer Pattern - Defines one-to-many dependency between objects
Common interview question: Stock price updates, Newsletter subscriptions
"""

from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass


class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)


class Stock(Subject):
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self._symbol = symbol
        self._price = price
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price: float):
        self._price = price
        self.notify()
    
    @property
    def symbol(self):
        return self._symbol


class StockDisplay(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, stock: Stock):
        print(f"{self.name}: {stock.symbol} is now ${stock.price}")


# Usage example
if __name__ == "__main__":
    apple_stock = Stock("AAPL", 150.0)
    
    display1 = StockDisplay("Portfolio App")
    display2 = StockDisplay("Trading Dashboard")
    
    apple_stock.attach(display1)
    apple_stock.attach(display2)
    
    apple_stock.price = 155.0  # Both displays get notified
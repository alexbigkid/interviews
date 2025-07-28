"""
Decorator Pattern - Adds behavior to objects dynamically
Common interview question: Coffee shop ordering, Text formatting
"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass


class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0
    
    def description(self) -> str:
        return "Simple Coffee"


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()
    
    def description(self) -> str:
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5
    
    def description(self) -> str:
        return self._coffee.description() + ", Milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2
    
    def description(self) -> str:
        return self._coffee.description() + ", Sugar"


class WhipDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.7
    
    def description(self) -> str:
        return self._coffee.description() + ", Whip"


# Usage example
if __name__ == "__main__":
    # Start with simple coffee
    coffee = SimpleCoffee()
    print(f"{coffee.description()}: ${coffee.cost()}")
    
    # Add milk
    coffee = MilkDecorator(coffee)
    print(f"{coffee.description()}: ${coffee.cost()}")
    
    # Add sugar
    coffee = SugarDecorator(coffee)
    print(f"{coffee.description()}: ${coffee.cost()}")
    
    # Add whip
    coffee = WhipDecorator(coffee)
    print(f"{coffee.description()}: ${coffee.cost()}")
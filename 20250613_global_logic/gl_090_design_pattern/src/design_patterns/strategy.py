"""
Strategy Pattern - Defines family of algorithms and makes them interchangeable
Common interview question: Payment processing, Sorting algorithms
"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
    
    def pay(self, amount: float):
        return f"Paid ${amount} using Credit Card ending in {self.card_number[-4:]}"


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float):
        return f"Paid ${amount} using PayPal account {self.email}"


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
    
    def pay(self, amount: float):
        return f"Paid ${amount} using Crypto wallet {self.wallet_address[:8]}..."


class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item: str, price: float):
        self.items.append((item, price))
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(price for _, price in self.items)
        if self.payment_strategy:
            return self.payment_strategy.pay(total)
        return "No payment method selected"


# Usage example
if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)
    
    # Pay with credit card
    cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
    print(cart.checkout())
    
    # Switch to PayPal
    cart.set_payment_strategy(PayPalPayment("user@example.com"))
    print(cart.checkout())
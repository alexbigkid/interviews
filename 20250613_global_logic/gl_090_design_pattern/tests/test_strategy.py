import unittest
from src.design_patterns.strategy import (
    ShoppingCart, CreditCardPayment, PayPalPayment, CryptoPayment
)


class TestStrategy(unittest.TestCase):
    
    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("Laptop", 999.99)
        self.cart.add_item("Mouse", 29.99)
    
    def test_credit_card_payment(self):
        """Test credit card payment strategy"""
        strategy = CreditCardPayment("1234567890123456")
        self.cart.set_payment_strategy(strategy)
        
        result = self.cart.checkout()
        self.assertIn("Paid $1029.98 using Credit Card ending in 3456", result)
    
    def test_paypal_payment(self):
        """Test PayPal payment strategy"""
        strategy = PayPalPayment("user@example.com")
        self.cart.set_payment_strategy(strategy)
        
        result = self.cart.checkout()
        self.assertIn("Paid $1029.98 using PayPal account user@example.com", result)
    
    def test_crypto_payment(self):
        """Test crypto payment strategy"""
        strategy = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        self.cart.set_payment_strategy(strategy)
        
        result = self.cart.checkout()
        self.assertIn("Paid $1029.98 using Crypto wallet 1A1zP1eP...", result)
    
    def test_no_payment_strategy(self):
        """Test checkout without setting payment strategy"""
        result = self.cart.checkout()
        self.assertEqual(result, "No payment method selected")
    
    def test_switch_payment_strategy(self):
        """Test switching between different payment strategies"""
        # Start with credit card
        credit_card = CreditCardPayment("1111222233334444")
        self.cart.set_payment_strategy(credit_card)
        result1 = self.cart.checkout()
        self.assertIn("Credit Card ending in 4444", result1)
        
        # Switch to PayPal
        paypal = PayPalPayment("test@test.com")
        self.cart.set_payment_strategy(paypal)
        result2 = self.cart.checkout()
        self.assertIn("PayPal account test@test.com", result2)
    
    def test_cart_total_calculation(self):
        """Test that cart calculates total correctly"""
        empty_cart = ShoppingCart()
        empty_cart.add_item("Item1", 10.50)
        empty_cart.add_item("Item2", 5.25)
        
        strategy = CreditCardPayment("1111111111111111")
        empty_cart.set_payment_strategy(strategy)
        
        result = empty_cart.checkout()
        self.assertIn("$15.75", result)
    
    def test_empty_cart(self):
        """Test checkout with empty cart"""
        empty_cart = ShoppingCart()
        strategy = PayPalPayment("empty@cart.com")
        empty_cart.set_payment_strategy(strategy)
        
        result = empty_cart.checkout()
        self.assertIn("$0", result)


if __name__ == '__main__':
    unittest.main()
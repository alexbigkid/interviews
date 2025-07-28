import unittest
from io import StringIO
import sys
from src.design_patterns.observer import Stock, StockDisplay


class TestObserver(unittest.TestCase):
    
    def setUp(self):
        self.stock = Stock("AAPL", 150.0)
        self.display1 = StockDisplay("Portfolio App")
        self.display2 = StockDisplay("Trading Dashboard")
    
    def test_attach_observer(self):
        """Test attaching observers to subject"""
        self.stock.attach(self.display1)
        self.assertEqual(len(self.stock._observers), 1)
        
        self.stock.attach(self.display2)
        self.assertEqual(len(self.stock._observers), 2)
    
    def test_detach_observer(self):
        """Test detaching observers from subject"""
        self.stock.attach(self.display1)
        self.stock.attach(self.display2)
        
        self.stock.detach(self.display1)
        self.assertEqual(len(self.stock._observers), 1)
        self.assertIn(self.display2, self.stock._observers)
    
    def test_notify_observers(self):
        """Test that observers are notified when stock price changes"""
        self.stock.attach(self.display1)
        self.stock.attach(self.display2)
        
        # Capture stdout to verify notifications
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.stock.price = 155.0
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Portfolio App: AAPL is now $155.0", output)
        self.assertIn("Trading Dashboard: AAPL is now $155.0", output)
    
    def test_stock_properties(self):
        """Test stock symbol and price properties"""
        self.assertEqual(self.stock.symbol, "AAPL")
        self.assertEqual(self.stock.price, 150.0)
        
        self.stock.price = 160.0
        self.assertEqual(self.stock.price, 160.0)
    
    def test_no_observers_no_error(self):
        """Test that setting price with no observers doesn't cause errors"""
        try:
            self.stock.price = 140.0
            self.assertEqual(self.stock.price, 140.0)
        except Exception as e:
            self.fail(f"Setting price with no observers raised {e}")


if __name__ == '__main__':
    unittest.main()
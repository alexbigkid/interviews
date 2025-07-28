import unittest
from src.design_patterns.decorator import (
    SimpleCoffee, MilkDecorator, SugarDecorator, WhipDecorator
)


class TestDecorator(unittest.TestCase):
    
    def test_simple_coffee(self):
        """Test simple coffee without decorators"""
        coffee = SimpleCoffee()
        self.assertEqual(coffee.cost(), 2.0)
        self.assertEqual(coffee.description(), "Simple Coffee")
    
    def test_milk_decorator(self):
        """Test adding milk to coffee"""
        coffee = SimpleCoffee()
        coffee_with_milk = MilkDecorator(coffee)
        
        self.assertEqual(coffee_with_milk.cost(), 2.5)  # 2.0 + 0.5
        self.assertEqual(coffee_with_milk.description(), "Simple Coffee, Milk")
    
    def test_sugar_decorator(self):
        """Test adding sugar to coffee"""
        coffee = SimpleCoffee()
        coffee_with_sugar = SugarDecorator(coffee)
        
        self.assertEqual(coffee_with_sugar.cost(), 2.2)  # 2.0 + 0.2
        self.assertEqual(coffee_with_sugar.description(), "Simple Coffee, Sugar")
    
    def test_whip_decorator(self):
        """Test adding whip to coffee"""
        coffee = SimpleCoffee()
        coffee_with_whip = WhipDecorator(coffee)
        
        self.assertEqual(coffee_with_whip.cost(), 2.7)  # 2.0 + 0.7
        self.assertEqual(coffee_with_whip.description(), "Simple Coffee, Whip")
    
    def test_multiple_decorators(self):
        """Test combining multiple decorators"""
        coffee = SimpleCoffee()
        coffee = MilkDecorator(coffee)
        coffee = SugarDecorator(coffee)
        coffee = WhipDecorator(coffee)
        
        expected_cost = 2.0 + 0.5 + 0.2 + 0.7  # 3.4
        self.assertEqual(coffee.cost(), expected_cost)
        self.assertEqual(coffee.description(), "Simple Coffee, Milk, Sugar, Whip")
    
    def test_different_decorator_order(self):
        """Test that decorator order doesn't affect final result"""
        # Order 1: Milk -> Sugar -> Whip
        coffee1 = SimpleCoffee()
        coffee1 = MilkDecorator(coffee1)
        coffee1 = SugarDecorator(coffee1)
        coffee1 = WhipDecorator(coffee1)
        
        # Order 2: Whip -> Sugar -> Milk
        coffee2 = SimpleCoffee()
        coffee2 = WhipDecorator(coffee2)
        coffee2 = SugarDecorator(coffee2)
        coffee2 = MilkDecorator(coffee2)
        
        self.assertEqual(coffee1.cost(), coffee2.cost())
        # Note: descriptions will be different due to order
    
    def test_decorator_chain_integrity(self):
        """Test that each decorator properly wraps the previous one"""
        coffee = SimpleCoffee()
        milk_coffee = MilkDecorator(coffee)
        sugar_milk_coffee = SugarDecorator(milk_coffee)
        
        # Verify the chain
        self.assertIs(sugar_milk_coffee._coffee, milk_coffee)
        self.assertIs(milk_coffee._coffee, coffee)
    
    def test_single_decorator_multiple_times(self):
        """Test applying the same decorator multiple times"""
        coffee = SimpleCoffee()
        coffee = MilkDecorator(coffee)
        coffee = MilkDecorator(coffee)  # Double milk
        
        self.assertEqual(coffee.cost(), 3.0)  # 2.0 + 0.5 + 0.5
        self.assertEqual(coffee.description(), "Simple Coffee, Milk, Milk")


if __name__ == '__main__':
    unittest.main()
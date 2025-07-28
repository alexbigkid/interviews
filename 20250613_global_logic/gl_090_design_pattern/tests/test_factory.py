import unittest
from src.design_patterns.factory import AnimalFactory, Dog, Cat, Bird


class TestFactory(unittest.TestCase):
    
    def setUp(self):
        self.factory = AnimalFactory()
    
    def test_create_dog(self):
        """Test creating a dog through factory"""
        dog = self.factory.create_animal("dog")
        self.assertIsInstance(dog, Dog)
        self.assertEqual(dog.make_sound(), "Woof!")
    
    def test_create_cat(self):
        """Test creating a cat through factory"""
        cat = self.factory.create_animal("cat")
        self.assertIsInstance(cat, Cat)
        self.assertEqual(cat.make_sound(), "Meow!")
    
    def test_create_bird(self):
        """Test creating a bird through factory"""
        bird = self.factory.create_animal("bird")
        self.assertIsInstance(bird, Bird)
        self.assertEqual(bird.make_sound(), "Tweet!")
    
    def test_case_insensitive(self):
        """Test factory works with different cases"""
        dog1 = self.factory.create_animal("DOG")
        dog2 = self.factory.create_animal("Dog")
        dog3 = self.factory.create_animal("dog")
        
        self.assertIsInstance(dog1, Dog)
        self.assertIsInstance(dog2, Dog)
        self.assertIsInstance(dog3, Dog)
    
    def test_invalid_animal_type(self):
        """Test factory raises error for unknown animal type"""
        with self.assertRaises(ValueError) as context:
            self.factory.create_animal("elephant")
        
        self.assertIn("Unknown animal type", str(context.exception))
    
    def test_multiple_instances_different(self):
        """Test that multiple instances of same type are different objects"""
        dog1 = self.factory.create_animal("dog")
        dog2 = self.factory.create_animal("dog")
        
        self.assertIsNot(dog1, dog2)
        self.assertEqual(dog1.make_sound(), dog2.make_sound())


if __name__ == '__main__':
    unittest.main()
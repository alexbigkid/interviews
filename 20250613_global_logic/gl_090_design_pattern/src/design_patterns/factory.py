"""
Factory Pattern - Creates objects without specifying exact classes
Common interview question: Animal factory, Vehicle factory
"""

from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"


class Bird(Animal):
    def make_sound(self):
        return "Tweet!"


class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        animals = {
            "dog": Dog,
            "cat": Cat,
            "bird": Bird
        }
        
        animal_class = animals.get(animal_type.lower())
        if animal_class:
            return animal_class()
        raise ValueError(f"Unknown animal type: {animal_type}")


# Usage example
if __name__ == "__main__":
    factory = AnimalFactory()
    
    dog = factory.create_animal("dog")
    cat = factory.create_animal("cat")
    
    print(dog.make_sound())  # Woof!
    print(cat.make_sound())  # Meow!
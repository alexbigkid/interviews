# Design Patterns for Interviews

Common design patterns with Python examples, visual diagrams, and comprehensive unit tests.

## Project Structure

```
design-patterns/
├── src/
│   └── design_patterns/
│       ├── __init__.py
│       ├── singleton.py
│       ├── factory.py
│       ├── observer.py
│       ├── strategy.py
│       ├── command.py
│       ├── decorator.py
│       ├── adapter.py
│       └── builder.py
├── tests/
│   ├── __init__.py
│   ├── test_singleton.py
│   ├── test_factory.py
│   ├── test_observer.py
│   ├── test_strategy.py
│   ├── test_command.py
│   ├── test_decorator.py
│   ├── test_adapter.py
│   └── test_builder.py
├── pyproject.toml
└── README.md
```

## Setup and Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync --dev

# Or install with pip
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_singleton.py

# Run tests with verbose output
uv run pytest -v

# Run tests without coverage
uv run pytest --no-cov
```

## Running Examples

```bash
# Run all pattern examples at once
uv run python run_examples.py

# Run individual pattern examples
uv run python src/design_patterns/singleton.py
uv run python src/design_patterns/factory.py
# ... etc for other patterns
```

## 1. Singleton Pattern
**Purpose:** Ensures only one instance exists  
**Use Cases:** Database connections, loggers, caches

```mermaid
classDiagram
    class Singleton {
        -instance: Singleton
        +getInstance(): Singleton
    }
    Singleton --> Singleton : creates once
```

## 2. Factory Pattern
**Purpose:** Creates objects without specifying exact classes  
**Use Cases:** Animal factory, vehicle factory, UI components

```mermaid
classDiagram
    class AnimalFactory {
        +createAnimal(type): Animal
    }
    class Animal {
        <<abstract>>
        +makeSound()
    }
    class Dog {
        +makeSound()
    }
    class Cat {
        +makeSound()
    }
    AnimalFactory --> Animal
    Animal <|-- Dog
    Animal <|-- Cat
```

## 3. Observer Pattern
**Purpose:** One-to-many dependency notification  
**Use Cases:** Stock prices, newsletter subscriptions, MVC

```mermaid
classDiagram
    class Subject {
        -observers: List
        +attach(observer)
        +notify()
    }
    class Observer {
        <<abstract>>
        +update(subject)
    }
    class Stock {
        -price: float
        +setPrice(price)
    }
    class StockDisplay {
        +update(stock)
    }
    Subject <|-- Stock
    Observer <|-- StockDisplay
    Subject o-- Observer
```

## 4. Strategy Pattern
**Purpose:** Interchangeable algorithms  
**Use Cases:** Payment processing, sorting, compression

```mermaid
classDiagram
    class PaymentStrategy {
        <<abstract>>
        +pay(amount)
    }
    class CreditCard {
        +pay(amount)
    }
    class PayPal {
        +pay(amount)
    }
    class ShoppingCart {
        -strategy: PaymentStrategy
        +setStrategy(strategy)
        +checkout()
    }
    PaymentStrategy <|-- CreditCard
    PaymentStrategy <|-- PayPal
    ShoppingCart --> PaymentStrategy
```

## 5. Command Pattern
**Purpose:** Encapsulates requests as objects  
**Use Cases:** Undo/redo, remote controls, queuing

```mermaid
classDiagram
    class Command {
        <<abstract>>
        +execute()
        +undo()
    }
    class LightOnCommand {
        +execute()
        +undo()
    }
    class RemoteControl {
        -commands: List
        +setCommand(slot, command)
        +pressButton(slot)
    }
    class Light {
        +turnOn()
        +turnOff()
    }
    Command <|-- LightOnCommand
    RemoteControl --> Command
    LightOnCommand --> Light
```

## 6. Decorator Pattern
**Purpose:** Adds behavior dynamically  
**Use Cases:** Coffee shop, text formatting, middleware

```mermaid
classDiagram
    class Coffee {
        <<abstract>>
        +cost(): float
        +description(): string
    }
    class SimpleCoffee {
        +cost(): float
        +description(): string
    }
    class CoffeeDecorator {
        -coffee: Coffee
        +cost(): float
        +description(): string
    }
    class MilkDecorator {
        +cost(): float
        +description(): string
    }
    Coffee <|-- SimpleCoffee
    Coffee <|-- CoffeeDecorator
    CoffeeDecorator <|-- MilkDecorator
    CoffeeDecorator --> Coffee
```

## 7. Adapter Pattern
**Purpose:** Makes incompatible interfaces work together  
**Use Cases:** Third-party libraries, legacy systems

```mermaid
classDiagram
    class MediaPlayer {
        <<abstract>>
        +play(type, filename)
    }
    class AudioPlayer {
        +play(type, filename)
    }
    class MediaAdapter {
        +play(type, filename)
    }
    class VlcPlayer {
        +playVlc(filename)
    }
    MediaPlayer <|-- AudioPlayer
    MediaPlayer <|-- MediaAdapter
    MediaAdapter --> VlcPlayer
```

## 8. Builder Pattern
**Purpose:** Constructs complex objects step by step  
**Use Cases:** Computer builder, house builder, SQL queries

```mermaid
classDiagram
    class ComputerBuilder {
        <<abstract>>
        +setCPU()
        +setRAM()
        +getComputer(): Computer
    }
    class GamingComputerBuilder {
        +setCPU()
        +setRAM()
        +getComputer(): Computer
    }
    class ComputerDirector {
        -builder: ComputerBuilder
        +buildComputer(): Computer
    }
    class Computer {
        +cpu: string
        +ram: string
    }
    ComputerBuilder <|-- GamingComputerBuilder
    ComputerDirector --> ComputerBuilder
    ComputerBuilder --> Computer
```

## Interview Tips
- **Know the problem each pattern solves**
- **Identify when to use each pattern**
- **Be able to implement from scratch**
- **Understand trade-offs and alternatives**
- **Practice drawing UML diagrams**

## Additional Resources
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns) - Comprehensive guide with examples and explanations
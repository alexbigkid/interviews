"""Tests for fizz_buzz module."""

from gl_011.fizz_buzz import fizz_buzz


def test_fizz_buzz_number():
    """Test fizz_buzz returns number for non-multiples."""
    assert fizz_buzz(1) == "1"
    assert fizz_buzz(2) == "2"
    assert fizz_buzz(4) == "4"
    assert fizz_buzz(7) == "7"
    assert fizz_buzz(11) == "11"


def test_fizz_buzz_fizz():
    """Test fizz_buzz returns 'Fizz' for multiples of 3."""
    assert fizz_buzz(3) == "Fizz"
    assert fizz_buzz(6) == "Fizz"
    assert fizz_buzz(9) == "Fizz"
    assert fizz_buzz(12) == "Fizz"


def test_fizz_buzz_buzz():
    """Test fizz_buzz returns 'Buzz' for multiples of 5."""
    assert fizz_buzz(5) == "Buzz"
    assert fizz_buzz(10) == "Buzz"
    assert fizz_buzz(20) == "Buzz"
    assert fizz_buzz(25) == "Buzz"


def test_fizz_buzz_fizzbuzz():
    """Test fizz_buzz returns 'FizzBuzz' for multiples of 15."""
    assert fizz_buzz(15) == "FizzBuzz"
    assert fizz_buzz(30) == "FizzBuzz"
    assert fizz_buzz(45) == "FizzBuzz"
    assert fizz_buzz(60) == "FizzBuzz"


def test_fizz_buzz_edge_cases():
    """Test fizz_buzz edge cases."""
    assert fizz_buzz(0) == "FizzBuzz"
    assert fizz_buzz(-3) == "Fizz"
    assert fizz_buzz(-5) == "Buzz"
    assert fizz_buzz(-15) == "FizzBuzz"


def test_fizz_buzz_type_hint():
    """Test fizz_buzz function signature."""
    import inspect

    sig = inspect.signature(fizz_buzz)
    assert sig.parameters["n"].annotation is int
    assert sig.return_annotation is str

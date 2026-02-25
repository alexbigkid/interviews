"""Return the n-th Fibonacci number."""

# Standard imports
from functools import wraps


def trace(func):
    """Decorator that prints the function signature and return value."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")
        return result

    return wrapper


# @trace
def fibonacci(n):
    """Return the n-th Fibonacci number."""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


def main():
    """Main function."""
    print("Fibonacci sequence:")
    for i in range(9):
        print(f"fibonacci({i}) = {fibonacci(i)}")
    # print(f"fibonacci(7) = {fibonacci_function(7)}")
    # print(fibonacci)


if __name__ == "__main__":
    main()

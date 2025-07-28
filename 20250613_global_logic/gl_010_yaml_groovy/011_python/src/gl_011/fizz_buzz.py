"""Fizz Buzz app."""


def fizz_buzz(n: int) -> str:
    """fizz_buzz function."""
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    return result or str(n)


def main():
    """Main function to run fizz_buzz for 1-100."""
    for i in range(1, 101):
        print(fizz_buzz(i))


if __name__ == "__main__":
    main()

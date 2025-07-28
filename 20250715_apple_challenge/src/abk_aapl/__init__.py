from .solution import solution

def main():
    """Main entry point for the abk_aapl package."""
    k = 3
    a = [1, 6, 8, 2, 4, 9, 12]
    result = solution(k, a)
    print(f"Result: {result}")
    print("Expected: 3")
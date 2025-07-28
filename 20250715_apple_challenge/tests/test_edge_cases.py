from abk_aapl.simple_solution import solution

# Test edge cases
print("Testing edge cases:")

# Empty list
try:
    result = solution(3, [])
    print(f"Empty list: {result}")
except Exception as e:
    print(f"Empty list error: {e}")

# Single element
try:
    result = solution(3, [5])
    print(f"Single element: {result}")
except Exception as e:
    print(f"Single element error: {e}")

# None (this will likely cause an error)
try:
    result = solution(3, None)
    print(f"None: {result}")
except Exception as e:
    print(f"None error: {e}")

# Two identical elements with k=0
try:
    result = solution(0, [5, 5])
    print(f"Two identical with k=0: {result}")
except Exception as e:
    print(f"Two identical error: {e}")
